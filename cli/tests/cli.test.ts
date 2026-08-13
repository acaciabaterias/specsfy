/** Contratos observáveis da interface de linha de comando. */
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { afterEach, describe, expect, test, vi } from "vitest";
import { buildProgram, runCli } from "../src/cli.js";
import { temporaryDirectory } from "./helpers.js";

describe("CLI público", () => {
  afterEach(() => {
    process.exitCode = 0;
  });

  test("expõe todos os comandos e subcomandos compatíveis", () => {
    const program = buildProgram();
    expect(
      program.commands.find((command) => command.name() === "install")?.aliases(),
    ).toContain("setup");
    expect(program.commands.map((command) => command.name())).toEqual([
      "install",
      "doctor",
      "update",
      "upgrade",
      "skills",
      "transition",
      "migrate",
      "effort",
      "progress",
      "milestones",
      "test",
      "tui",
      "config",
    ]);
    expect(
      program.commands
        .find((command) => command.name() === "skills")
        ?.commands.map((command) => command.name()),
    ).toEqual(["list", "detect", "add", "remove", "update"]);
    expect(
      program.commands
        .find((command) => command.name() === "config")
        ?.commands.map((command) => command.name()),
    ).toEqual(["show", "set"]);
    expect(
      program.commands
        .find((command) => command.name() === "milestones")
        ?.commands.map((command) => command.name()),
    ).toEqual(["sync"]);
  });

  test("progress JSON mantém summary e remove conteúdo bruto", async () => {
    const project = await temporaryDirectory();
    const path = join(project, "specs/specs/0001-dashboard/spec.md");
    await mkdir(join(path, ".."), { recursive: true });
    await writeFile(
      path,
      "# Dashboard\n\n**Status**: Implementing\n\n" +
        "- [x] T001 Feita\n- [ ] T002 Pendente\n",
    );
    const output = vi.spyOn(console, "log").mockImplementation(() => undefined);

    expect(
      await runCli([
        "node",
        "specsfy",
        "progress",
        "--project",
        project,
        "--json",
      ]),
    ).toBe(0);

    const payload = JSON.parse(String(output.mock.calls[0]?.[0])) as {
      summary: Record<string, number>;
      specs: Array<Record<string, unknown>>;
    };
    expect(payload.summary.percent).toBe(50);
    expect(payload.specs[0]?.slug).toBe("0001-dashboard");
    expect(payload.specs[0]).not.toHaveProperty("content");
  });

  test("progress vazio preserva exit code 2", async () => {
    const project = await temporaryDirectory();
    vi.spyOn(console, "log").mockImplementation(() => undefined);
    expect(
      await runCli(["node", "specsfy", "progress", "--project", project]),
    ).toBe(2);
  });

  test("install interrompe antes de escrever quando o preflight falha", async () => {
    const project = await temporaryDirectory();
    const previousPath = process.env.PATH;
    const error = vi.spyOn(console, "error").mockImplementation(() => undefined);
    process.env.PATH = "";
    try {
      expect(
        await runCli(["node", "specsfy", "install", "--project", project]),
      ).toBe(1);
      expect(String(error.mock.calls.at(-1)?.[0])).toContain(
        "pré-requisitos ausentes",
      );
    } finally {
      if (previousPath === undefined) delete process.env.PATH;
      else process.env.PATH = previousPath;
    }
  });

  test("transition e migrate expõem o ciclo de vida físico", async () => {
    const project = await temporaryDirectory();
    const path = join(project, "specs/planned/0001-dashboard/spec.md");
    await mkdir(join(path, ".."), { recursive: true });
    await writeFile(path, "# Dashboard\n\n| Status | Planned |\n| Milestones | M01 |\n");
    const output = vi.spyOn(console, "log").mockImplementation(() => undefined);

    expect(
      await runCli([
        "node", "specsfy", "transition", "0001-dashboard", "in-progress",
        "--project", project, "--json",
      ]),
    ).toBe(0);
    expect(JSON.parse(String(output.mock.calls.at(-1)?.[0]))).toMatchObject({
      to: "in-progress",
      status: "Implementing",
    });
    expect(await readFile(join(project, "specs.md"), "utf8")).toContain("M01");
  });

  test("effort registra estimativa e justificativa na spec", async () => {
    const project = await temporaryDirectory();
    const path = join(project, "specs/draft/0001-dashboard/spec.md");
    await mkdir(join(path, ".."), { recursive: true });
    await writeFile(path, "# Dashboard\n\n| Status | Draft |\n");
    const output = vi.spyOn(console, "log").mockImplementation(() => undefined);

    expect(
      await runCli([
        "node", "specsfy", "effort", "0001-dashboard", "6",
        "--reason", "Mudança atravessa CLI e skills.", "--project", project, "--json",
      ]),
    ).toBe(0);
    expect(JSON.parse(String(output.mock.calls.at(-1)?.[0]))).toMatchObject({
      effort: 6,
      identifier: "0001-dashboard",
    });
  });

  test("config set e show usam o mesmo contrato", async () => {
    const project = await temporaryDirectory();
    const output = vi.spyOn(console, "log").mockImplementation(() => undefined);

    expect(
      await runCli([
        "node",
        "specsfy",
        "config",
        "set",
        "--project",
        project,
        "--watch-interval",
        "0.5",
        "--json",
      ]),
    ).toBe(0);

    expect(JSON.parse(String(output.mock.calls.at(-1)?.[0]))).toMatchObject({
      project,
      watch_interval: 0.5,
    });
  });
});
