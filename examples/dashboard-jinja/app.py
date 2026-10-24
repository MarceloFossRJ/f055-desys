"""F055 dashboard, server-rendered.

The second implementation of the same screen. Its job is to test whether the
design system survives a stack that is not React: no components, no props, no
CSS-in-JS -- just Jinja macros and the generated Python tokens.

    pip install -r requirements.txt
    npm install && npm run css
    uvicorn app:app --reload
"""
from __future__ import annotations

import pathlib
import re
import sys

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import data

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent

# The generated Python tokens, imported rather than copied -- the same rule the
# CSS follows. dist/python/ is a plain module directory, not a package.
sys.path.insert(0, str(REPO / "dist" / "python"))
import tokens  # noqa: E402

# Icons come from lucide-static in node_modules, read off disk at startup. The
# Next.js example imports lucide-react; there is no Python port, but the icon
# SOURCE can still be shared instead of retyped into this repo.
ICON_DIR = HERE / "node_modules" / "lucide-static" / "icons"


_SVG_BODY = re.compile(r"<svg[^>]*>(.*)</svg>", re.S)


def load_icon(name: str) -> str:
    """Return the INNER markup of a lucide icon -- the paths, without its <svg>.

    The file is wrapped in its own <svg> with its own width, height and stroke,
    and those must not survive: the macro supplies them from the size tokens.
    Splitting on the first ">" does not work, because the files open with an XML
    declaration, and the result is an <svg> nested inside the macro's own -- the
    inner one keeps its native 24px and quietly overflows whatever contains it.
    """
    f = ICON_DIR / f"{name}.svg"
    if not f.exists():
        raise FileNotFoundError(
            f"lucide icon {name!r} not found in {ICON_DIR}. Run `npm install`.")
    m = _SVG_BODY.search(f.read_text())
    if not m:
        raise ValueError(f"{f} does not look like an SVG")
    return m.group(1).strip()


app = FastAPI(title="F055 — Dashboard (Jinja)")
app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")

templates = Jinja2Templates(directory=HERE / "templates")
# colors, color_scheme, type, radius, space, size, control, elevation
templates.env.globals.update(tokens.jinja_globals())
templates.env.globals["icon"] = load_icon


def chart_geometry(points, width=720, height=240, pad=(44, 8, 12, 28)):
    """Area-chart path data, computed server side.

    The React version does this in the browser. Here it is plain Python, which
    is the clearer demonstration anyway: the geometry is data, not a component.
    """
    pad_l, pad_r, pad_t, pad_b = pad
    inner_w, inner_h = width - pad_l - pad_r, height - pad_t - pad_b
    top = max(max(p["current"], p["previous"]) for p in points)
    mag = 10 ** (len(str(int(top))) - 1)
    ceiling = -(-top // (mag // 2)) * (mag // 2)

    def x(i): return pad_l + (i / (len(points) - 1)) * inner_w
    def y(v): return pad_t + inner_h - (v / ceiling) * inner_h

    def path(key):
        return " ".join(f"{'ML'[bool(i)]}{x(i):.1f},{y(p[key]):.1f}" for i, p in enumerate(points))

    area = f"{path('current')} L{x(len(points) - 1):.1f},{pad_t + inner_h} L{pad_l},{pad_t + inner_h} Z"
    ticks = [{"v": t * ceiling, "y": y(t * ceiling),
              "label": f"{t * ceiling / 1000:.0f}k" if t else "0"}
             for t in (0, 0.25, 0.5, 0.75, 1)]
    return {
        "width": width, "height": height, "pad_l": pad_l, "pad_r": pad_r,
        "baseline": pad_t + inner_h, "plot_top": pad_t,
        "current": path("current"), "previous": path("previous"), "area": area,
        "ticks": ticks,
        "labels": [{"x": x(i), "text": p["label"]} for i, p in enumerate(points)],
    }


@app.get("/login", response_class=HTMLResponse)
def login(request: Request, theme: str = "light", error: bool = False):
    return templates.TemplateResponse(
        request=request, name="login.html",
        context={"theme": "dark" if theme == "dark" else "light", "error": error},
    )


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, theme: str = "light"):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "theme": "dark" if theme == "dark" else "light",
            "stats": data.STATS,
            "releases": data.RELEASES,
            "selected": data.SELECTED,
            "chart": chart_geometry(data.STREAMS),
            "nav_main": data.NAV_MAIN,
            "nav_library": data.NAV_LIBRARY,
            "nav_footer": data.NAV_FOOTER,
            "tabs": ["All releases", "In review", "Scheduled", "Takedowns"],
            "ranges": ["Last 3 months", "Last 30 days", "Last 7 days"],
        },
    )
