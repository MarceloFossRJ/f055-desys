# OTPInput

One box per digit, in the mono face.

## Provenance

**Derived.** The reference has no one-time-code field. The box borrows Input's
fill and the figures use the system's mono face, both extracted; the geometry is
new.

## Anatomy

| Part | Token |
|---|---|
| Box | 40 × 48, `input` fill, `radius-14` |
| Box gap | `space-8` |
| Group separator | an extra `space-8` |
| Digit | `numeric` style scaled to 18px, tabular |
| Empty digit | `muted-foreground` |
| Filled digit | `foreground` |
| Current box | `ring` + `ring-offset` |
| Error | 1px `destructive` ring, as Validation |

## `radius-14`, not `radius-pill`

A 40 × 48 box at `radius-pill` is close to a stadium and reads as a text field
rather than a slot. `radius-14` is the system's rounded-square — the same value
40px icon tiles and overlays use — and it is what makes these read as discrete
cells.

This is the second place where `pill` is wrong by default; DatePicker's day
cells are the other.

## Mono, and taller than it is wide

Digits are the mono face at 18px with tabular figures, so every character
occupies the same box and nothing shifts as the code is typed.

The box is **48px tall against 40px wide** — portrait, not square. A square box
with a single character in it reads as a checkbox; the taller proportion reads
as a slot waiting for one character.

## It is one field, not six

Six boxes, one value. That has consequences:

- Paste fills every box from one paste. People paste codes from messages; a
  field that only accepts the first character is broken.
- Backspace in an empty box moves to the previous one and clears it.
- The error state marks **every** box, not the last. The code is wrong, not the
  final digit.
- One `aria-label` for the group, and one error message with
  `aria-describedby`. Six separately-labelled inputs make a screen reader
  announce six fields for one value.

## The group separator

Six digits split 3 + 3 with an extra `space-8` between the groups. Codes are
read aloud and remembered in chunks; an unbroken run of six is measurably harder
to transcribe.

Four-digit codes are not split.

## Guidelines

Use `inputmode="numeric"` and `autocomplete="one-time-code"` — the second is
what lets a phone offer the code from the message.

Submit automatically when the last box fills, and say so. Do not also leave a
Verify button that does nothing.

Never mask the digits. The person is copying them from somewhere else.

## Not yet tokenised

Box width (48), digit size (18), group split (3 + 3). The box height is
`--control-tile`.
