# Menu

A list of actions in a floating panel. It reuses the Popover shell exactly; what
is specific to Menu is the item vocabulary and the keyboard contract.

## Shell — identical to Popover

| Part | Token |
|---|---|
| Surface | `popover` / `popover-foreground` |
| Radius | `radius-14` |
| Shadow | `shadow-overlay` |
| Padding | `space-4` |
| Offset from trigger | `space-6` |
| Min width | 224px |

Never give a menu card geometry (`radius-24`, `shadow-card`). A floating panel
is `popover` + `radius-14` + `shadow-overlay`, always.

## Items

| Part | Token |
|---|---|
| Height | 32px minimum |
| Padding | `space-6` / `space-8` |
| Radius | `radius-6` |
| Text | 14 / 20 |
| Gap | `space-8` |
| Icon | 16px, `currentColor` |
| Hover / active | `accent` fill, `radius-6` |
| Disabled | 50% opacity, no hover |

The item radius is `radius-6` against the panel's `radius-14` — small enough
that a highlighted row reads as inside the panel rather than as a second panel.

### Item types

| Type | Role | Notes |
|---|---|---|
| Action | `menuitem` | Icon optional, but all-or-nothing per group |
| Shortcut | `menuitem` + `kbd` | `kbd` in `font-mono` 12px, `muted-foreground`, pushed right |
| Submenu | `menuitem` `aria-haspopup="menu"` | 14px chevron right, `muted-foreground` |
| Checkbox | `menuitemcheckbox` `aria-checked` | A 16px check in the icon slot; **the slot stays reserved when unchecked** |
| Radio | `menuitemradio` `aria-checked` | Same, with a dot |
| Label | `presentation` | 12 / 16 / 500 in `muted-foreground` |
| Separator | `separator` | 1px `border`, `space-4` above and below |
| Destructive | `menuitem` | Text in `destructive`; **hover keeps `accent`**, not a red fill |

The reserved icon slot matters: letting unchecked rows close up makes the whole
list shift when a box is toggled.

## Destructive items

Text in `destructive`, hover in `accent` like every other row. A red fill on
hover would be indistinguishable from a primary action, since the brand is red —
see `tokens/color.json` on the open `destructive` decision.

**Put destructive items last, after a separator.** With only hue to carry the
distinction, position does real work.

## Keyboard

The whole point of a menu. Without this it is a styled list.

| Key | Behaviour |
|---|---|
| `Enter` / `Space` / `↓` on trigger | Open, focus first item |
| `↑` on trigger | Open, focus last item |
| `↓` / `↑` | Move, wrapping at both ends |
| `Home` / `End` | First / last item |
| a–z | Jump to the next item starting with that letter |
| `→` | Open a submenu, focus its first item |
| `←` | Close a submenu, return focus to its parent item |
| `Esc` | Close everything, focus the trigger |
| `Tab` | Close and move on in the page |

Focus moves **within** the menu with arrows; `Tab` leaves it. Skip disabled
items when moving. The trigger carries `aria-haspopup="menu"` and
`aria-expanded`.

## Hover, highlight and focus are one state

`.it.on` and `:hover` paint the same `accent` fill, and the focused item should
too. A menu with separate hover and focus highlights shows two active rows at
once, which reads as a bug. There is no visible focus ring inside a menu — the
`accent` fill *is* the focus indicator, which is why it must follow keyboard
focus and not only the pointer.

## Width

`min-width: 224px`, growing to fit the longest row. Do not cap it and truncate —
a menu item you cannot read is not an actionable item. If labels are long
enough to need truncation, they are descriptions and belong in a Dialog.

## Not yet tokenised

Min width (224) and the `z-index` of 50.
