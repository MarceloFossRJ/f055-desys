# Toolbar

A row of 32px icon buttons, each outlined by a hairline ring and filled by nothing.

## Anatomy

| Part | Token |
|---|---|
| Button size | 32×32 |
| Shape | `radius-8` |
| Outline | `shadow-hairline` |
| Fill | transparent |
| Icon | 16×16 in `foreground` |
| Gap between buttons | `space-16` |
| Divider | 1px × 20px in `border` |

## This is where two unused tokens earn their place

`radius-8` and `shadow-hairline` were both defined and referenced by nothing
until this component. They belong together: a hairline ring with no drop and no
fill is exactly what an icon button in a toolbar needs, and 8px is the shape
that goes with it.

**The ring is a shadow, not a border.** That is what keeps the button exactly
32×32 — a 1px border would make it 34, or shrink the icon box if you set
`box-sizing`. Everything in this system that looks like a thin outline is drawn
this way.

## Why not pills

Every other control in F055 is a pill. The toolbar is the exception, and
deliberately so: a row of eight circles reads as a strip of dots, while squarer
buttons at `radius-8` read as a set of tools. The reference does this.

The two other icon-only controls — CloseButton and the Breadcrumb ellipsis —
*are* pills, because they sit alone rather than in a row.

| Icon button | Shape | Fill |
|---|---|---|
| Toolbar | `radius-8` | transparent + `shadow-hairline` |
| CloseButton | `radius-pill` | `muted` |
| Breadcrumb overflow | `radius-pill` | transparent |

## Focus

The ring stacks onto the hairline rather than replacing it, as Slider's does:

```css
box-shadow: var(--shadow-hairline), 0 0 0 2px var(--ring-offset), 0 0 0 4px var(--ring);
```

## Guidelines

Every button needs an `aria-label` — nothing here carries text.

Group related tools and separate groups with a 1px divider rather than extra
space. The reference lays its toolbar out on an 8-column grid, which is a
showcase arrangement rather than a rule; in a real toolbar use a flex row.

A toolbar is for actions on the current view. If the buttons navigate
elsewhere, it is a NavBar.

## Not yet tokenised

Nothing — every dimension is a `--control-*` token.
