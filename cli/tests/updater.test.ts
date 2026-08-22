/** Regressões da consulta, do cache e da atualização pelo npm. */
import { readFile, stat, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { describe, expect, test, vi } from "vitest";
import {
  checkForUpdate,
  ensureGlobalConfig,
  EXECUTABLE_DOWNLOAD_URL,
  NPM_REGISTRY_URL,
  npmUpgradeArguments,
  standaloneExecutablePath,
  upgradeWithExecutable,
} from "../src/updater.js";
import { temporaryDirectory } from "./helpers.js";

describe("atualizador", () => {
  test("cria cache privado e mantém as configurações padrão", async () => {
    const root = await temporaryDirectory();
    const path = join(root, ".specsfy/cli.json");

    const payload = await ensureGlobalConfig(path);

    expect(payload.schema_version).toBe(1);
    expect(payload.settings).toMatchObject({
      check_updates_on_startup: true,
      check_interval_seconds: 86400,
    });
    expect((await stat(path)).mode & 0o777).toBe(0o600);
  });

  test("seleciona a maior tag estável e armazena ETag e commit", async () => {
    const root = await temporaryDirectory();
    const path = join(root, ".specsfy/cli.json");
    const fetcher = vi.fn(async (url: RequestInfo | URL) =>
      url === NPM_REGISTRY_URL
        ? new Response(JSON.stringify({ version: "0.8.0" }), {
            status: 200,
          })
        : new Response(
            JSON.stringify([
              { name: "v0.7.0", commit: { sha: "7".repeat(40) } },
              { name: "v0.8.0", commit: { sha: "8".repeat(40) } },
              { name: "v0.9.0-beta.1", commit: { sha: "9".repeat(40) } },
            ]),
            { status: 200, headers: { etag: '"tags-v1"' } },
          ),
    );

    const update = await checkForUpdate("0.6.0", {
      cachePath: path,
      now: 1000,
      fetcher,
    });

    expect(update).toEqual({
      current_version: "0.6.0",
      latest_version: "0.8.0",
      tag: "v0.8.0",
      commit_sha: "8".repeat(40),
    });
    const payload = JSON.parse(await readFile(path, "utf8")) as {
      cache: Record<string, unknown>;
    };
    expect(payload.cache.etag).toBe('"tags-v1"');
  });

  test("reutiliza cache recente e preserva chaves desconhecidas", async () => {
    const root = await temporaryDirectory();
    const path = join(root, "cli.json");
    await writeFile(
      path,
      JSON.stringify({
        schema_version: 1,
        settings: {
          check_updates_on_startup: true,
          check_interval_seconds: 86400,
          custom: "preservar",
        },
        cache: {
          last_checked_at: 900,
          latest_version: "0.7.0",
          latest_distribution_version: "0.7.0",
          latest_tag: "v0.7.0",
          latest_commit: "7".repeat(40),
        },
      }),
    );
    const fetcher = vi.fn();

    expect(
      await checkForUpdate("0.6.0", {
        cachePath: path,
        now: 1000,
        fetcher,
      }),
    ).toMatchObject({ latest_version: "0.7.0" });
    expect(fetcher).not.toHaveBeenCalled();
    expect(await readFile(path, "utf8")).toContain("preservar");
  });

  test("usa o pacote npm oficial no upgrade", () => {
    expect(npmUpgradeArguments()).toEqual([
      "install",
      "--global",
      "@promovaweb/specsfy@latest",
    ]);
  });

  test("reconhece executável avulso pela entrada sem extensão", () => {
    expect(standaloneExecutablePath(["node", "/usr/local/bin/specsfy"])).toBe(
      "/usr/local/bin/specsfy",
    );
    expect(standaloneExecutablePath(["node", "/usr/local/bin/specsfy.cjs"])).toBe(
      undefined,
    );
  });

  test("substitui o executável avulso somente após validar a versão baixada", async () => {
    const root = await temporaryDirectory();
    const executable = join(root, "specsfy");
    const downloaded = Buffer.from(
      "#!/usr/bin/env node\n" +
        'if (process.argv[2] === "--version") console.log("0.9.0");\n',
    );
    const fetcher = vi.fn(async (url: RequestInfo | URL) => {
      expect(url).toBe(EXECUTABLE_DOWNLOAD_URL);
      return new Response(downloaded, { status: 200 });
    });

    await upgradeWithExecutable(executable, "0.9.0", fetcher);

    expect(await readFile(executable)).toEqual(downloaded);
    expect(fetcher).toHaveBeenCalledOnce();
  });

  test("não oferece downgrade quando a versão local é mais recente", async () => {
    const root = await temporaryDirectory();
    const fetcher = vi.fn(async (url: RequestInfo | URL) =>
      url === NPM_REGISTRY_URL
        ? new Response(JSON.stringify({ version: "0.8.0" }), { status: 200 })
        : new Response(
            JSON.stringify([
              { name: "v0.8.0", commit: { sha: "8".repeat(40) } },
            ]),
            { status: 200 },
          ),
    );

    expect(
      await checkForUpdate("0.8.1", {
        cachePath: join(root, "cli.json"),
        force: true,
        fetcher,
      }),
    ).toBeUndefined();
  });

  test("ignora tag não publicada para não repetir o aviso de atualização", async () => {
    const root = await temporaryDirectory();
    const fetcher = vi.fn(async (url: RequestInfo | URL) =>
      url === NPM_REGISTRY_URL
        ? new Response(JSON.stringify({ version: "0.8.1" }), { status: 200 })
        : new Response(
            JSON.stringify([
              { name: "v0.9.0", commit: { sha: "9".repeat(40) } },
            ]),
            { status: 200 },
          ),
    );

    expect(
      await checkForUpdate("0.8.1", {
        cachePath: join(root, "cli.json"),
        force: true,
        fetcher,
      }),
    ).toBeUndefined();
  });
});
