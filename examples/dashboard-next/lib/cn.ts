/** Minimal class joiner. The system has no variant library and does not need one. */
export function cn(...parts: Array<string | false | null | undefined>) {
  return parts.filter(Boolean).join(' ');
}
