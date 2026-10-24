# NavBar

Brand, horizontal navigation and actions in one bar, separated from the page by a hairline.

## Provenance — read this first

**Derived, not extracted.** The reference has no horizontal navigation bar. It
had a fifth artboard ("Hello World", 1440×900) that was the likely place for
one, and that artboard was deleted from the file before I could examine it.

So every value here comes from parts that *are* extracted — Nav's item
geometry, Toolbar's icon button, Button, and the `border` hairline — assembled
by rule rather than measured. Treat it as provisional, and if the designer
produces a real navbar, that should win.

## Anatomy

| Part | Token |
|---|---|
| Bar padding | `space-12` block, `space-20` inline |
| Bottom rule | 1px `border`, drawn as an inset shadow |
| Gap between regions | `space-24` |
| Brand | type style `card-title` |
| Nav item | identical to Nav: 32px, `radius-pill`, `space-10` inline |
| Gap between items | `space-2` |
| Active item | `muted` fill, weight 500 |
| Action gap | `space-8` |
| Icon action | Toolbar's icon button — `radius-8`, `shadow-hairline` |
| Primary action | Button, 32px |

## The bar's rule is an inset shadow

```css
box-shadow: inset 0 -1px 0 0 var(--border);
```

Not `border-bottom`. Consistent with the rest of the system, where every
hairline is drawn as a shadow so it never affects layout — and here it also
means the bar's height stays exactly `space-12` × 2 + 32px.

## It reuses Nav's item, exactly

A horizontal nav item is the same 32px pill with the same `space-10` padding,
the same weight shift from 400 to 500, and the same `muted` active fill. Nothing
about the orientation changes the item.

That is deliberate: a product with a sidebar on one screen and a top bar on
another should not have two different-looking active states.

## Three regions, not a flex row of everything

Brand and actions are `flex: none`; the nav takes the remaining space. This
keeps the brand pinned left and the actions pinned right regardless of how many
nav items there are, and it is what makes the overflow behaviour in
`NavOverflow` possible.

## Guidelines

One primary action at most, at the right end. Everything else is an icon button
or a secondary.

Nav items do not wrap — they collapse. See NavOverflow.

The bar sits on `background`, not `card`. It is page chrome, not a surface on
the page.

## Not yet tokenised

Bar height (56 = 12 + 32 + 12), item height (32), icon size (16).
