# Breadcrumb

The trail to the current page. Ancestors are muted; only the current page is full contrast.

## Anatomy

| Part | Token |
|---|---|
| Gap between items | `space-10` |
| Ancestor link | type style `text` in `muted-foreground` |
| Current page | type style `text` in `foreground` |
| Separator | 14×14 chevron-right in `muted-foreground` |
| Collapsed-levels button | 28×28, `radius-pill`, transparent, 16×16 ellipsis icon |

## The separator is 14px, not 16px

Every other icon in the system is 16px. The breadcrumb separator is **14px** —
deliberately smaller, so it recedes behind the labels rather than competing with
them. Keep it; a 16px chevron here makes the trail look like a row of buttons.

## Only the last item is foreground

Ancestors sit at `muted-foreground`, the current page at `foreground`. That
single contrast step is what makes the trail readable at a glance. Do not bold
the current page as well — weight and colour both shifting is heavier than this
system wants.

The current page is not a link. Mark it `aria-current="page"` and render it as a
`<span>`, not an `<a>`.

## Collapsing

When the trail is too long, the reference replaces the middle with a 28px
ellipsis button — the same geometry as CloseButton but transparent, since it
sits inline rather than on a surface. Keep the first and last items either side
of it.

Collapse by level count, not by pixel width: first, ellipsis, last is the
pattern, regardless of how much room there is.

## Guidelines

Wrap rather than truncate — the container sets `flex-wrap: wrap`. A truncated
breadcrumb loses exactly the information it exists to carry.

Breadcrumbs reflect hierarchy, not history. If the path shows where the user has
been rather than where the page sits, it is a back button.

Do not use a breadcrumb with fewer than three levels; two levels is a back link.

## Not yet tokenised

Separator size (14), ellipsis button (28), icon size (16).
