# Tabs

A pill thumb moving inside a pill track. There is no underline tab style in this system.

## Two forms

**Tabs** — a `muted` track at `radius-pill` with `space-4` padding, holding
28px pill buttons. The active tab lifts onto `card` with `shadow-thumb`;
inactive tabs are transparent with `muted-foreground` text. Use for switching
between views of the same thing.

**Segmented filters** — separate outlined pills with `space-8` between them, the
active one filled `primary`. Use for filtering a list, where more than one state
could plausibly be "on" conceptually even if only one is selected at a time.

The difference matters: a track implies the options are exclusive views; loose
pills imply they are filters over one view.

## Tokens

| Part | Token |
|---|---|
| Track | `muted`, `radius-pill`, `space-4` padding |
| Gap between tabs | `space-4` (track) / `space-8` (segmented) |
| Tab height | 28px |
| Tab padding | `space-12` |
| Label | type style `button` |
| Active tab (track) | `card` + `shadow-thumb` |
| Active pill (segmented) | `primary` + `primary-foreground` |
| Inactive text | `muted-foreground` |
| Focus | `ring` + `ring-offset` |

The active tab uses `shadow-thumb` rather than `shadow-card` for the same reason
a switch knob does: it sits on a filled track, where a hairline ring would read
as a seam.

## Guidelines

Three to five tabs. Beyond that use a select or a sidebar — the track does not
scroll, and shrinking labels to fit defeats the point.

Inactive tabs sit at `muted-foreground`, which is 4.74:1 in light mode. Do not
lighten them further to emphasise the active tab; reduce the active tab's
contrast instead, or accept the difference the lift already provides.

Never mix the two forms in one view.

## Not yet tokenised

Nothing — the tab height is `--control-button-sm`.
