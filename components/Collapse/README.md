# Collapse

One disclosure, standing alone. No fill, no dividers, no siblings.

## Provenance

**Derived.** The reference has an Accordion but no single collapse. This is that
component with everything that implies a *set* removed, so the two read as
relatives rather than duplicates.

## Anatomy

| Part | Token |
|---|---|
| Trigger | 32px pill, `space-10` inline, `width: fit-content` |
| Trigger fill | transparent |
| Trigger label | type style `button` |
| Chevron | 16×16 in `muted-foreground`, **leading**, rotated −90° when closed |
| Gap to label | `space-6` |
| Panel | `space-10` inline padding, aligning with the trigger label |
| Gap to panel | `space-12` |

## Three differences from Accordion, all deliberate

| | Accordion | Collapse |
|---|---|---|
| Fill | `muted-subtle` | none |
| Chevron | trailing, pushed right | leading, beside the label |
| Width | full | `fit-content` |

An accordion item is a **row** — full width, filled, with the chevron at the far
end. A collapse is a **control** — it sits inline, sized to its label, with the
chevron leading like a disclosure triangle.

Making a single collapse full-width and filled makes it look like an accordion
missing its siblings.

## The panel aligns to the label, not the trigger edge

Panel content takes the same `space-10` inline padding as the trigger, so the
revealed content lines up with the trigger's text. Aligning to the trigger's
outer edge leaves the content hanging 10px to the left of everything above it.

## Guidelines

Use for optional detail: advanced settings, a long field set, extra rows.

Do not hide anything required behind a collapse. If a form cannot be submitted
without a field, that field is not optional detail.

The trigger is a `<button>` with `aria-expanded` and `aria-controls`. Label it
with what will appear — "Show 4 more fields" beats "More".

Give it no animation. The reference defines no motion, and a height transition
on arbitrary content is the kind of thing that needs a real decision rather than
a default.

## Not yet tokenised

Trigger height (32), chevron size (16).
