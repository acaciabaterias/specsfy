/** Contratos do executável Node.js versionado. */
import { createHash } from "node:crypto";
import { execFile } from "node:child_process";
import { readFile, stat } from "node:fs/promises";
import { join, resolve } from "node:path";
import { promisify } from "node:util";
import { describe, expect, test } from "vitest";
import { VERSION } from "../src/version.js";

const execFileAsync = promisify(execFile);
const root = resolve(import.meta.dirname, "..");

describe("artefato executável", () => {
  test("corresponde à versão, ao runtime e ao hash registrados", async () => {
    const binary = join(root, "bin", "specsfy");
    const manifest = JSON.parse(
      await readFile(join(root, "bin", "specsfy.build.json"), "utf8"),
    ) as Record<string, unknown>;
    const bytes = await readFile(binary);

    expect((await stat(binary)).mode & 0o111).not.toBe(0);
    expect(manifest).toMatchObject({
      schema_version: 3,
      version: VERSION,
      runtime: "node",
    });
    expect(manifest.binary_sha256).toBe(
      createHash("sha256").update(bytes).digest("hex"),
    );
    const result = await execFileAsync(binary, ["--version"]);
    expect(result.stdout.trim()).toBe(VERSION);
  });
});
