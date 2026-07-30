#!/usr/bin/env node

/**
 * Gera o executável Node.js autocontido e registra seus fingerprints.
 */

import { createHash } from "node:crypto";
import {
  chmod,
  mkdir,
  readFile,
  readdir,
  rename,
  rm,
  stat,
  writeFile,
} from "node:fs/promises";
import { dirname, join, relative, resolve } from "node:path";
import { build } from "esbuild";

const root = resolve(import.meta.dirname, "..");
const output = join(root, "bin", "specsfy");
const temporary = join(root, "bin", `.specsfy.${process.pid}.tmp`);
const manifest = join(root, "bin", "specsfy.build.json");
const packageJson = JSON.parse(await readFile(join(root, "package.json"), "utf8"));

await mkdir(dirname(output), { recursive: true });
try {
  await build({
    entryPoints: [join(root, "src", "main.ts")],
    outfile: temporary,
    bundle: true,
    platform: "node",
    target: "node22.12",
    format: "cjs",
    external: ["term.js", "pty.js"],
    alias: {
      "blessed/lib/colors": join(
        root,
        "node_modules",
        "neo-blessed",
        "lib",
        "colors.js",
      ),
    },
    banner: { js: "#!/usr/bin/env node" },
    sourcemap: false,
    minify: true,
    legalComments: "none",
    plugins: [
      {
        name: "neo-blessed-dynamic-widgets",
        setup(buildContext) {
          buildContext.onLoad(
            { filter: /neo-blessed[/\\]lib[/\\]widget\.js$/ },
            async (args) => ({
              contents: (
                await readFile(args.path, "utf8")
              ).replace(
                "require('./widgets/' + file)",
                "require('./widgets/' + file + '.js')",
              ),
              loader: "js",
            }),
          );
        },
      },
    ],
  });
  await chmod(temporary, 0o755);
  await rename(temporary, output);
} finally {
  await rm(temporary, { force: true });
}

const sourceSha256 = await sourceFingerprint(root);
const binarySha256 = createHash("sha256")
  .update(await readFile(output))
  .digest("hex");
await writeFile(
  manifest,
  `${JSON.stringify(
    {
      schema_version: 3,
      version: packageJson.version,
      runtime: "node",
      minimum_node: packageJson.engines.node,
      source_sha256: sourceSha256,
      binary_sha256: binarySha256,
    },
    null,
    2,
  )}\n`,
);

async function sourceFingerprint(directory) {
  const digest = createHash("sha256");
  const inputs = [
    join(directory, "package.json"),
    join(directory, "package-lock.json"),
    join(directory, "tsconfig.json"),
    join(directory, "bin", "package.json"),
    join(directory, "src"),
    join(directory, "scripts", "build-executable.mjs"),
  ];
  const files = [];
  for (const input of inputs) {
    const metadata = await stat(input);
    if (metadata.isDirectory()) files.push(...(await walk(input)));
    else files.push(input);
  }
  for (const file of files.sort()) {
    const metadata = await stat(file);
    digest.update(relative(directory, file));
    digest.update("\0");
    digest.update(metadata.mode & 0o111 ? "executable" : "regular");
    digest.update("\0");
    digest.update(await readFile(file));
    digest.update("\0");
  }
  return digest.digest("hex");
}

async function walk(directory) {
  const output = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) output.push(...(await walk(path)));
    else if (entry.isFile()) output.push(path);
  }
  return output;
}
