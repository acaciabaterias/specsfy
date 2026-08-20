#!/usr/bin/env node
/** Importa a fonte MVP.md como a milestone inicial sem sobrescrever conteúdo existente. */

import { createHash } from "node:crypto";
import { execFile } from "node:child_process";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { join, relative, resolve } from "node:path";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

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

/**
 * Retorna a raiz do superprojeto apenas quando a raiz consumidora é um
 * submódulo Git. Worktrees e projetos sem superprojeto Git não ampliam a busca.
 */
async function resolveSuperprojectRoot(root) {
  try {
    const { stdout } = await execFileAsync(
      "git",
      ["-C", root, "rev-parse", "--show-superproject-working-tree"],
      { encoding: "utf8" },
    );
    return stdout.trim() || null;
  } catch {
    return null;
  }
}

/**
 * Lê o MVP local e usa o MVP do superprojeto somente como fallback para um
 * consumidor instalado como submódulo dentro de um Hub.
 */
async function readMvpSource(root) {
  const localSource = join(root, "MVP.md");
  try {
    return { content: await readFile(localSource, "utf8"), source: localSource };
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }

  const superprojectRoot = await resolveSuperprojectRoot(root);
  if (!superprojectRoot) fail("MVP.md não encontrado na raiz do projeto");

  const source = join(superprojectRoot, "MVP.md");
  try {
    return { content: await readFile(source, "utf8"), source };
  } catch (error) {
    if (error?.code === "ENOENT") fail("MVP.md não encontrado no projeto nem no repositório pai");
    throw error;
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const root = resolve(args.root ?? process.cwd());
  const destination = join(root, "specs", "milestones", "M01.md");
  const { content, source } = await readMvpSource(root);
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
    `| Origem | \`${relative(root, source) || "MVP.md"}\` |`,
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
