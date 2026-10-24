#!/usr/bin/env python3
"""Check that Kotlin sources only reference F055 tokens that exist.

There is no Kotlin toolchain in this repo's CI, so examples/login-compose is
the one implementation that is never compiled or rendered. That is stated
plainly in its README -- but "never checked at all" and "not compiled" are
different things, and the gap between them is worth closing.

This closes the part a design system is responsible for: every `F055Radius.x`,
`F055Control.x`, `colors.x` and `type.x` in a Kotlin source must exist in
dist/kotlin. It catches a token renamed in tokens/ and not followed through, or
invented from memory -- which is the failure this repo keeps finding. It does
NOT catch a Compose mistake, a type error, or a screen that does not lay out.
Do not read a pass here as "it works".

Standard library only.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist" / "kotlin"
SOURCES = sorted((ROOT / "examples").rglob("*.kt"))

OBJECTS = ("F055Radius", "F055Space", "F055Size", "F055Control", "F055Elevation")
# Locals the screens bind the composition locals to.
LOCALS = {"colors": "F055Colors", "type": "F055Type"}
# Members of a TextStyle / Color that are Compose's, not ours.
PASSTHROUGH = {"copy", "current", "value"}


def members_of_block(text: str, header: re.Pattern) -> set:
    m = header.search(text)
    if not m:
        return set()
    depth, i = 0, m.end() - 1
    while i < len(text):
        depth += (text[i] == "{") - (text[i] == "}")
        if depth == 0 and i > m.end() - 1:
            break
        i += 1
    return set(re.findall(r"\bval\s+([A-Za-z_]\w*)\s*:", text[m.end():i]))


def build_index() -> dict:
    idx: dict[str, set] = {}
    blob = "\n".join(p.read_text() for p in sorted(DIST.glob("*.kt")))
    for name in OBJECTS:
        idx[name] = members_of_block(blob, re.compile(rf"\bobject\s+{name}\s*\{{"))
    for iface in set(LOCALS.values()):
        idx[iface] = members_of_block(blob, re.compile(rf"\binterface\s+{iface}\s*\{{"))
    return idx


def main() -> int:
    if not DIST.exists():
        print("dist/kotlin missing -- run scripts/build_tokens.py")
        return 1
    idx = build_index()
    empty = [k for k, v in idx.items() if not v]
    if empty:
        print(f"Could not read members of {', '.join(empty)} -- the parser is "
              f"broken, so a pass here would mean nothing.")
        return 1

    if not SOURCES:
        print("No Kotlin sources under examples/ -- nothing to check.")
        return 0

    bad, checked = [], 0
    for f in SOURCES:
        text = re.sub(r"//[^\n]*|/\*.*?\*/", "", f.read_text(), flags=re.S)
        rel = f.relative_to(ROOT)
        for obj in OBJECTS:
            for member in re.findall(rf"\b{obj}\.([A-Za-z_]\w*)", text):
                checked += 1
                if member not in idx[obj]:
                    bad.append((rel, f"{obj}.{member}", sorted(idx[obj])))
        for local, iface in LOCALS.items():
            for member in re.findall(rf"(?<![\w.]){local}\.([A-Za-z_]\w*)", text):
                if member in PASSTHROUGH:
                    continue
                checked += 1
                if member not in idx[iface]:
                    bad.append((rel, f"{local}.{member}  ({iface})", sorted(idx[iface])))

    print(f"Kotlin tokens: {checked} references across {len(SOURCES)} source file(s).")
    if bad:
        print(f"\n{len(bad)} reference(s) to tokens that do not exist:\n")
        for rel, ref, available in bad:
            near = [a for a in available if a.lower().startswith(ref.split('.')[-1][:3].lower())]
            hint = f"  did you mean: {', '.join(near[:4])}" if near else ""
            print(f"  {rel}: {ref}{hint}")
        print("\nThese are not compiled anywhere, so this check is the only thing")
        print("standing between a renamed token and a screen that will not build.")
        return 1
    print("Every F055 token referenced from Kotlin exists in dist/kotlin.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
