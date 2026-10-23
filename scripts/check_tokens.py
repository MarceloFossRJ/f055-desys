#!/usr/bin/env python3
"""
Validate the component specs against the token layer.

    python3 scripts/check_tokens.py

Two hard checks, both of which have already caught real bugs:

  1. Every var(--token) in a component preview resolves to a token that exists.
     A renamed or mistyped token fails silently in CSS -- the property is simply
     dropped and the element renders with an inherited or initial value, which
     often looks almost right.

  2. No raw colour literals in a component preview. Colour is fully tokenised,
     so a hex or rgb() in a preview means the spec and the tokens have diverged.

Sizes are deliberately NOT checked: control geometry has no tokens yet, and the
component READMEs list those literals under "Not yet tokenised".

Exits non-zero on any error, so CI can gate on it.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKENS = ROOT / "dist" / "artifact" / "tokens.json"
COMPONENTS = ROOT / "components"

VAR_REF = re.compile(r"var\(\s*--([A-Za-z0-9_.\-]+)")
# Hex colours, and rgb()/hsl()/oklch() calls. `currentColor` and `transparent`
# are keywords, not literals, and are fine.
COLOR_LITERAL = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|oklch|oklab)\s*\(")


def defined_tokens() -> set[str]:
    data = json.loads(TOKENS.read_text())
    names = {t["name"] for group in ("color", "radius", "spacing", "shadow")
             if group in data
             for t in data[group]["tokens"]}
    names |= {f"font-{family}" for family in data["type"]["families"]}
    return names


def main() -> int:
    if not TOKENS.exists():
        print(f"error: {TOKENS.relative_to(ROOT)} is missing. "
              f"Run: python3 scripts/build_tokens.py", file=sys.stderr)
        return 1

    defined = defined_tokens()
    previews = sorted(COMPONENTS.glob("*/preview.html"))
    if not previews:
        print("error: no component previews found under components/", file=sys.stderr)
        return 1

    errors: list[str] = []
    used: set[str] = set()

    for preview in previews:
        name = preview.parent.name
        text = preview.read_text()

        for ref in sorted(set(VAR_REF.findall(text))):
            used.add(ref)
            if ref not in defined:
                errors.append(f"{name}: undefined token  var(--{ref})")

        for literal in sorted(set(COLOR_LITERAL.findall(text))):
            errors.append(f"{name}: raw colour literal  {literal!r} "
                          f"-- colour is fully tokenised, use var(--token)")

        if not VAR_REF.search(text):
            errors.append(f"{name}: preview references no tokens at all")

    print(f"{len(defined)} tokens defined · {len(used)} referenced "
          f"across {len(previews)} previews")

    unused = sorted(defined - used)
    if unused:
        print(f"\nnote: {len(unused)} tokens unused by any preview "
              f"(expected for components not yet specified)")
        print("  " + ", ".join(unused))

    if errors:
        print(f"\n{len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    print("\nAll component previews resolve against the token layer.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
