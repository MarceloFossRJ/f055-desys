#!/usr/bin/env python3
"""Measure text contrast in every component preview, in both themes.

Stdlib only, like the other checks, so CI needs no browser. The previews use
flat class and tag selectors with no specificity games, which is simple enough
to resolve the cascade directly: build the rule table, walk the element tree,
inherit `color` down and take the background from the nearest painted ancestor.

This exists because the rules it enforces were all found by rendering the
dashboard and measuring the live DOM, and a rule that is only written down
gets broken again. In particular it fails the build on `muted-foreground` over
`muted` or `accent`, which is 4.35:1 in light -- under AA.
"""
from __future__ import annotations
import json, pathlib, re, sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
FLAT = json.loads((ROOT / "dist" / "tokens.flat.json").read_text())
COLORS = FLAT["colors"]
PAGE = {"light": (255, 255, 255), "dark": (10, 10, 10)}   # --background

AA_BODY, AA_LARGE = 4.5, 3.0


# ---------------------------------------------------------------- colour maths
def _hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def token_rgba(name: str, mode: str):
    t = COLORS.get(name)
    if t is None:
        return None
    return _hex_rgb(t[mode]["hex"]), float(t[mode]["alpha"])


def over(fg, alpha, bg):
    return tuple(f * alpha + b * (1 - alpha) for f, b in zip(fg, bg))


def _lin(c: float) -> float:
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb) -> float:
    r, g, b = (_lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b) -> float:
    l1, l2 = sorted((luminance(a), luminance(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


# ------------------------------------------------------------------ css subset
DECL = re.compile(r"([-a-z]+)\s*:\s*([^;}]+)")
VAR = re.compile(r"var\(\s*--([a-z0-9-]+)\s*\)")
RULE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)
INTERESTING = {"color", "background", "background-color", "font-size", "font-weight", "opacity"}


def parse_css(css: str):
    """-> list of (selector_key, {prop: value}); selector_key is a class or tag."""
    out = []
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"@media[^{]*\{.*?\n\}", "", css, flags=re.S)      # skip at-rules wholesale
    for sel, body in RULE.findall(css):
        decls = {p.strip(): v.strip() for p, v in DECL.findall(body) if p.strip() in INTERESTING}
        if not decls:
            continue
        for one in sel.split(","):
            one = one.strip()
            if not one or "@" in one:
                continue
            # keep the rightmost simple key; good enough for these previews
            last = one.split()[-1].split(">")[-1].strip()
            last = re.sub(r"::?[a-z-]+(\([^)]*\))?$", "", last)     # drop pseudo
            if last.startswith("."):
                key = ("class", last[1:].split(".")[0].split("[")[0])
            elif re.fullmatch(r"[a-z][a-z0-9]*", last):
                key = ("tag", last)
            elif last == "*":
                key = ("any", "*")
            else:
                continue
            out.append((key, decls))
    return out


# ----------------------------------------------------------------- html subset
class Tree(HTMLParser):
    VOID = {"br", "img", "input", "hr", "meta", "link", "path", "circle", "line", "rect", "use", "stop"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = {"tag": "root", "classes": [], "kids": [], "text": "", "parent": None}
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        node = {"tag": tag, "classes": (a.get("class") or "").split(),
                "kids": [], "text": "", "parent": self.cur}
        self.cur["kids"].append(node)
        if tag not in self.VOID:
            self.cur = node

    def handle_endtag(self, tag):
        if tag not in self.VOID and self.cur["parent"] is not None:
            self.cur = self.cur["parent"]

    def handle_data(self, data):
        if data.strip():
            self.cur["text"] += data.strip() + " "


def declared(node, rules, prop):
    """Last matching declaration wins -- these previews never fight on specificity."""
    val = None
    for (kind, key), decls in rules:
        if prop not in decls:
            continue
        if kind == "any" or (kind == "tag" and key == node["tag"]) or (kind == "class" and key in node["classes"]):
            val = decls[prop]
    return val


def resolve_colour(value: str, mode: str):
    if not value:
        return None
    m = VAR.search(value)
    if m:
        return token_rgba(m.group(1), mode)
    if value.strip().startswith("#"):
        try:
            return _hex_rgb(value.strip().split()[0]), 1.0
        except Exception:
            return None
    if value.strip() in ("transparent", "none"):
        return None
    return None


def walk(node, rules, mode, inherited, out):
    colour = inherited["color"]
    fs, fw = inherited["font-size"], inherited["font-weight"]

    c = resolve_colour(declared(node, rules, "color"), mode)
    if c:
        colour = c
    v = declared(node, rules, "font-size")
    if v and v.endswith("px"):
        try: fs = float(v[:-2])
        except ValueError: pass
    v = declared(node, rules, "font-weight")
    if v and v.strip().isdigit():
        fw = int(v)

    bgv = declared(node, rules, "background-color") or declared(node, rules, "background")
    bg = resolve_colour(bgv, mode)
    stack = inherited["bg-stack"] + ([bg] if bg else [])

    if node["text"] and colour:
        base = PAGE[mode]
        for layer in stack:
            base = over(layer[0], layer[1], base)
        fg = over(colour[0], colour[1], base)
        need = AA_LARGE if (fs >= 18.66 or (fs >= 14 and fw >= 700)) else AA_BODY
        ratio = contrast(fg, base)
        if ratio < need - 0.005:
            out.append((node["text"].strip()[:34], round(ratio, 2), need, f"{fs:g}px/{fw}"))

    inh = {"color": colour, "font-size": fs, "font-weight": fw, "bg-stack": stack}
    for k in node["kids"]:
        walk(k, rules, mode, inh, out)


def main() -> int:
    previews = sorted((ROOT / "components").glob("*/preview.html"))
    failures, checked = [], 0
    for f in previews:
        src = f.read_text()
        css = "\n".join(re.findall(r"<style>(.*?)</style>", src, re.S))
        html = re.sub(r"<style>.*?</style>", "", src, flags=re.S)
        rules = parse_css(css)
        tree = Tree(); tree.feed(html)
        for mode in ("light", "dark"):
            out: list = []
            walk(tree.root, rules, mode,
                 {"color": token_rgba("foreground", mode), "font-size": 16.0,
                  "font-weight": 400, "bg-stack": []}, out)
            checked += 1
            for text, ratio, need, meta in out:
                failures.append((f.parent.name, mode, text, ratio, need, meta))

    print(f"Contrast: {len(previews)} previews x 2 themes, {checked} passes.")
    if failures:
        print(f"\n{len(failures)} text node(s) below the WCAG AA floor:\n")
        for comp, mode, text, ratio, need, meta in failures:
            print(f"  {comp:<18} {mode:<5} {ratio:>5.2f} / {need}  {meta:<10} {text!r}")
        print("\nCommon cause: muted-foreground over muted or accent (4.35:1 in light).")
        print("A muted or accent surface pairs with accent-foreground -- see tokens/color.json.")
        return 1
    print("Every text node clears AA in both themes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
