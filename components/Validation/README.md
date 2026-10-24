# Validation

Field-level error and success states. An icon and a sentence; the field keeps its fill.

## Provenance

**Derived.** The reference has no validation states at all — no red borders
anywhere in the file, no error text, no success marks. I checked the whole
document for a `destructive` border and found none.

So this follows the system's existing rules rather than importing a convention.

## The field keeps its fill

An invalid field gets a **1px `destructive` ring** and nothing else. The `input`
fill stays exactly as it is.

Tinting the field red would be decorative red, which is the one thing this
palette forbids — the same reasoning that keeps Alert from being a tinted
banner. A hairline ring is enough to find a field in a form, and it composites
over `card` and `background` identically because it is a shadow, not a border.

## Error text is 14px, never smaller

`destructive` reaches **4.36:1 in light and 3.48:1 in dark** — AA-large only.
That is fine at 14px, and not fine below it.

So error messages use the `text` style at 14px, not `caption` at 12px, even
though ordinary help text is 12px. If an error must be smaller, drop the colour
and rely on the icon and the wording.

## Colour is never the only channel

Every error carries a 16px icon beside the text. Every success carries a tick.
Someone who cannot distinguish the red still sees a marker and reads the
sentence.

That is also why the icon sits in the **message**, not inside the field. An icon
in the field's trailing slot competes with Select's chevron and Password's
reveal toggle, and it is the message that has to be read.

## There is no success green

A verified field gets a `border` ring — the same hairline an ordinary bounded
element uses — and a tick in `foreground`. The system has one hue and spends it
on action, data and genuine problems. "This is fine" does not need a colour.

## Anatomy

| State | Field | Message |
|---|---|---|
| Default | `input`, no ring | `caption` in `muted-foreground`, 12px |
| Error | `input` + 1px `destructive` ring | 14px `destructive` + alert icon |
| Success | `input` + 1px `border` ring | 14px `foreground` + tick icon |

Focus stacks in front of the error ring rather than replacing it, so a focused
invalid field shows both:

```css
box-shadow: 0 0 0 1px var(--destructive), 0 0 0 2px var(--ring-offset), 0 0 0 4px var(--ring);
```

## Guidelines

Validate on blur, not on keystroke. Marking a field invalid while someone is
still typing the valid value is the most common way to make a form feel hostile.

Say what to do, not what is wrong. "Enter a full email address, including the
domain" beats "Invalid email".

Wire the message to the field with `aria-describedby`, and set `aria-invalid` on
the field itself.

One message per field. If a field has three problems, name the first.

## Not yet tokenised

Ring width (1px) and the 2px icon nudge.
