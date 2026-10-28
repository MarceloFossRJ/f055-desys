#!/usr/bin/env python3
"""Check that dist/kotlin and dist/swift carry the right numbers.

check_kotlin_tokens.py checks that a token a source NAMES exists. Nothing
checked that the value beside the name is correct -- and the Kotlin and Swift
outputs are the two that no test, no browser and no CI job has ever executed.

This is not circular. The flat JSON passes the token dicts through unchanged;
the native outputs go through a different code path -- px() parsing, dp and sp
conversion, camelCase renaming, ARGB packing for Kotlin, 0-1 float components
for Swift. That layer is where a unit slip, a rounding error, a dropped alpha
channel or a mangled negative lives, and until now nothing looked at it.

Standard library only.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FLAT = json.loads((ROOT / "dist" / "tokens.flat.json").read_text())
KT = ROOT / "dist" / "kotlin"
SW = ROOT / "dist" / "swift" / "F055Tokens.swift"

FLOAT_TOL = 0.001          # Swift components are written to four decimals


def camel(name: str) -> str:
    head, *rest = name.split("-")
    return head + "".join(w[:1].upper() + w[1:] for w in rest)


def px(value: str) -> float:
    return float(str(value).replace("px", ""))


def fmt(v: float) -> str:
    return f"{v:g}"


# ------------------------------------------------------------------- parsing
def kotlin_object(blob: str, name: str) -> dict:
    m = re.search(rf"\bobject\s+{name}\s*(?::\s*\w+\s*)?\{{", blob)
    if not m:
        return {}
    depth, i = 1, m.end()
    while i < len(blob) and depth:
        depth += (blob[i] == "{") - (blob[i] == "}")
        i += 1
    body = blob[m.end():i]
    out = {}
    for k, v in re.findall(r"\bval\s+(\w+)\s*:\s*\w+\s*=\s*([^\n]+)", body):
        out[k] = v.strip().rstrip(",")
    return out


def swift_enum(blob: str, name: str) -> dict:
    m = re.search(rf"\b(?:public\s+)?(?:enum|struct)\s+{name}\s*(?::[^{{]*)?\{{", blob)
    if not m:
        return {}
    depth, i = 1, m.end()
    while i < len(blob) and depth:
        depth += (blob[i] == "{") - (blob[i] == "}")
        i += 1
    body = blob[m.end():i]
    return {k: v.strip() for k, v in
            re.findall(r"public\s+(?:static\s+)?let\s+(\w+)\s*:\s*CGFloat\s*=\s*([^\n]+)", body)}


# -------------------------------------------------------------------- checks
def check_dimensions(errors: list) -> int:
    kt_blob = "\n".join(p.read_text() for p in sorted(KT.glob("*.kt")))
    sw_blob = SW.read_text()
    n = 0
    families = [
        ("radius",  FLAT["radius"],  "F055Radius",  "F055Radius",  lambda k: f"s{k}" if k[0].isdigit() else k),
        ("spacing", FLAT["spacing"], "F055Space",   "F055Space",   lambda k: f"s{k}"),
        ("size",    FLAT["size"],    "F055Size",    "F055Size",    lambda k: f"s{k}"),
    ]
    for label, src, kt_obj, sw_obj, key in families:
        kt = kotlin_object(kt_blob, kt_obj)
        sw = swift_enum(sw_blob, sw_obj)
        if not kt:
            errors.append(f"kotlin: object {kt_obj} not found"); continue
        for token, meta in src.items():
            want = px(meta["value"])
            name = key(token)
            n += 1
            got = kt.get(name)
            if got is None:
                errors.append(f"kotlin {kt_obj}.{name}: missing (expected {fmt(want)}.dp)")
            elif got != f"{fmt(want)}.dp":
                errors.append(f"kotlin {kt_obj}.{name}: {got!r}, expected {fmt(want)}.dp")
            if sw:
                n += 1
                got = sw.get(name)
                if got is None:
                    errors.append(f"swift {sw_obj}.{name}: missing (expected {fmt(want)})")
                elif got != fmt(want):
                    errors.append(f"swift {sw_obj}.{name}: {got!r}, expected {fmt(want)}")

    # control roles resolve to the size they point at
    kt_ctl = kotlin_object(kt_blob, "F055Control")
    for role, meta in FLAT["control"].items():
        name = camel(role)
        n += 1
        want = f"F055Size.s{int(px(meta['value']))}"
        got = kt_ctl.get(name)
        if got != want:
            errors.append(f"kotlin F055Control.{name}: {got!r}, expected {want}")
    return n


def check_colours(errors: list) -> int:
    kt_blob = (KT / "F055Colors.kt").read_text()
    sw_blob = SW.read_text()
    n = 0
    for mode, kt_obj in (("light", "F055Light"), ("dark", "F055Dark")):
        kt = kotlin_object(kt_blob, kt_obj)
        if not kt:
            errors.append(f"kotlin: object {kt_obj} not found"); continue
        for token, modes in FLAT["colors"].items():
            spec = modes[mode]
            name = camel(token)
            r, g, b = (int(spec["hex"].lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
            a = round(float(spec["alpha"]) * 255)
            n += 1
            want = f"Color(0x{a:02X}{r:02X}{g:02X}{b:02X})"
            got = kt.get(name)
            if got is None:
                errors.append(f"kotlin {kt_obj}.{name}: missing (expected {want})")
            elif got.upper() != want.upper():
                errors.append(f"kotlin {kt_obj}.{name}: {got!r}, expected {want}")

    # Swift writes components as 0-1 floats
    for mode in ("light", "dark"):
        m = re.search(rf"\b(?:public\s+)?struct\s+F055{mode.capitalize()}\w*\b[^{{]*\{{", sw_blob)
        body = sw_blob if not m else sw_blob
        for token, modes in FLAT["colors"].items():
            spec = modes[mode]
            name = camel(token)
            r, g, b = (int(spec["hex"].lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
            pat = re.compile(
                rf"let\s+{name}\s*:\s*Color\s*=\s*Color\(\.sRGB,\s*red:\s*([\d.]+),\s*"
                rf"green:\s*([\d.]+),\s*blue:\s*([\d.]+),\s*opacity:\s*([\d.]+)\)")
            found = pat.findall(body)
            if not found:
                continue          # the Swift output ships light only; see its header
            n += 1
            fr, fg, fb, fa = (float(x) for x in found[0])
            if max(abs(fr - r), abs(fg - g), abs(fb - b)) > FLOAT_TOL:
                errors.append(
                    f"swift {name} ({mode}): ({fr}, {fg}, {fb}) vs expected "
                    f"({r:.4f}, {g:.4f}, {b:.4f})")
            if abs(fa - float(spec["alpha"])) > FLOAT_TOL:
                errors.append(f"swift {name} ({mode}) opacity: {fa} vs {spec['alpha']}")
        break                      # Swift carries one scheme; checking it once is enough
    return n


def check_type(errors: list) -> int:
    kt_blob = (KT / "F055Type.kt").read_text()
    sw_blob = SW.read_text()
    n = 0
    for token, style in FLAT["typography"]["styles"].items():
        name = camel(token)
        m = re.search(rf"val\s+{name}\s*:\s*TextStyle\s*=\s*TextStyle\((.*?)\n    \)", kt_blob, re.S)
        if not m:
            errors.append(f"kotlin F055Type.{name}: not found"); continue
        body = m.group(1)
        for prop, want, unit in (
            ("fontSize", px(style["fontSize"]), "sp"),
            ("lineHeight", px(style["lineHeight"]), "sp"),
        ):
            n += 1
            got = re.search(rf"{prop}\s*=\s*([-\d.]+)\.{unit}", body)
            if not got or abs(float(got.group(1)) - want) > FLOAT_TOL:
                errors.append(f"kotlin {name}.{prop}: {got and got.group(1)}, expected {fmt(want)}")
        n += 1
        w = re.search(r"fontWeight\s*=\s*FontWeight\((\d+)\)", body)
        if not w or int(w.group(1)) != style["fontWeight"]:
            errors.append(f"kotlin {name}.fontWeight: {w and w.group(1)}, expected {style['fontWeight']}")

        ls = style.get("letterSpacing")
        got = re.search(r"letterSpacing\s*=\s*([-\d.]+)\.sp", body)
        n += 1
        if ls and (not got or abs(float(got.group(1)) - px(ls)) > FLOAT_TOL):
            errors.append(f"kotlin {name}.letterSpacing: {got and got.group(1)}, expected {fmt(px(ls))}")
        if not ls and got:
            errors.append(f"kotlin {name}.letterSpacing: {got.group(1)} set, but the token has none")

        # Swift publishes tracking as a separate constant
        if ls:
            n += 1
            sw = re.search(rf"let\s+{name}Tracking\s*:\s*CGFloat\s*=\s*([-\d.]+)", sw_blob)
            if not sw or abs(float(sw.group(1)) - px(ls)) > FLOAT_TOL:
                errors.append(f"swift {name}Tracking: {sw and sw.group(1)}, expected {fmt(px(ls))}")
    return n


IMPL = re.compile(r"\bobject\s+(\w+)?\s*:\s*(F055\w+)\s*\{")


def check_overrides(errors: list) -> int:
    """Every interface member an object implements must say `override`.

    Kotlin rejects the file otherwise -- "hides member of supertype and needs
    'override' modifier". The generator emitted 130 such declarations across
    F055Colors.kt and F055Type.kt and nothing noticed, because until the Compose
    example got a real build nothing ever compiled the generated Kotlin. This is
    a structural check, not a type check, but it catches that whole class.
    """
    blob = "\n".join(p.read_text() for p in sorted(KT.glob("*.kt")))
    n = 0
    for m in IMPL.finditer(blob):
        obj, iface = m.group(1) or "<anonymous>", m.group(2)
        members = members_of_interface(blob, iface)
        if not members:
            errors.append(f"kotlin: interface {iface} has no members, or was not parsed")
            continue
        depth, i = 1, m.end()
        while i < len(blob) and depth:
            depth += (blob[i] == "{") - (blob[i] == "}")
            i += 1
        body = blob[m.end():i]
        for name in sorted(members):
            n += 1
            if re.search(rf"\boverride\s+val\s+{name}\b", body):
                continue
            if re.search(rf"(?<!override )\bval\s+{name}\b", body):
                errors.append(
                    f"kotlin {obj} : {iface}: `val {name}` needs `override` -- "
                    f"this file does not compile")
            else:
                errors.append(f"kotlin {obj} : {iface}: does not implement {name}")
    return n


def members_of_interface(blob: str, name: str) -> set:
    m = re.search(rf"\binterface\s+{name}\s*\{{", blob)
    if not m:
        return set()
    depth, i = 1, m.end()
    while i < len(blob) and depth:
        depth += (blob[i] == "{") - (blob[i] == "}")
        i += 1
    return set(re.findall(r"\bval\s+(\w+)\s*:", blob[m.end():i]))


def main() -> int:
    errors: list = []
    n = (check_dimensions(errors) + check_colours(errors)
         + check_type(errors) + check_overrides(errors))
    print(f"Native tokens: {n} checks against dist/tokens.flat.json and the "
          f"interfaces the outputs declare.")
    if n < 200:
        print(f"Only {n} comparisons ran -- the parser is not finding the outputs, "
              f"so a pass here would mean nothing.")
        return 1
    if errors:
        print(f"\n{len(errors)} value(s) wrong in the generated native outputs:\n")
        for e in errors[:40]:
            print(f"  {e}")
        if len(errors) > 40:
            print(f"  ... and {len(errors) - 40} more")
        print("\nNothing compiles or runs these outputs, so this is the only thing")
        print("checking the numbers in them.")
        return 1
    print("Kotlin and Swift agree with the flat token file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
