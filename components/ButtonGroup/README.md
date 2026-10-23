# ButtonGroup

Buttons joined into one control: outer corners rounded, inner corners square, one shared hairline between segments.

## Anatomy

| Part | Token |
|---|---|
| Segment height | 32px |
| Segment padding | `space-12` (icon-only: 32px square, no padding) |
| Fill | `card` |
| Border | 1px `border` |
| Outer corners | `radius-pill` |
| Inner corners | 0 |
| Label | type style `button` |
| Icon | 16×16 |
| Selected segment | `secondary` / `secondary-foreground` |

## The two rules that make it look right

**Only the ends are rounded.** First segment takes left radii, last takes right,
everything between stays square. A group where every segment is a pill is not a
group — it is a row of buttons, which is a different thing and should use
`space-8` between them instead.

**Drop the left border on every segment after the first.** Otherwise adjacent
segments each draw a hairline and you get a visible 2px seam. The reference does
this: its trailing icon segment carries top, right and bottom borders only.

```css
.seg + .seg { border-left: 0; }
```

## Group versus segmented tabs

ButtonGroup is for **actions** that belong together — Export plus a menu, or a
split button. Tabs' segmented form is for **filtering a view**. They look
similar and mean different things: a group's segments each do something; a
segmented filter's options select among states.

If your segments are mutually exclusive view states, use Tabs.

## Focus

A focused segment's ring would be clipped by its neighbours, so raise it:

```css
.seg:focus-visible { z-index: 1; box-shadow: 0 0 0 2px var(--ring-offset), 0 0 0 4px var(--ring); }
```

Without `z-index` the ring disappears under the adjacent segment's background.

## Guidelines

Two to four segments. Beyond that the shared hairlines stop reading as one
control.

Mixing a labelled segment with a trailing icon segment is the reference's own
pattern, and the icon segment is square at the group's height — 32×32 — not a
padded button.

## Not yet tokenised

Segment height (32), icon size (16), border width (1).
