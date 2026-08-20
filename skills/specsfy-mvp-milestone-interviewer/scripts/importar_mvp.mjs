#!/usr/bin/env node
/** Importa a fonte MVP.md como a milestone inicial sem sobrescrever conteúdo existente. */

import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

function fail(message) { throw new Error(message); }

function parseArgs(argv) {
  const values = {};
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    const value = argv[index + 1];
    if (!key?.startsWith("--")) fail(`argumento inválido: ${key}`);
    if (value === undefined || value.startsWith("--")) fail(`valor ausente para ${key}`);
    values[key.slice(2)] = value;
    index += 1;
  }
  return values;
}

function containsSensitiveData(content) {
  return /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:api[_-]?key|secret|token|password)\s*[:=]\s*\S+/iu.test(content);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const root = resolve(args.root ?? process.cwd());
  const source = join(root, "MVP.md");
  const destination = join(root, "specs", "milestones", "M01.md");
  let content;
  try {
    content = await readFile(source, "utf8");
  } catch (error) {
    if (error?.code === "ENOENT") fail("MVP.md não encontrado na raiz do projeto");
    throw error;
  }
  if (!content.trim()) fail("MVP.md não pode estar vazio");
  if (containsSensitiveData(content)) fail("MVP.md contém dado sensível aparente; remova-o antes de importar");

  await mkdir(resolve(root, "specs", "milestones"), { recursive: true });
  const hash = createHash("sha256").update(content).digest("hex");
  const milestone = [
    "# Milestone 1.0",
    "",
    "| Metadado | Valor |",
    "| --- | --- |",
    "| Status | Importada de MVP.md |",
    "| Origem | `MVP.md` |",
    `| Integridade da origem | SHA-256 \`${hash}\` |`,
    "",
    "## Material importado",
    "",
    content.trim(),
    "",
    "## Próximo passo",
    "",
    "Preservar a conversa em Inboxes e tratar a sessão com `$specsfy-02-backlog`.",
    "",
  ].join("\n");
  try {
    await writeFile(destination, milestone, { encoding: "utf8", flag: "wx" });
  } catch (error) {
    if (error?.code === "EEXIST") fail("a milestone 1.0 já existe e não será sobrescrita");
    throw error;
  }
  console.log(destination);
}

main().catch((error) => {
  console.error(`erro: ${error instanceof Error ? error.message : String(error)}`);
  process.exitCode = 1;
});
