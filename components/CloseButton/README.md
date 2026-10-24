# CloseButton

A 28px circle in `muted` with a 16px cross. The system's only icon-only action.

## Anatomy

| Part | Token |
|---|---|
| Size | 28×28 |
| Shape | `radius-pill` — a circle at this size |
| Fill | `muted` |
| Icon | 16×16 cross in `foreground`, 2px stroke |
| Border | 1px transparent, so focus does not shift layout |
| Focus | `ring` + `ring-offset` |

## It is filled, not a ghost

The reference gives the close button a `muted` fill rather than leaving it
transparent. That matters: at 28px with a thin cross, a ghost button in a busy
card header is easy to miss. Keep the fill on `card` and `background`.

The exception is a surface that is already filled — a `muted` tile, a coloured
banner — where the fill would disappear. There, drop to transparent.

## Placement in a card header

The header is a two-column grid: `1fr auto`, two rows. The close button occupies
column 2 spanning both rows, `justify-self: end`, `align-self: start`. That
keeps it pinned to the top-right whether the header has a subtitle or not, and
it never shifts when the title wraps.

```css
grid-column: 2; grid-row: 1 / span 2; justify-self: end; align-self: start;
```

## Guidelines

Always give it an accessible name — `aria-label="Close"` — because the cross
carries no text. The icon itself is `aria-hidden`.

Close dismisses without saving. If the action discards work the user would
expect to keep, it is not a close button; use a labelled Cancel in the footer.

Never pair a close button with a Cancel button that does the same thing.

28px is below the 44px touch target most guidance asks for. Extend the hit area
with padding or a pseudo-element rather than growing the circle.

## Not yet tokenised

Nothing — `--control-icon-button` and `--control-icon`.
