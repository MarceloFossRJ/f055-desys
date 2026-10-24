/* Icon sizes read from the generated token file rather than retyped.
 *
 * This is what dist/web/tokens.js is for: CSS custom properties cannot reach a
 * React prop, so `size={16}` on a lucide icon would otherwise be a literal in
 * every call site — the exact drift the size tokens exist to prevent.
 *
 * Resolves because next.config.ts sets turbopack.root to the repo root. */
import { control } from '../../../dist/web/tokens.js';

const n = (v: string) => parseInt(v, 10);

export const ICON = {
  xs: n(control['icon-xs']),   // 12
  sm: n(control['icon-sm']),   // 14
  md: n(control.icon),         // 16
  lg: n(control['icon-lg']),   // 20
} as const;
