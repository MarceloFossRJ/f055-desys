# Accordion

Stacked disclosure items on `muted-subtle`, divided by hairlines.

## Anatomy

| Part | Token |
|---|---|
| Item fill | `muted-subtle` |
| Divider | 1px `border`, dropped on the last item |
| Trigger padding | `space-16` all round |
| Trigger label | type style `text` at weight **500** |
| Gap to chevron | `space-24` |
| Chevron | 16×16 in `muted-foreground`; **up** when open, down when closed |
| Panel padding | `space-16` inline and bottom, none at the top |
| Panel text | type style `text` at weight 400 in `foreground` |

## The panel has no top padding

The trigger's own 16px bottom padding already separates it from the panel.
Adding padding-top as well gives 32px, which visibly detaches the answer from
its question. The reference pads the panel on three sides only.

## Chevron up means open

The reference points the chevron **up** on the open item — "press to collapse" —
rather than the rotate-from-down convention. Both are legible; this one is the
system's. Implement it as a 180° rotation of the same icon so there is one
asset.

## Panel body is `foreground`, not muted

The answer is the content, not an aside. It stays full contrast at weight 400.
Only the trigger's weight marks it as the heading.

## Accordion versus Collapse

An **Accordion** is a set. Items sit on one surface, share dividers, and
optionally close each other. A **Collapse** is a single disclosure with no
siblings, no dividers and no fill.

Use Accordion for three or more related disclosures — an FAQ, a settings group.
Use Collapse for one.

## Guidelines

Allow several items open at once unless there is a reason not to. Auto-closing
siblings is surprising when the person wanted to compare two answers.

The trigger is a `<button>` with `aria-expanded`, and the panel is referenced
with `aria-controls`. The whole trigger row is the target, not just the text.

Round the group, not the items: `radius-14` on the container with
`overflow: hidden`. Rounding each item leaves gaps in the dividers.

## Not yet tokenised

Divider width (1px).
