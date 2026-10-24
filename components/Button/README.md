# Button

Five variants across three heights, all fully rounded.

## Anatomy

A pill-shaped box with centred content, optionally an icon before the label.

| Part | Token |
|---|---|
| Shape | `radius-pill` |
| Horizontal padding | `space-12`, at every height |
| Icon-to-label gap | `space-6` at 32px, `space-4` at 28px and 20px |
| Label | type style `button` (14 / 20 / 500) |
| Icon | 16×16, `stroke: currentColor`, 2px |
| Focus | `ring` + `ring-offset` |

## Variants

| Variant | Background | Foreground | Border |
|---|---|---|---|
| `primary` | `primary` | `primary-foreground` | transparent |
| `secondary` | `secondary` | `secondary-foreground` | transparent |
| `outline` | `background` | `foreground` | `border` |
| `ghost` | transparent | `foreground` | transparent |
| `destructive` | `destructive` | `destructive-foreground` | transparent |

**One `primary` per view.** If two buttons on screen are both primary red,
neither reads as the main action.

`destructive` is currently very close to `primary` — the brand is red, so the
two read similarly. This is a known open decision; until it is resolved, lean on
the label ("Delete", not "Confirm") to carry the warning rather than the colour.

## Heights

32px is the default. 28px is for buttons sitting inside a card footer or beside
a row of content. 20px is effectively a badge with a click target — use it
sparingly, and never as the only way to reach an action, since it is below the
24px minimum most touch guidance asks for.

At all three heights `radius-pill` (18px) exceeds half the height, so the
browser clamps it and the button renders as a true pill. That is the intended
look. A square-cornered button will not read as part of this system.

## Focus

```css
box-shadow: 0 0 0 2px var(--ring-offset), 0 0 0 4px var(--ring);
```

Two shadows, not an outline: this keeps the ring outside the box model so it
never shifts layout, and the inner `ring-offset` band is what makes the ring
legible on a primary or destructive button, where ring and surface are both red.

Use `:focus-visible`, not `:focus`, so pointer users do not see rings on click.

## What the consumer provides

The icon. Nothing here ships icons — pass an inline SVG that inherits
`currentColor` at 16×16 with 2px strokes.

## Not yet tokenised

Border width (1px) and the focus geometry (2px ring, 2px offset).
Control heights are now `--control-badge`, `--control-button-sm` and
`--control-button`.
