# Range

A Slider with two thumbs and a filled segment between them.

## Provenance

**Derived.** The reference has a single-thumb Slider and no range control. Every
value here is Slider's; what is new is the second thumb and the bounded fill.

## Anatomy

Identical to Slider except where noted.

| Part | Token |
|---|---|
| Track | 4px, `track`, `radius-pill` |
| Filled segment | `primary`, bounded **both** sides |
| Thumbs | 16×16, `background`, `radius-pill`, `shadow-raised` |
| Value readout | type style `title`, tabular |
| Min/max captions | `caption` in `muted-foreground`, tabular |

## The one structural difference

Slider's fill runs from 0 to the value. Range's fill is bounded at both ends:

```css
.fill { position: absolute; left: <lower>%; right: <100 − upper>%; }
```

Everything else — track height, thumb size, elevation, focus stacking — is
Slider's, unchanged. If you are implementing both, build Range and let Slider
be the case where the lower bound is pinned to 0.

## Thumbs that meet

Two 16px thumbs at the same value overlap completely, and the one on top wins
every drag — so the range can get stuck. Three rules:

1. The **focused** thumb takes the highest `z-index`, so the thumb being driven
   by the keyboard is always on top.
2. Otherwise the **upper** thumb sits above the lower one.
3. A thumb may not cross its partner. Clamp at equality rather than swapping
   roles mid-drag; swapping means the thumb under the cursor suddenly moves the
   other end.

## The readout shows both bounds

`$2,500 – $7,500`, in the `title` style with tabular numerals, as Slider shows
its single value. An en dash with hair spaces, not a hyphen.

Without a readout a range is close to unusable — two thumbs on a bare track
give no way to know what either one is.

## Guidelines

Each thumb needs its own accessible name — "Minimum", "Maximum" — and its own
`aria-valuenow`. A single slider role cannot express two values.

Both thumbs are below any touch target. Give each an invisible larger hit area,
and make sure the two areas do not overlap at the clamp point.

For a date range, use two DatePickers rather than this. A 4px track cannot
express months.

## Not yet tokenised

Track height (4), thumb size (16).
