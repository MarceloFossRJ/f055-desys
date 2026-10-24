# Popover

Anything that floats above the page. One shell, three densities.

## Provenance

**Composed.** The shell is extracted — the reference's chart tooltip establishes
`popover` + `radius-14` + `shadow-overlay`, and Select's panel already uses it.
What is new here is naming it as its own component and setting the padding for
interactive content.

## The shell

Every floating surface in this system is the same three tokens:

| Part | Token |
|---|---|
| Fill | `popover` / `popover-foreground` |
| Shape | `radius-14` |
| Elevation | `shadow-overlay` |

**Never `radius-24` with `shadow-card`.** A card is a surface *on* the page; a
popover floats *above* it. Card geometry on a small floating panel makes it look
like a card that lost its place.

## Three densities, one shell

| Use | Padding | Gap |
|---|---|---|
| Tooltip | `space-6` block, `space-10` inline | `space-8` |
| Menu / listbox | `space-6` | `space-2` |
| Popover with content | `space-16` | `space-12` |

A tooltip is read, not operated: small, tight, no interactive children. A menu is
a list of 32px pill rows — identical to Select's panel, because it is the same
thing. A content popover has a title, body and footer, and is padded like a
small card.

## No arrow

The reference's tooltip has no pointer, tail or arrow, and neither does this.
Position alone carries the association. An arrow would need its own border and
shadow to match the shell, which is a lot of machinery for a decoration this
system never uses.

## Close affordance

A content popover carries a CloseButton; a menu and a tooltip do not. A menu
closes on selection or on dismiss, and a tooltip is not focusable at all.

## Guidelines

A tooltip must never contain something you can click. If it does, it is a
popover, and it needs to be reachable by keyboard.

Destructive menu items take `destructive` on the **label only** — no fill. Same
rule as Alert: the fill stays neutral, the colour goes on the smallest element
that carries the meaning.

Return focus to the trigger on close, and close on Escape.

Keep the width under about 320px. Beyond that it is a dialog.

## The tooltip swatch

`series-1`, at `--size-4` wide and full height. It identifies a data series, so
it takes a categorical token, not a step of the sequential `chart-*` ramp. It
used to be `chart-1`; when that ramp became theme-aware on 2026-10-24 — the
dark ramp is the light one reversed — `chart-1` became the step *nearest* the
dark surface, and the swatch would have dropped to 2.15:1. `series-1` clears
3:1 in both themes because that is what it is for.

## Not yet tokenised

Nothing. Close button and footer button height are now `--control-icon-button`
and `--control-button-sm`.
