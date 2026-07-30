/**
 * Regressão do fingerprint usado pelo executável versionado.
 */

import { mkdir, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { describe, expect, test } from "vitest";
// @ts-expect-error O utilitário MJS não publica tipos para o pacote do CLI.
import { sourceFingerprint } from "../scripts/source-fingerprint.mjs";
import { temporaryDirectory } from "./helpers.js";

describe("fingerprint das fontes do executável", () => {
  test("ignora caches e arquivos sem efeito no build", async () => {
    const root = await temporaryDirectory();
    await mkdir(join(root, "bin"), { recursive: true });
    await mkdir(join(root, "scripts"), { recursive: true });
    await mkdir(join(root, "src"), { recursive: true });
    await writeFile(join(root, "package.json"), "{}\n");
    await writeFile(join(root, "package-lock.json"), "{}\n");
    await writeFile(join(root, "tsconfig.json"), "{}\n");
    await writeFile(join(root, "bin", "package.json"), "{}\n");
    await writeFile(join(root, "scripts", "build-executable.mjs"), "// build\n");
    await writeFile(join(root, "scripts", "source-fingerprint.mjs"), "// hash\n");
    await writeFile(join(root, "src", "main.ts"), "export {};\n");
    const original = await sourceFingerprint(root);

    await mkdir(join(root, "src", "__pycache__"));
    await writeFile(join(root, "src", "__pycache__", "legado.pyc"), "cache");
    await writeFile(join(root, "src", "diagnostico.log"), "temporário");

    expect(await sourceFingerprint(root)).toBe(original);
    await writeFile(join(root, "src", "main.ts"), "export const valor = 1;\n");
    expect(await sourceFingerprint(root)).not.toBe(original);
  });
});
