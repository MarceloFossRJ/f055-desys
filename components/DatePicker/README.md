# DatePicker

An Input trigger that opens a Calendar in an overlay panel.

## Provenance

**Composed, not derived.** Both halves are extracted — the trigger is the
reference's Input with a leading icon, and the grid is the reference's Calendar.
What is new is only the pairing: the reference shows a Calendar inline in a
card, never in a popover.

That makes this more grounded than MultiSelect or NavBar, and less than
Calendar itself.

## Anatomy

**Trigger** — Input with a leading icon rather than a trailing one:

| Part | Token |
|---|---|
| Fill | `input` |
| Shape | `radius-pill`, height 32px |
| Padding | `space-10` inline |
| Leading icon | 16×16 calendar glyph in `muted-foreground` |
| Value | type style `text`; placeholder in `muted-foreground` |
| Focus | `ring` + `ring-offset` |

**Panel** — Select's panel geometry with Calendar inside:

| Part | Token |
|---|---|
| Fill | `popover`, `radius-14`, `shadow-overlay` |
| Padding | `space-16` |
| Section gap | `space-12` |
| Day cell | `radius-full` — see below |
| Day gap | `space-4` |
| Footer buttons | 28px, right-aligned, primary last |

## The icon leads, unlike Select

Select's chevron trails, because it signals "this opens". A date picker's
calendar icon **leads**, because it says what kind of value the field holds —
the same role an icon plays in a ListGroup row.

A date field with a trailing chevron reads as a dropdown of arbitrary options
rather than a date.

## Day cells use `radius-full`, not `radius-pill`

Calendar's README flags this: at a cell narrower than about 36px, `radius-pill`
(18px) stops clamping and the selected day becomes a rounded square rather than
a circle. A picker panel is narrower than the inline calendar the reference
shows, so cells land in exactly that range.

Use `radius-full` here. It is the one deliberate difference from the Calendar
spec.

## Footer

The reference's inline calendar has no footer; a picker needs one, because the
person needs a way out that is not "pick a date".

Keep it to two: a text shortcut (Today) and the confirming action. If the picker
applies on selection, drop the footer entirely rather than leaving a dead Apply
button.

## Guidelines

Always allow typing. A calendar grid is slow for a date two years out, and a
keyboard is faster for anyone who knows the date. The trigger shown here is
display-only for clarity; in a real implementation it is a text input.

Show the full month name — "23 October 2026", not "23/10/2026". Numeric formats
are ambiguous across locales, which is exactly the mistake a date picker exists
to prevent.

For a range, see Range.

## Not yet tokenised

Nothing — every dimension is a `--control-*` token.
