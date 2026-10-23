# ListGroup

A stack of pill rows on a tinted fill. Each row is its own surface — there are no dividers.

## Anatomy

| Part | Token |
|---|---|
| Row fill | `muted` |
| Row shape | `radius-pill` |
| Row padding | `space-14` block, `space-16` inline |
| Gap between rows | `space-8` |
| Gap between row parts | `space-14` |
| Leading icon | 16×16 in `foreground`, top-aligned with a 2px nudge |
| Title | type style `label` |
| Description | type style `text` in `muted-foreground`, clamped to 2 lines |
| Trailing chevron | 16×16 in `muted-foreground` |
| Trailing shortcut | type style `numeric` in `muted-foreground` |

## Rows are separated by space, not by rules

This is the part that distinguishes a ListGroup from a Table. A table uses
hairline `border` rules between rows and no fill. A list group gives each row
its own `muted` pill with `space-8` between them, and no rules at all.

Use a **Table** when the rows are records to compare — columns line up, figures
align. Use a **ListGroup** when each row is a destination or an action.

Nothing here is a divided list. If you find yourself adding a `border-bottom`
between rows, you want a Table.

## The icon is top-aligned, not centred

The leading icon sits at `align-self: flex-start` with a 2px downward nudge, so
it aligns with the title's cap height rather than floating in the middle of a
two-line row. Centre-aligning it looks wrong the moment a description wraps.

## Two densities

The full row — icon, title, description, chevron — uses `space-14` vertical
padding. A compact row with a title and a trailing shortcut drops to `space-8`.
Do not mix the two densities within one group.

## Guidelines

If every row has a chevron, the group is navigation; if none do, it is
information. Mixing them within a group is ambiguous.

Descriptions clamp to two lines. A row needing three lines is a card.

The whole row is the target, not just the title — which is what makes the small
icons and chevrons acceptable here.

## Deviation from the reference

The reference fills rows with `muted` at 50% (`#F5F5F580`), and this spec uses
solid `muted`. Over `card` the difference is roughly one step of grey. It is
called out because the reference also uses partial-alpha fills for `input` and
`track`, which *are* tokenised — a `muted` variant at 50% may deserve a token of
its own if this pattern recurs.

## Not yet tokenised

Icon size (16), the 2px icon nudge, the two row densities.
