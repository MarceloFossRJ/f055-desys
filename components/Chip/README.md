# Chip

A 20px `secondary` pill carrying a value. Four variants: plain, with icon, with avatar, removable.

## Why one component and not three

This spec covers "chip", "chip with icon" and "chip with avatar" together,
because they are one component with a leading slot — same height, same shape,
same fill, same type. Splitting them into three specs would mean three places to
keep the height in step, and four stacks implementing near-duplicates.

If a variant needed different geometry it would deserve its own spec. None does.

## Anatomy

| Part | Token |
|---|---|
| Height | 20px (28px when beside 28px controls) |
| Shape | `radius-pill` |
| Fill | `secondary` / `secondary-foreground` |
| Selected fill | `primary` / `primary-foreground` |
| Label | type style `badge` (14 / 20 at 28px) |
| Inline padding | `space-8` (`space-10` at 28px) |
| Gap between parts | `space-4` |
| Leading icon | 12×12 in `currentColor` |
| Leading avatar | 16×16 circle (24px at 28px chip) |
| Remove button | 12×12 cross |

## Chip versus Badge

They look identical and are not the same thing.

- **Badge** is a label. It has no hover, no focus and no click target. A status,
  a count, a category.
- **Chip** is a value the person put there, or can act on. It is selectable,
  removable, or both.

If nothing happens when you click it, it is a Badge. The reference's MultiSelect
chips are Chips; its "Pending" and "ETF" markers are Badges.

## The avatar variant drops the left padding

An avatar fills the chip's full inner height and sits flush to the leading edge,
so the chip's left padding drops to 2px. Keeping `space-8` there leaves the
circle floating in the middle of a gap.

The avatar is `muted`, not `secondary` — it must read as distinct from the chip
body it sits inside.

## Selection is `primary`, unlike everywhere else

A selected chip is the one place a `primary` fill marks state rather than an
action. That is consistent, not an exception: a selected chip **is** a chosen
value — data — which is exactly what red means here. The same reasoning makes
Calendar's selected day red, and keeps Pagination's current page `muted`.

Only use it where chips are genuinely a selection control. A row of
`primary` chips as decoration spends the system's one signal.

## Removable chips

The remove control is 12px inside a 20px chip — far below any touch target. On
touch, drop it and remove from the source control instead, as MultiSelect's
README says.

It is a real `<button>` with its own `aria-label` naming the value, not a
decorative cross. The chip itself stays non-interactive unless it is selectable.

## Not yet tokenised

Both heights (20, 28), icon size (12), avatar sizes (16, 24), remove size (12),
and the 2px flush-left inset.
