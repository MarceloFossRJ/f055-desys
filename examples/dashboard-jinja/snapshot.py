"""Render both themes to static HTML, for review and for the contrast check.

    python3 snapshot.py [out_dir]

Not part of the app. It exists because a design system has to be looked at, and
a screenshot of a running server is harder to automate than a file on disk.
"""
import pathlib, shutil, sys

from starlette.testclient import TestClient

from app import app

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "out").resolve()
OUT.mkdir(parents=True, exist_ok=True)

client = TestClient(app)
for route, stem in (("/", ""), ("/login", "login-")):
    for theme in ("light", "dark"):
        r = client.get(route, params={"theme": theme})
        r.raise_for_status()
        name = f"{stem}{theme}.html"
        (OUT / name).write_text(r.text)
        print(f"{name}  {len(r.text):,} bytes")

shutil.copytree(pathlib.Path("static"), OUT / "static", dirs_exist_ok=True)
print(f"static/ copied -> {OUT}")
