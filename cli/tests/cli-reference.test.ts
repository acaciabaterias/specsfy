/**
 * Contrato entre a gramática do Commander e a referência pública do CLI.
 *
 * Evita que um comando executável seja publicado sem seção própria e sem os
 * cinco usos exigidos pelo manual do produto.
 */

import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import type { Command } from "commander";
import { describe, expect, it } from "vitest";
import { buildProgram } from "../src/cli.js";

/** Retorna apenas comandos que executam uma ação, com seu caminho completo. */
function actionCommands(command: Command, prefix = "specsfy"): string[] {
  return command.commands.flatMap((child) => {
    const path = `${prefix} ${child.name()}`;
    return child.commands.length ? actionCommands(child, path) : [path];
  });
}

/** Isola o conteúdo de uma seção H2 da referência Markdown. */
function referenceSection(reference: string, command: string): string {
  const heading = `## \`${command}\``;
  const start = reference.indexOf(heading);
  if (start === -1) return "";
  const next = reference.indexOf("\n## ", start + heading.length);
  return reference.slice(start, next === -1 ? undefined : next);
}

describe("referência pública do CLI", () => {
  it("documenta o comando raiz e cada comando executável", async () => {
    const reference = await readFile(
      resolve(process.cwd(), "../docs/user/cli-reference.md"),
      "utf8",
    );
    const commands = ["specsfy", ...actionCommands(buildProgram())];

    for (const command of commands) {
      expect(referenceSection(reference, command), command).not.toBe("");
    }
  });

  it("mantém pelo menos cinco exemplos em cada seção de comando", async () => {
    const reference = await readFile(
      resolve(process.cwd(), "../docs/user/cli-reference.md"),
      "utf8",
    );
    const commands = ["specsfy", ...actionCommands(buildProgram())];

    for (const command of commands) {
      const section = referenceSection(reference, command);
      const examples = section.match(/^.*\bspecsfy\b.*$/gmu) ?? [];
      expect(examples.length, command).toBeGreaterThanOrEqual(5);
    }
  });
});
