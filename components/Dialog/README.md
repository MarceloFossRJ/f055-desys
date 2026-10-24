# Dialog

A modal panel over a scrim. **Derived** — the reference has an "Alert Dialog"
button but never draws the dialog, and a page-wide search for a scrim fill
returned nothing. Every value here is a decision.

## Anatomy

| Part | Token |
|---|---|
| Scrim | `foreground` at 50% opacity, full viewport |
| Surface | `popover` / `popover-foreground` |
| Radius | `radius-24` |
| Shadow | `shadow-overlay` |
| Padding | `space-24` |
| Max width | 384px (prompt) / 512px (form) |
| Gap | `space-8` |
| Title | 18 / 28 / 500, tracking −0.45px |
| Body | 14 / 22.75 (`prose`) in `muted-foreground` |
| Actions | right-aligned, `space-8` apart, `space-8` above |
| Close | 24px CloseButton, `space-12` inset |

## Radius follows size, shadow follows floating

A Dialog takes `radius-24` — card geometry — while Menu, Popover and Toast take
`radius-14`. That is not inconsistent; it is the rule the reference implies:

> **Radius follows size. Shadow follows whether it floats.**

A 384px panel at `radius-14` looks under-rounded next to the cards behind it; a
200px menu at `radius-24` looks like a card that lost its page. Both take
`shadow-overlay`, because both float.

## The scrim

`background: var(--foreground); opacity: .5` on a full-bleed element — a token
plus an opacity, not a new colour. It inverts with the theme for free: near-black
over light, near-white over dark.

That dark-mode behaviour is deliberate. A dark scrim over a dark page is
invisible, so the layering stops reading. A light scrim dims the page the way a
dark one does in light mode.

Clicking the scrim closes the dialog **unless there is unsaved input**, where it
should do nothing — a stray click should not discard typing.

## Modal means modal

- `role="dialog"` with `aria-modal="true"`
- `aria-labelledby` → the title, `aria-describedby` → the body
- Focus moves into the dialog on open — to the first field, or to the safest
  action when there is no field. **Never auto-focus a destructive button.**
- Focus is trapped while open: `Tab` cycles within.
- `Esc` closes, except with unsaved input.
- Focus returns to the trigger on close.
- Everything behind it gets `aria-hidden` or `inert`; the body gets
  `overflow: hidden`.

A dialog that does not trap focus is a floating div — a keyboard user tabs
straight out and onto the page they cannot see.

## Actions

Right-aligned, confirming action last. Cancel is an outline Button; the confirm
is `primary`, or `destructive` when it destroys something.

**Both reading as red is a known weakness.** The destructive and primary reds
sit one step apart, which is why the title must state the consequence —
"Delete this workspace?", not "Are you sure?" — and the button must name the
act — "Delete workspace", not "OK". The words carry what the colour cannot.

See `tokens/color.json`: a non-red destructive is the real fix.

## Which overlay

| Need | Use |
|---|---|
| A choice that must be made before continuing | Dialog |
| A confirmation of something destructive | Dialog |
| A short form, 1–4 fields | Dialog |
| A long form, or a flow with steps | Drawer, or a page |
| Secondary information, dismissible | Popover |
| Actions on a thing | Menu |
| Something happened, no response needed | Toast |

If the person can usefully ignore it, it is not a dialog.

Never stack dialogs. A dialog that opens a dialog is a flow that wants a Drawer.

## Not yet tokenised

Max widths (384, 512), the 50% scrim opacity, the close button inset.
