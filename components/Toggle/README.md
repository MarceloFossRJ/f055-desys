# Toggle

Switch, checkbox and radio — the three binary controls, and the only place the system uses three different radii side by side.

## The three shapes

| Control | Size | Shape | On state |
|---|---|---|---|
| Switch | 32×20 | `radius-pill` track, 2px border | track `primary`, thumb slides right |
| Checkbox | 16×16 | `radius-sm` (5px) | fill `primary`, tick in `primary-foreground` |
| Radio | 16×16 | `radius-full` | fill `primary`, 8px dot in `primary-foreground` |

The checkbox is the **only square-ish thing in the entire system.** Everything
else is a pill or a circle. That is deliberate in the reference and worth
keeping — it is what distinguishes a checkbox from a radio at a glance, which
matters more than internal consistency here.

## Tokens

| Part | Token |
|---|---|
| Off track / border | `muted` (switch), `border` (checkbox, radio) |
| On fill | `primary` |
| Mark (tick, dot) | `primary-foreground` |
| Switch thumb | `background` with `shadow-thumb` |
| Label | type style `label` |
| Gap to label | `space-12` |
| Focus | `ring` + `ring-offset` |

`shadow-thumb` is the card drops with no ring — a hairline would read as a seam
against the coloured track.

## Guidelines

A switch takes effect immediately; a checkbox is staged until the form is
submitted. If your control needs a Save button next to it, it is a checkbox.

All three are below the 24px touch minimum. Make the **label** part of the
target rather than enlarging the control — that is how the reference lays out
its settings rows, with the whole row clickable.

Radio groups need a group label and at least two options. A single radio should
be a checkbox or a switch.

## Not yet tokenised

Every size here: 32×20, 16×16, the 8px dot, the 14px tick, and the switch's 2px
border. This component needs more hard-coded geometry than any other, which is
the strongest argument for a `size` token family if a second implementation
lands.
