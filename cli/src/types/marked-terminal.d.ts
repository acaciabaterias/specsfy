/** Tipos mínimos usados pela integração com marked-terminal. */
declare module "marked-terminal" {
  import type { MarkedExtension } from "marked";

  export interface MarkedTerminalOptions {
    reflowText?: boolean;
    width?: number;
    showSectionPrefix?: boolean;
  }

  export function markedTerminal(
    options?: MarkedTerminalOptions,
    highlightOptions?: Record<string, unknown>,
  ): MarkedExtension;
}
