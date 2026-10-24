#!/usr/bin/env python3
"""Measure text contrast against WCAG AA, in both themes, without a browser.

Two halves:

  previews  the 40 component specs, which carry their own <style> block
  screens   the built examples -- real pages, Tailwind's minified output, and
            markup produced by React and by Jinja

The second half exists because the first is not enough. Every rule this file
enforces was found by rendering a screen and measuring the live DOM; the specs
being accessible says nothing about whether the screens assembled from them are.

Dark mode needs no second parse: neither example uses a single `dark:` variant,
because the semantic tokens flip under `.dark` on their own. So the same markup
is measured twice, once against each mode's token values.

Standard library only -- CI needs no browser and no install.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _css  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Token values come from the generated flat file, not from the stylesheet's own
# :root. CI already fails when dist/ drifts from tokens/, so the two cannot
# disagree -- and this way the checker measures how tokens are USED, which is
# where the mistakes are, rather than re-deriving values it already has.
FLAT = json.loads((ROOT / "dist" / "tokens.flat.json").read_text())
COLORS = FLAT["colors"]
PAGE = {"light": (255, 255, 255), "dark": (10, 10, 10)}       # --background

AA_BODY, AA_LARGE = 4.5, 3.0
SKIP_CLASS = {"sr-only"}

# Non-colour custom properties, so font-size can be resolved through var().
SCALARS: dict[str, str] = {}
for _k, _v in FLAT["typography"]["scale"].items():
    SCALARS[f"text-{_k}"] = _v["fontSize"]
    SCALARS[f"text-{_k}--line-height"] = _v["lineHeight"]
for _fam, _vals in (("size", FLAT["size"]), ("space", FLAT["spacing"]), ("radius", FLAT["radius"])):
    for _k, _v in _vals.items():
        SCALARS[f"{_fam}-{_k}"] = _v["value"]
for _k, _v in FLAT["control"].items():
    SCALARS[f"control-{_k}"] = _v["value"]


# ------------------------------------------------------------------- colour
def _hex_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _lin(c: float) -> float:
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb) -> float:
    r, g, b = (_lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b) -> float:
    l1, l2 = sorted((luminance(a), luminance(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def over(fg, alpha, bg):
    return tuple(f * alpha + b * (1 - alpha) for f, b in zip(fg, bg))


VAR = re.compile(r"var\(\s*--([a-z0-9-]+)\s*(?:,[^)]*)?\)")
RGBA = re.compile(r"rgba?\(\s*([\d.]+)[ ,]+([\d.]+)[ ,]+([\d.]+)(?:[ ,/]+([\d.%]+))?\s*\)")


def resolve_colour(value: str, mode: str):
    """-> ((r, g, b), alpha) or None when it is not a colour this can resolve."""
    if not value:
        return None
    value = value.strip()
    m = VAR.search(value)
    if m:
        t = COLORS.get(m.group(1))
        if t is None:
            return None
        return _hex_rgb(t[mode]["hex"]), float(t[mode]["alpha"])
    if value.startswith("#"):
        h = value.split()[0].lstrip("#")
        if len(h) in (6, 8):
            a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
            return _hex_rgb(h[:6]), a
        return None
    m = RGBA.match(value)
    if m:
        r, g, b, a = m.groups()
        alpha = 1.0 if a is None else (float(a[:-1]) / 100 if a.endswith("%") else float(a))
        return (float(r), float(g), float(b)), alpha
    return None


def resolve_px(value: str):
    if not value:
        return None
    m = VAR.search(value)
    if m:
        value = SCALARS.get(m.group(1), "")
    value = value.strip()
    if value.endswith("px"):
        try:
            return float(value[:-2])
        except ValueError:
            return None
    if value.endswith("rem"):
        try:
            return float(value[:-3]) * 16
        except ValueError:
            return None
    return None


# --------------------------------------------------------------------- html
class Tree(HTMLParser):
    VOID = {"br", "img", "input", "hr", "meta", "link", "source", "col",
            "path", "circle", "line", "rect", "use", "stop", "polyline", "polygon", "ellipse"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = {"tag": "root", "classes": set(), "style": {}, "kids": [],
                     "text": "", "parent": None}
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        node = {"tag": tag.lower(),
                "classes": set((a.get("class") or "").split()),
                "style": _css.inline(a.get("style")),
                "kids": [], "text": "", "parent": self.cur}
        self.cur["kids"].append(node)
        if tag.lower() not in self.VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag.lower() not in self.VOID and self.cur["parent"] is not None:
            self.cur = self.cur["parent"]

    def handle_endtag(self, tag):
        if tag.lower() not in self.VOID and self.cur["parent"] is not None:
            self.cur = self.cur["parent"]

    def handle_data(self, data):
        if data.strip():
            self.cur["text"] += data.strip() + " "


def build_tree(html: str):
    html = re.sub(r"<(script|style|template)\b.*?</\1>", "", html, flags=re.S | re.I)
    t = Tree()
    t.feed(html)
    return t.root


# ------------------------------------------------------------------- walking
def prop(node, rules, name):
    """Inline style beats the stylesheet, as in a browser."""
    if name in node["style"]:
        return node["style"][name]
    return _css.declared(node["classes"], node["tag"], rules, name)


def walk(node, rules, mode, inherited, out, where):
    if node["classes"] & SKIP_CLASS:
        return
    if (prop(node, rules, "display") or "").strip() == "none":
        return
    if (prop(node, rules, "visibility") or "").strip() == "hidden":
        return

    colour, fs, fw, stack = (inherited["colour"], inherited["fs"],
                             inherited["fw"], inherited["stack"])

    # Inside an <svg>, text is painted by `fill`, not by `color`.
    paint = "fill" if node["tag"] in ("svg", "text", "tspan") else "color"
    c = resolve_colour(prop(node, rules, paint), mode) or resolve_colour(prop(node, rules, "color"), mode)
    if c:
        colour = c
    v = resolve_px(prop(node, rules, "font-size"))
    if v:
        fs = v
    v = (prop(node, rules, "font-weight") or "").strip()
    if v.isdigit():
        fw = int(v)
    elif v in ("bold",):
        fw = 700

    bg = (resolve_colour(prop(node, rules, "background-color"), mode)
          or resolve_colour(prop(node, rules, "background"), mode))
    if bg:
        stack = stack + [bg]

    if node["text"] and colour:
        base = PAGE[mode]
        for layer in stack:
            base = over(layer[0], layer[1], base)
        fg = over(colour[0], colour[1], base)
        need = AA_LARGE if (fs >= 18.66 or (fs >= 14 and fw >= 700)) else AA_BODY
        ratio = contrast(fg, base)
        if ratio < need - 0.005:
            out.append((where, mode, node["text"].strip()[:34], round(ratio, 2),
                        need, f"{fs:g}px/{fw}"))

    inh = {"colour": colour, "fs": fs, "fw": fw, "stack": stack}
    for k in node["kids"]:
        walk(k, rules, mode, inh, out, where)


STATS: dict[str, dict] = {}


def measure(html: str, css: str, where: str, failures: list) -> int:
    rules = _css.parse(css)
    tree = build_tree(html)
    for mode in ("light", "dark"):
        walk(tree, rules, mode,
             {"colour": (_hex_rgb(COLORS["foreground"][mode]["hex"]), 1.0),
              "fs": 16.0, "fw": 400, "stack": []},
             failures, where)
    STATS[where] = {
        "rules": len(rules),
        "colour_rules": sum(1 for r in rules
                            if {"color", "background-color", "background", "fill"} & set(r[2])),
    }
    return 2


# -------------------------------------------------------------------- halves
def check_previews(failures: list) -> int:
    passes = 0
    for f in sorted((ROOT / "components").glob("*/preview.html")):
        src = f.read_text()
        css = "\n".join(re.findall(r"<style>(.*?)</style>", src, re.S))
        passes += measure(src, css, f.parent.name, failures)
    return passes


NEXT_CSS  = ["examples/dashboard-next/out/_next/static/chunks/*.css"]
JINJA_CSS = ["examples/dashboard-jinja/out/static/css/app.css"]
RAILS_CSS = ["examples/login-rails/out/assets/application.css"]

SCREENS = [
    ("dashboard-next",   "examples/dashboard-next/out/index.html",        NEXT_CSS),
    ("dashboard-jinja",  "examples/dashboard-jinja/out/light.html",       JINJA_CSS),
    ("login-next",       "examples/dashboard-next/out/login.html",        NEXT_CSS),
    ("login-jinja",      "examples/dashboard-jinja/out/login-light.html", JINJA_CSS),
    ("login-rails",      "examples/login-rails/out/login-light.html",     RAILS_CSS),
    # The error variant, so destructive-text on a card is measured and not just
    # asserted -- it is the pair that broke twice.
    ("login-rails-error", "examples/login-rails/out/login-light-error.html", RAILS_CSS),
    # No stylesheet at all: a mailer is inline styles only, built from the
    # generated Ruby tokens. This is the one screen where dist/ruby is load
    # bearing, so it is the one place its contrast can actually be wrong.
    ("password-reset-email", "examples/login-rails/out/password-reset-email.html", []),
]


def check_screens(failures: list):
    passes, skipped = 0, []
    for name, html_rel, css_globs in SCREENS:
        html_path = ROOT / html_rel
        css_paths = [p for g in css_globs for p in sorted(ROOT.glob(g))]
        if not html_path.exists() or (css_globs and not css_paths):
            skipped.append(name)
            continue
        css = "\n".join(p.read_text() for p in css_paths)
        passes += measure(html_path.read_text(), css, name, failures)
    return passes, skipped


# ----------------------------------------------------------------- self-test
# A checker that cannot fail is worse than no checker: it reads as evidence and
# carries none. These fixtures assert that this one still catches what it is
# for, and they are run before the real pass, in CI as well as by hand.
#
# Case 5 exists because of a real bug. The at-rule test compared the whole
# prelude, so "@layer utilities" never matched "@layer" and the entire Tailwind
# utility layer was discarded. Every screen still reported a clean pass, because
# with no background rules every text node was measured against the bare page.

_UTIL_CSS = """
@layer utilities{
  .text-muted-foreground{color:var(--muted-foreground)}
  .text-destructive-text{color:var(--destructive-text)}
  .text-primary-foreground{color:var(--primary-foreground)}
  .text-border{color:var(--border)}
  .bg-muted{background-color:var(--muted)}
  .bg-card{background-color:var(--card)}
  .bg-primary{background-color:var(--primary)}
  .text-sm{font-size:var(--text-sm)}
  .hover\\:text-foreground:hover{color:var(--foreground)}
}
"""


def _fixture(bg: str, fg: str) -> str:
    return f'<div class="{bg}"><span class="{fg} text-sm">x</span></div>'


_CASES = [
    # The system's own rules, so these fixtures fail the day someone loosens one.
    ("destructive-text on muted must fail", False,
     _fixture("bg-muted", "text-destructive-text")),          # 4.38 light
    ("muted-foreground on muted must now pass", True,
     _fixture("bg-muted", "text-muted-foreground")),          # 7.17 since neutral.600
    ("muted-foreground on card must pass", True,
     _fixture("bg-card", "text-muted-foreground")),           # 7.81

    # Reads a background out of @layer utilities. This one passes ONLY if the
    # layer was read: without the fill, primary-foreground sits on the page and
    # drops to about 1.05:1. It exists because the at-rule test once compared
    # the whole prelude, so "@layer utilities" never matched "@layer" and the
    # entire Tailwind utility layer was discarded -- and every screen still
    # reported a clean pass, because every text node then sat on bare paper.
    ("a background inside @layer utilities is read", True,
     _fixture("bg-primary", "text-primary-foreground")),      # 5.87 on the fill

    # The arithmetic catches an ink nobody could see.
    ("an invisible ink must fail", False,
     _fixture("bg-card", "text-border")),                     # 1.26

    # Resting state only: if :hover were applied this would pass instead.
    ("a :hover rule must not be applied", False,
     _fixture("bg-card", "text-border hover:text-foreground")),
]


def self_test() -> int:
    bad = []
    for name, should_pass, html in _CASES:
        found: list = []
        measure(html, _UTIL_CSS, "fixture", found)
        passed = not found
        if passed != should_pass:
            bad.append(f"{name}: expected {'pass' if should_pass else 'FAIL'}, got "
                       f"{'pass' if passed else 'fail'}")
    if bad:
        print("Self-test broken -- this checker is not measuring what it claims:")
        for b in bad:
            print(f"  {b}")
        return 1
    print(f"Self-test: {len(_CASES)} fixtures behave as expected.")
    return 0


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    if self_test():
        return 1

    failures: list = []
    preview_passes = check_previews(failures)
    screen_passes, skipped = check_screens(failures)

    print(f"Contrast: {preview_passes // 2} previews and {screen_passes // 2} screens, "
          f"x2 themes = {preview_passes + screen_passes} passes.")
    if skipped:
        print(f"  skipped (not built): {', '.join(skipped)} "
              f"-- build the example to include it")

    # A screen whose stylesheet did not parse still reports a clean pass,
    # because every text node then sits on the bare page colour. Refuse that.
    for name, _, css_globs in SCREENS:
        st = STATS.get(name)
        if css_globs and st and st["colour_rules"] < 10:
            print(f"\n{name}: only {st['colour_rules']} colour rules parsed out of "
                  f"{st['rules']} -- the stylesheet did not read, so this pass means nothing.")
            return 1

    if failures:
        print(f"\n{len(failures)} text node(s) below the WCAG AA floor:\n")
        for where, mode, text, ratio, need, meta in failures:
            print(f"  {where:<18} {mode:<5} {ratio:>5.2f} / {need}  {meta:<10} {text!r}")
        print("\nA muted or accent surface pairs with accent-foreground, not")
        print("muted-foreground. Destructive ink is destructive-text, and goes on")
        print("neither. See tokens/color.json.")
        return 1

    print("Every text node clears AA in both themes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
