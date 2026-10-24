# Dashboard — Python / FastAPI / Jinja2

The same screen as `examples/dashboard-next`, server-rendered. It exists to
answer one question: **does the system survive a stack that is not React?**

```bash
pip install -r requirements.txt
npm install && npm run build     # Tailwind CSS + fonts; both are npm-only tools
uvicorn app:app --reload         # http://localhost:8000
python3 snapshot.py out          # both themes to static HTML, for review
```

No client JavaScript at all. The theme is a query parameter, which is the
server-rendered equivalent of a toggle and keeps the page scriptless.

## What is shared, and what is not

Shared, imported rather than copied:

| | How |
|---|---|
| Colour, radius, spacing, size, elevation | `dist/web/tokens.css`, imported by `static/css/input.css` |
| The same values, in Python | `dist/python/tokens.py`, imported by `app.py` |
| Icons | `lucide-static` from npm, read off disk at startup |
| Fonts | `@fontsource`, copied into `static/` by `build_fonts.py` |

Not shared, and this is the honest result: **every component is written twice.**
`templates/components/_ui.html` and `components/ui.tsx` have the same structure,
the same tokens and the same class strings, and no common code. The repo README
predicted this from the start — "a button in Jinja2, ERB, React and Compose is
four implementations" — and building the second one confirms it. What travels is
the token layer and the written spec. Nothing else does.

## What the port exposed

### 1. `jinja_globals()` did not expose the size family — fixed

`SIZE` and `CONTROL` were added to the generated Python module but not to the
dict that `jinja_globals()` returns, so the one output built specifically for
this stack was missing the newest family. Found before a single template was
written. Fixed in `scripts/build_tokens.py`.

### 2. The Python output can do something the JS one cannot

`TYPE` gives each named style as a complete CSS declaration string:

```jinja
<text style="{{ type['caption'] }}">700k</text>
```

That is a named type style applied with no class and no stylesheet — useful
exactly where Tailwind cannot reach, which for this screen is inside the SVG.
The React version has to repeat `font-size: 12` as a literal there.

### 3. Icons have no Python port, but the source can still be shared

`lucide-static` ships the raw SVGs. `app.py` reads them at startup and strips
the wrapper so the macro can supply width, height and stroke from the size
tokens.

Stripping that wrapper is where it went wrong. Splitting on the first `>` looks
right and is not: the files open with an XML declaration, so the split left the
icon's own `<svg>` nested inside the macro's. The inner one kept its native 24px
and silently overflowed every button it was in, pushing the labels out of view.
The HTML contained the right text throughout; only the render showed it.

That is the third time in this project that a check passed while the screen was
visibly broken. It stays a rule: **render it and look at it.**

### 4. The size roles travelled without modification

`h-(--control-button)`, `size-(--control-checkbox)`, `size-(--control-dot)` work
in a Jinja template exactly as in JSX, because they are CSS custom properties and
nothing about them was React-shaped. Measured in the browser: button 32px,
checkbox 16px, avatar 32px, icon 16px, zero unresolved `var()` on the page.

The one adjustment is that `control.icon` is the string `"32px"`, and an SVG
`width` attribute wants `32`, so the macro strips the unit. A typed output would
not need that; it is the cost of tokens being strings.

### 5. Tailwind needs pointing at the templates

`@source "../../templates"` in `input.css`. Tailwind v4 scans for class names by
file extension and a Python project has none it recognises. Without it the
stylesheet builds clean and empty.

## Verified

Both themes rendered at 1440px and looked at, and **every text-bearing element
on the page** measured for contrast — not a sample. All clear WCAG AA in both
themes. The same audit on the React version needs a hand-picked selector list;
here the page is static, so the whole DOM can be walked.
