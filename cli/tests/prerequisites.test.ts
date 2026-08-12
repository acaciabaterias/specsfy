/** Contratos do diagnóstico executado antes de setup e atualização. */
import { chmod, mkdir, writeFile } from "node:fs/promises";
import { delimiter, join } from "node:path";
import { describe, expect, test } from "vitest";
import {
  assertPrerequisites,
  checkPrerequisites,
  nodeVersionSupported,
} from "../src/prerequisites.js";
import { temporaryDirectory } from "./helpers.js";

describe("pré-requisitos", () => {
  test("exige Node.js 22.12 ou mais recente", () => {
    expect(nodeVersionSupported("22.11.9")).toBe(false);
    expect(nodeVersionSupported("22.12.0")).toBe(true);
    expect(nodeVersionSupported("24.1.0")).toBe(true);
  });

  test("aceita skills instalado e registra todos os requisitos do setup", async () => {
    const root = await temporaryDirectory();
    const bin = join(root, "bin");
    const project = join(root, "project");
    await mkdir(bin);
    await mkdir(project);
    for (const name of ["git", "npm", "skills"]) {
      const executable = join(bin, name);
      await writeFile(executable, "#!/bin/sh\nexit 0\n");
      await chmod(executable, 0o755);
    }

    const checks = await checkPrerequisites(project, {
      path: [bin, process.env.PATH ?? ""].join(delimiter),
      nodeVersion: "22.12.0",
    });

    expect(checks.map(({ name }) => name)).toEqual([
      "node",
      "git",
      "skills",
      "npm",
      "project",
    ]);
    expect(checks.every(({ ok }) => ok)).toBe(true);
    expect(checks.find(({ name }) => name === "skills")?.detail).toContain(
      join(bin, "skills"),
    );
  });

  test("aceita npx como fallback e agrega falhas acionáveis", async () => {
    const root = await temporaryDirectory();
    const bin = join(root, "bin");
    await mkdir(bin);
    const npx = join(bin, "npx");
    await writeFile(npx, "#!/bin/sh\nexit 0\n");
    await chmod(npx, 0o755);

    const checks = await checkPrerequisites(join(root, "ausente"), {
      path: bin,
      nodeVersion: "20.0.0",
    });

    expect(checks.find(({ name }) => name === "skills")).toMatchObject({
      ok: true,
      command: [npx, "--yes", "skills"],
    });
    expect(() => assertPrerequisites(checks)).toThrow(
      /Node\.js 22\.12.*Git.*npm.*projeto/s,
    );
  });
});
