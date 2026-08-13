#!/usr/bin/env node

/**
 * Gera o executável Node.js autocontido e registra seus fingerprints.
 */

import { createHash } from "node:crypto";
import {
  chmod,
  mkdir,
  readFile,
  rename,
  rm,
  writeFile,
} from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { build } from "esbuild";
import { sourceFingerprint } from "./source-fingerprint.mjs";

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
    target: "node22.20",
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
