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
for theme in ("light", "dark"):
    r = client.get("/", params={"theme": theme})
    r.raise_for_status()
    (OUT / f"{theme}.html").write_text(r.text)
    print(f"{theme}.html  {len(r.text):,} bytes")

shutil.copytree(pathlib.Path("static"), OUT / "static", dirs_exist_ok=True)
print(f"static/ copied -> {OUT}")
