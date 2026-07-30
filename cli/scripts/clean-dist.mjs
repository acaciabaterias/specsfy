#!/usr/bin/env node

/**
 * Remove somente a saída compilada do CLI antes de um novo build.
 */

import { rm } from "node:fs/promises";
import { resolve } from "node:path";

await rm(resolve(import.meta.dirname, "..", "dist"), {
  recursive: true,
  force: true,
});
