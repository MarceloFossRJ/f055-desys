# Toast

A transient message that does not block the page. **Derived** — the reference
draws no toast.

## Anatomy

| Part | Token |
|---|---|
| Surface | `popover` / `popover-foreground` |
| Radius | `radius-14` |
| Shadow | `shadow-overlay` |
| Padding | `space-12`, `space-14` on the icon side |
| Max width | 384px |
| Gap between toasts | `space-8` |
| Region inset | `space-16` from the bottom-right |
| Title | 14 / 20 / 500 |
| Message | 14 / 20 in `muted-foreground` |
| Icon | 16px, `muted-foreground` |
| Action | 24px Button, 12 / 16 |
| Dismiss | 20px, 14px glyph, `radius-5` |

Same shell as Popover and Menu: a small floating panel, so `radius-14` and
`shadow-overlay`.

## There is no status palette

The system has no success green and no amber — see `CLAUDE.md`. A toast
therefore cannot carry meaning in its fill, and must not invent one.

| Kind | Treatment |
|---|---|
| Success | Default surface, check icon in `muted-foreground` |
| Info | Default surface, icon optional |
| Error | Default surface **plus a 1px inset `destructive` ring** |

The error ring is `box-shadow: var(--shadow-overlay), inset 0 0 0 1px var(--destructive)`.
Same pattern Validation uses: a ring, not a tint. One hue means errors get the
single accent available, and a successful save gets none — which is right, since
success needs no emphasis.

Because colour carries almost nothing here, **the title does the work.**
"Release submitted", not "Success". "Upload failed — the master exceeds the
2 GB limit", not "Error".

## Placement and stacking

Bottom-right, `space-16` from both edges, `space-8` between toasts, newest at
the bottom (nearest the corner). Cap the stack at three visible; queue the rest.

Below ~640px, go full-width at the bottom with `space-12` insets.

Bottom-right keeps toasts clear of the top-of-page NavBar and of a Dialog's
centred panel.

## Timing

| Content | Duration |
|---|---|
| Confirmation, no action | 4s |
| With an action ("Undo") | 8s |
| Error | **No auto-dismiss** |

Pause the timer on hover and on focus within the toast, and restart it on
leave. A toast that disappears while being read is worse than none.

An error that vanishes on its own takes the only record of the failure with it.

## Announcement

`role="status"` (polite) for confirmations, `role="alert"` (assertive) for
errors. The region is a `role="region"` with `aria-label="Notifications"`.

Every toast carries a dismiss button, including the auto-dismissing ones — a
screen-reader or keyboard user has no hover to pause with.

`Esc` dismisses the focused toast. Do not trap focus; a toast is not modal.

## Guidelines

**Never put something a person must act on in a toast.** It disappears. If a
response is required, use a Dialog; if the state matters, show it in the page.

One toast per event. A loop that fires five toasts should fire one that says
"5 tracks uploaded".

Do not toast the obvious. A filter applied and visibly reflected in the list
needs no announcement.

## Not yet tokenised

Max width (384), durations (4s, 8s), the three-toast cap, and the 640px
breakpoint.
