# Input

A pill-shaped text field with no shadow and no visible border — the fill alone separates it from the surface.

## Anatomy

| Part | Token |
|---|---|
| Fill | `input` |
| Border | 1px transparent (present so focus does not shift layout) |
| Shape | `radius-pill` |
| Height | 32px single-line, 64px minimum for a textarea |
| Padding | `space-10` leading, `space-8` trailing; textarea `space-8` / `space-10` |
| Text | type style `text` (14 / 20 / 400) |
| Placeholder | `muted-foreground` |
| Label | type style `label` |
| Help text | type style `caption` in `muted-foreground` |
| Elevation | `none` — inputs sit flush, deliberately |
| Focus | `ring` + `ring-offset` |

## The fill is translucent

`input` is `border-200` at 50% in light and white at 15% in dark — a wash, not a
solid. That is intentional: the same token composites correctly on `background`
and on `card`, which is where most forms actually live. Do not substitute a
solid colour; it will look wrong on one of the two surfaces.

A consequence worth knowing: against `card` the fill sits at only 1.12:1. The
field is legible because of its shape and its content, not its contrast. If you
need a field to read as strongly bounded, add a `border` hairline — but do it
consistently across the whole form, never on one field.

## Focus

Apply the ring to the **wrapper**, via `:focus-within`, and remove the inner
`outline` on the control itself. Same two-shadow pattern as Button.

## Guidelines

Always pair with a `<label>`; placeholder text is not a label, and it disappears
exactly when the user needs it. Help text goes below the field in `caption` /
`muted-foreground`.

For an error state there is no dedicated token. Use `destructive` on the ring
and the help text — and note that `destructive` only reaches AA-large, so keep
error text at 14px or above.

## Not yet tokenised

Heights (32 / 64), border width, and the icon size.
