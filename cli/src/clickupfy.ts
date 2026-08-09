/** Integração opcional com ClickUpfy, sem substituir a spec local. */
import { access, readFile } from "node:fs/promises";
import { join } from "node:path";

export interface ClickUpfyHandoff {
  available: boolean;
  task_id?: string;
  action?: "transition" | "effort";
}

/** Detecta a skill instalada e lê o vínculo de tarefa do metadado da spec. */
export async function clickUpfyHandoff(
  project: string,
  specPath: string,
  action: "transition" | "effort",
): Promise<ClickUpfyHandoff> {
  const available = await hasClickUpfySkill(project);
  const content = await readFile(specPath, "utf8");
  const task = content.match(/^\|\s*ClickUp Task\s*\|\s*([^|]+?)\s*\|\s*$/imu)?.[1]?.trim();
  return task ? { available, task_id: task, action } : { available };
}

async function hasClickUpfySkill(project: string): Promise<boolean> {
  try {
    await access(join(project, ".agents", "skills", "clickupfy-executar-tarefa", "SKILL.md"));
    return true;
  } catch {
    return false;
  }
}
