# Slider

A 4px track with a 16px thumb that floats on `raised`.

## Anatomy

| Part | Token |
|---|---|
| Track height | 4px |
| Track fill (empty) | `track` |
| Track shape | `radius-pill` |
| Filled portion | `primary` |
| Thumb | 16×16, `background`, `radius-pill`, `shadow-raised` |
| Label | type style `label` |
| Value | type style `title` with tabular numerals |
| Min/max captions | `caption` in `muted-foreground`, tabular |
| Row gap | `space-8` |

## `track`, not `border` or `muted`

The empty half of the track uses its own colour — `#E5E5E5E6` light,
`#FFFFFF22` dark. That is a third alpha ramp, distinct from `border` (10% in
dark) and `input` (15%). It is also what an unchecked checkbox and radio use, so
`track` means "the off state of a control" generally, not just a slider groove.

## The thumb is the only `raised` element in the reference

`shadow-raised` exists for exactly this: something that floats just off the
surface it controls. A ring plus a 4px drop reads as grabbable in a way the
card shadow does not. Do not substitute `shadow-card`.

The thumb fill is `background`, not `card` — it reads as a cut-out of the page
rather than a small panel. On a card this is still correct: the contrast against
the track is what does the work.

## Focus

The thumb already carries a shadow, so the focus ring **stacks** rather than
replaces:

```css
box-shadow: var(--shadow-raised), 0 0 0 2px var(--ring-offset), 0 0 0 4px var(--ring);
```

Replacing the shadow on focus makes the thumb visibly flatten at the moment it
gains focus, which reads as a bug.

## Guidelines

Show the current value — as `title` above the track in the reference, which is
the pattern to follow. A slider without a readout forces the user to guess.

Min and max captions go below in `caption`, left and right. Use tabular numerals
on every number here so the value does not jitter as it changes.

16px is below any touch minimum. Give the thumb an invisible larger hit area
rather than enlarging it.

## Not in the reference

Range sliders (two thumbs), steps or tick marks, vertical orientation, and a
disabled state. All would need a decision.

## Not yet tokenised

Nothing — `--control-track` and `--control-slider-thumb`.
