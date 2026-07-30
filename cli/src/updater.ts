/**
 * Verificação consentida de versões e atualização do pacote npm global.
 */

import { execFile } from "node:child_process";
import { chmod, mkdir } from "node:fs/promises";
import { homedir } from "node:os";
import { dirname, join } from "node:path";
import { promisify } from "node:util";
import { apiHeaders } from "./github.js";
import { isFile, readJson, writeTextAtomic } from "./filesystem.js";

const execFileAsync = promisify(execFile);

export const TAGS_API_URL =
  "https://api.github.com/repos/promovaweb/specsfy/tags?per_page=100";
export const NPM_PACKAGE_NAME = "@promovaweb/specsfy";
export const DEFAULT_CHECK_INTERVAL_SECONDS = 86_400;
const SEMANTIC_TAG = /^v?(\d+)\.(\d+)\.(\d+)$/;
const COMMIT_SHA = /^[0-9a-f]{40,64}$/;

/** Versão estável mais recente que supera a versão em execução. */
export interface UpdateInfo {
  current_version: string;
  latest_version: string;
  tag: string;
  commit_sha: string;
}

interface GlobalConfig {
  schema_version: 1;
  settings: Record<string, unknown> & {
    check_updates_on_startup: boolean;
    check_interval_seconds: number;
  };
  cache: Record<string, unknown>;
  [key: string]: unknown;
}

/** Retorna o caminho global do cache do CLI. */
export function globalConfigPath(home = homedir()): string {
  return join(home, ".specsfy", "cli.json");
}

/** Cria ou normaliza o cache global com permissão privada. */
export async function ensureGlobalConfig(
  path = globalConfigPath(),
): Promise<GlobalConfig> {
  const raw = (await isFile(path)) ? await readJson(path) : {};
  if (!raw || typeof raw !== "object" || Array.isArray(raw)) {
    throw new Error(`configuração global inválida em ${path}`);
  }
  const payload = raw as Record<string, unknown>;
  payload.schema_version = 1;
  if (
    payload.settings !== undefined &&
    (!payload.settings ||
      typeof payload.settings !== "object" ||
      Array.isArray(payload.settings))
  ) {
    throw new Error(`settings inválido em ${path}`);
  }
  if (
    payload.cache !== undefined &&
    (!payload.cache ||
      typeof payload.cache !== "object" ||
      Array.isArray(payload.cache))
  ) {
    throw new Error(`cache inválido em ${path}`);
  }
  const settings = (payload.settings as Record<string, unknown> | undefined) ?? {};
  const cache = (payload.cache as Record<string, unknown> | undefined) ?? {};
  settings.check_updates_on_startup ??= true;
  settings.check_interval_seconds ??= DEFAULT_CHECK_INTERVAL_SECONDS;
  payload.settings = settings;
  payload.cache = cache;
  await writeGlobalConfig(path, payload as GlobalConfig);
  return payload as GlobalConfig;
}

/** Consulta tags com cache e retorna somente atualização estável válida. */
export async function checkForUpdate(
  currentVersion: string,
  options: {
    cachePath?: string;
    now?: number;
    force?: boolean;
    fetcher?: typeof fetch;
  } = {},
): Promise<UpdateInfo | undefined> {
  const target = options.cachePath ?? globalConfigPath();
  const payload = await ensureGlobalConfig(target);
  const { settings, cache } = payload;
  if (settings.check_updates_on_startup === false && !options.force) return undefined;
  const timestamp = options.now ?? Date.now() / 1000;
  const checkedAt = cache.last_checked_at;
  const interval = settings.check_interval_seconds;
  if (
    !options.force &&
    typeof checkedAt === "number" &&
    typeof interval === "number" &&
    interval > 0 &&
    timestamp - checkedAt < interval
  ) {
    return cachedUpdate(currentVersion, cache);
  }
  const headers = await apiHeaders(`specsfy-cli/${currentVersion}`);
  if (typeof cache.etag === "string" && cache.etag) {
    headers["If-None-Match"] = cache.etag;
  }
  try {
    const response = await (options.fetcher ?? fetch)(TAGS_API_URL, {
      headers,
      signal: AbortSignal.timeout(4_000),
    });
    cache.last_checked_at = timestamp;
    delete cache.last_error;
    if (response.status === 304) {
      await writeGlobalConfig(target, payload);
      return cachedUpdate(currentVersion, cache);
    }
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const latest = latestSemanticTag((await response.json()) as unknown);
    const etag = response.headers.get("etag");
    if (etag) cache.etag = etag;
    if (latest) {
      cache.latest_version = latest.version;
      cache.latest_tag = latest.tag;
      cache.latest_commit = latest.commit;
    } else {
      delete cache.latest_version;
      delete cache.latest_tag;
      delete cache.latest_commit;
    }
    await writeGlobalConfig(target, payload);
    return cachedUpdate(currentVersion, cache);
  } catch (error) {
    cache.last_checked_at = timestamp;
    cache.last_error = error instanceof Error ? error.message : String(error);
    await writeGlobalConfig(target, payload);
    return cachedUpdate(currentVersion, cache);
  }
}

/** Comando público usado para atualizar a instalação global. */
export function npmUpgradeArguments(): string[] {
  return ["install", "--global", `${NPM_PACKAGE_NAME}@latest`];
}

/** Atualiza o pacote pelo npm encontrado no PATH. */
export async function upgradeWithNpm(): Promise<void> {
  await execFileAsync("npm", npmUpgradeArguments(), { encoding: "utf8" });
}

/** Conduz o prompt de consentimento e informa se o processo deve encerrar. */
export async function offerStartupUpdate(
  currentVersion: string,
  ask: (prompt: string) => Promise<string>,
  output: (line: string) => void = console.log,
): Promise<boolean> {
  if (!process.stdin.isTTY || !process.stdout.isTTY) return false;
  let update: UpdateInfo | undefined;
  try {
    update = await checkForUpdate(currentVersion);
  } catch (error) {
    output(
      `Aviso: não foi possível verificar atualizações: ${
        error instanceof Error ? error.message : String(error)
      }`,
    );
    return false;
  }
  if (!update) return false;
  output(
    `Uma nova versão do Specsfy CLI está disponível: ` +
      `${update.current_version} → ${update.latest_version}.`,
  );
  const answer = (await ask("Deseja atualizar agora? [s/N] ")).trim().toLowerCase();
  if (!["s", "sim", "y", "yes"].includes(answer)) {
    output("Atualização adiada. Abrindo a aplicação normalmente.");
    return false;
  }
  try {
    await upgradeWithNpm();
  } catch (error) {
    output(
      `Falha ao atualizar: ${
        error instanceof Error ? error.message : String(error)
      }. Abrindo normalmente.`,
    );
    return false;
  }
  output(
    `O npm atualizou o Specsfy CLI para ${update.latest_version}. ` +
      "O CLI será fechado; abra-o novamente para usar a nova versão.",
  );
  return true;
}

async function writeGlobalConfig(
  path: string,
  payload: GlobalConfig,
): Promise<void> {
  await mkdir(dirname(path), { recursive: true, mode: 0o700 });
  await chmod(dirname(path), 0o700);
  await writeTextAtomic(path, `${JSON.stringify(payload, null, 2)}\n`, 0o600);
  await chmod(path, 0o600);
}

function latestSemanticTag(
  tags: unknown,
): { version: string; tag: string; commit: string } | undefined {
  if (!Array.isArray(tags)) throw new Error("resposta de tags inválida");
  const candidates: Array<{
    tuple: [number, number, number];
    version: string;
    tag: string;
    commit: string;
  }> = [];
  for (const item of tags) {
    if (!item || typeof item !== "object") continue;
    const value = item as Record<string, unknown>;
    const match = typeof value.name === "string" ? SEMANTIC_TAG.exec(value.name) : null;
    const commit =
      value.commit && typeof value.commit === "object"
        ? (value.commit as Record<string, unknown>).sha
        : undefined;
    if (!match || typeof commit !== "string" || !COMMIT_SHA.test(commit)) continue;
    const tuple = [
      Number(match[1]),
      Number(match[2]),
      Number(match[3]),
    ] as [number, number, number];
    candidates.push({
      tuple,
      version: tuple.join("."),
      tag: value.name as string,
      commit,
    });
  }
  candidates.sort((left, right) => compareVersions(right.tuple, left.tuple));
  return candidates[0];
}

function cachedUpdate(
  currentVersion: string,
  cache: Record<string, unknown>,
): UpdateInfo | undefined {
  const latest = cache.latest_version;
  const tag = cache.latest_tag;
  const commit = cache.latest_commit;
  if (
    typeof latest !== "string" ||
    typeof tag !== "string" ||
    typeof commit !== "string" ||
    !COMMIT_SHA.test(commit)
  ) {
    return undefined;
  }
  const currentTuple = versionTuple(currentVersion);
  const latestTuple = versionTuple(latest);
  const tagTuple = versionTuple(tag);
  if (
    compareVersions(latestTuple, currentTuple) <= 0 ||
    compareVersions(tagTuple, latestTuple) !== 0
  ) {
    return undefined;
  }
  return {
    current_version: currentVersion,
    latest_version: latest,
    tag,
    commit_sha: commit,
  };
}

function versionTuple(version: string): [number, number, number] {
  const match = SEMANTIC_TAG.exec(version);
  if (!match) throw new Error(`versão semântica inválida: ${version}`);
  return [Number(match[1]), Number(match[2]), Number(match[3])];
}

function compareVersions(
  left: [number, number, number],
  right: [number, number, number],
): number {
  for (let index = 0; index < 3; index += 1) {
    const difference = left[index]! - right[index]!;
    if (difference) return difference;
  }
  return 0;
}
