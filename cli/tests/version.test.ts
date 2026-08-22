/** Garante que a versão exibida pelo CLI acompanha o pacote publicado. */

import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { describe, expect, test } from "vitest";
import { VERSION } from "../src/version.js";

describe("versão pública", () => {
  test("mantém o pacote e o código executável na mesma versão", async () => {
    const packageJson = JSON.parse(
      await readFile(join(import.meta.dirname, "..", "package.json"), "utf8"),
    ) as { version: string };

    expect(VERSION).toBe(packageJson.version);
  });
});
