/**
 * Calcula um fingerprint determinístico dos arquivos que afetam o executável.
 */

import { createHash } from "node:crypto";
import { readFile, readdir, stat } from "node:fs/promises";
import { join, relative } from "node:path";

/**
 * Retorna o SHA-256 dos manifestos, do build e das fontes TypeScript/JSON.
 *
 * Caches legados, logs e outros arquivos ignorados dentro de `src/` não
 * participam do cálculo porque não alteram o executável gerado.
 *
 * @param {string} directory Raiz absoluta ou relativa do CLI.
 * @returns {Promise<string>} SHA-256 hexadecimal dos arquivos relevantes.
 */
export async function sourceFingerprint(directory) {
  const digest = createHash("sha256");
  const inputs = [
    join(directory, "package.json"),
    join(directory, "package-lock.json"),
    join(directory, "tsconfig.json"),
    join(directory, "bin", "package.json"),
    join(directory, "src"),
    join(directory, "scripts", "build-executable.mjs"),
    join(directory, "scripts", "source-fingerprint.mjs"),
  ];
  const files = [];
  for (const input of inputs) {
    const metadata = await stat(input);
    if (metadata.isDirectory()) files.push(...(await walkSources(input)));
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

/**
 * Lista recursivamente apenas fontes consumidas pelo build.
 *
 * @param {string} directory Diretório de fontes.
 * @returns {Promise<string[]>} Caminhos de arquivos TypeScript e JSON.
 */
async function walkSources(directory) {
  const output = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) output.push(...(await walkSources(path)));
    else if (
      entry.isFile() &&
      (entry.name.endsWith(".ts") || entry.name.endsWith(".json"))
    ) {
      output.push(path);
    }
  }
  return output;
}
