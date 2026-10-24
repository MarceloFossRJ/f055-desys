#!/usr/bin/env python3
"""
Validate the component specs against the token layer.

    python3 scripts/check_tokens.py

Two hard checks, both of which have already caught real bugs:

  1. Every var(--token) in a component preview resolves in the :root block of
     dist/web/tokens.css -- the stylesheet that actually ships. Checking against
     the token JSON is not enough: a name can exist as a token and still be
     unresolvable in plain CSS, which is exactly how --shadow-card came to be
     declared only inside @theme (a Tailwind construct, not a cascade layer) and
     render flat everywhere Tailwind was not in the pipeline. A missing property
     fails silently -- the declaration is dropped and the element renders with an
     inherited or initial value, which often looks almost right.

  2. No raw colour literals in a component preview. Colour is fully tokenised,
     so a hex or rgb() in a preview means the spec and the tokens have diverged.

  3. Every class a preview uses is defined in that same preview. A preview may
     depend on tokens via var(), and on nothing else -- generated utility class
     names differ between the repo stylesheet (.type-caption) and the
     design-system page (.caption), so a preview leaning on one renders
     unstyled in the other context.

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
STYLESHEET = ROOT / "dist" / "web" / "tokens.css"
COMPONENTS = ROOT / "components"

VAR_REF = re.compile(r"var\(\s*--([A-Za-z0-9_.\-]+)")
# Hex colours, and rgb()/hsl()/oklch() calls. `currentColor` and `transparent`
# are keywords, not literals, and are fine.
COLOR_LITERAL = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|oklch|oklab)\s*\(")
CLASS_ATTR = re.compile(r'class="([^"]*)"')
CLASS_RULE = re.compile(r"\.([A-Za-z][A-Za-z0-9_-]*)")

# Classes the generated stylesheet defines -- the `type-*` named styles. A
# preview may use these without redeclaring them; that is the whole point of a
# named style, and hand-copying one is the drift this checker exists to stop.
TOKEN_CLASSES = set(re.findall(
    r"^\.([a-z][a-z0-9-]*)\s*\{",
    (pathlib.Path(__file__).resolve().parent.parent / "dist" / "web" / "tokens.css").read_text(),
    re.M))


def css_root_properties() -> set[str]:
    """Custom properties declared in the :root block of the shipped stylesheet.

    Deliberately NOT @theme: those exist only after a Tailwind build, so a
    preview relying on them is broken anywhere else.
    """
    css = STYLESHEET.read_text()
    start = css.index(":root {")
    end = css.index("}", start)
    return set(re.findall(r"^\s*--([A-Za-z0-9_.\-]+)\s*:", css[start:end], re.M))


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

    if not STYLESHEET.exists():
        print(f"error: {STYLESHEET.relative_to(ROOT)} is missing. "
              f"Run: python3 scripts/build_tokens.py", file=sys.stderr)
        return 1

    defined = defined_tokens()
    resolvable = css_root_properties()
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
            if ref not in resolvable:
                extra = ("  (declared as a token, but not in :root -- is it "
                         "only inside @theme?)" if ref in defined else "")
                errors.append(
                    f"{name}: var(--{ref}) does not resolve in "
                    f"dist/web/tokens.css{extra}")

        for literal in sorted(set(COLOR_LITERAL.findall(text))):
            errors.append(f"{name}: raw colour literal  {literal!r} "
                          f"-- colour is fully tokenised, use var(--token)")

        style = text[text.index("<style>"):] if "<style>" in text else ""
        declared = set(CLASS_RULE.findall(style)) | TOKEN_CLASSES
        for attr in CLASS_ATTR.findall(text):
            for cls in attr.split():
                if cls not in declared:
                    errors.append(
                        f"{name}: class .{cls} is used but not defined in the "
                        f"preview -- previews may depend on tokens only")

        if not VAR_REF.search(text):
            errors.append(f"{name}: preview references no tokens at all")

    print(f"{len(resolvable)} properties in :root · {len(used)} referenced "
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

    print("\nAll component previews resolve against dist/web/tokens.css.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
