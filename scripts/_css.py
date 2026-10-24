"""A deliberately small CSS reader, enough to resolve contrast and no more.

Shared by check_contrast.py's two halves. The component previews hand-write a
few flat rules; the examples ship Tailwind's minified output. Both are read
here, under one rule: **anything this cannot resolve with certainty is skipped,
never guessed.** A skipped rule can only make the checker miss a failure; a
guessed one would invent failures and train people to ignore it.

What is deliberately NOT supported, and why it is safe:
  - pseudo-classes and elements -- :hover, :focus, ::placeholder. A hover colour
    is not the resting state, so applying it would be wrong.
  - combinators -- descendant, child, sibling. Neither codebase needs them for
    colour, and resolving them properly means a real selector engine.
  - @media other than a min-width this viewport satisfies, @property, @keyframes.
  - specificity. Rules are applied in source order, last match wins, which is
    how utility CSS is designed to work anyway.
"""
from __future__ import annotations

import re

VIEWPORT_WIDTH = 1440          # what the screens are reviewed at

_PSEUDO = re.compile(r"(?<!\\):")              # a colon Tailwind did not escape
_COMBINATOR = re.compile(r"[ >+~]")
_DECL = re.compile(r"([-a-z]+)\s*:\s*([^;]+)")
_MIN_WIDTH = re.compile(r"min-width\s*:\s*(\d+(?:\.\d+)?)(px|rem)")

KEEP = {"color", "background", "background-color", "fill",
        "font-size", "font-weight", "opacity", "display", "visibility"}


def _unescape(sel: str) -> str:
    return re.sub(r"\\(.)", r"\1", sel)


def _declarations(body: str) -> dict:
    out = {}
    for prop, value in _DECL.findall(body):
        prop = prop.strip()
        if prop in KEEP:
            out[prop] = value.strip()
    return out


def _selector_key(sel: str):
    """-> (frozenset_of_classes, tag_or_None), or None if unsupported."""
    sel = sel.strip()
    if not sel or _PSEUDO.search(sel) or _COMBINATOR.search(sel) or "[" in sel:
        return None
    if sel == "*":
        return (frozenset(), None)
    parts = [p for p in re.split(r"(?<!\\)\.", sel) if p]
    if sel.startswith("."):
        return (frozenset(_unescape(p) for p in parts), None)
    tag, *classes = parts
    if not re.fullmatch(r"[a-zA-Z][a-zA-Z0-9]*", tag):
        return None
    return (frozenset(_unescape(c) for c in classes), tag.lower())


def _at_rule_is_live(prelude: str) -> bool:
    """Should the block inside this at-rule be read at review width?"""
    head = prelude.split("(")[0].strip().lower()
    # startswith, not equality: the name is part of the prelude -- "@layer
    # utilities" is where every Tailwind utility lives, and an equality test
    # silently discarded the entire stylesheet.
    if head.startswith("@layer") or head.startswith("@supports"):
        return True
    if not head.startswith("@media"):
        return False
    if head.strip() == "@media screen":
        return True
    if "prefers-color-scheme" in prelude or "print" in prelude:
        return False          # dark mode here is a class, not a media query
    widths = _MIN_WIDTH.findall(prelude)
    if not widths or "max-width" in prelude:
        return False
    return all(float(v) * (16 if unit == "rem" else 1) <= VIEWPORT_WIDTH
               for v, unit in widths)


def parse(css: str) -> list:
    """-> [(frozenset_of_classes, tag_or_None, {prop: value}), ...] in source order.

    Brace-matched rather than regex-matched, because Tailwind ships one long
    line and nested at-rules make a regex either wrong or unreadable.
    """
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    rules: list = []
    stack: list[bool] = []          # is each open at-rule block live?
    i, start = 0, 0
    while i < len(css):
        ch = css[i]
        if ch == "{":
            prelude = css[start:i].strip()
            if prelude.startswith("@"):
                stack.append(_at_rule_is_live(prelude))
                start = i + 1
            else:
                depth, j = 1, i + 1
                while j < len(css) and depth:          # find this rule's close
                    depth += (css[j] == "{") - (css[j] == "}")
                    j += 1
                if all(stack):
                    decls = _declarations(css[i + 1:j - 1])
                    if decls:
                        for one in prelude.split(","):
                            key = _selector_key(one)
                            if key:
                                rules.append((key[0], key[1], decls))
                i, start = j, j
                continue
        elif ch == "}":
            if stack:
                stack.pop()
            start = i + 1
        i += 1
    return rules


def declared(classes: set, tag: str, rules: list, prop: str):
    """Last matching rule wins -- utility CSS is built on source order."""
    value = None
    for need, want_tag, decls in rules:
        if prop not in decls:
            continue
        if want_tag and want_tag != tag:
            continue
        if need <= classes:
            value = decls[prop]
    return value


def inline(style_attr: str) -> dict:
    return _declarations(style_attr or "")
