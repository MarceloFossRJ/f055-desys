# Alert

A message that needs attention. In this system that is a **row**, not a tinted banner.

## Read this before using it

**Derived — and deliberately not the usual component.** The reference contains
no alert banner: no tinted backgrounds, no coloured left rails, no red or amber
fills behind text. I checked. What it has instead is the "Danger Zone" row,
which is an ordinary ListGroup row with a warning icon, and the "Observability
Plus" card, which carries a plain `secondary` Badge reading *Warning*.

That absence is consistent, not an oversight. The system has one rule — **red
means action or data, never decoration** — and a tinted red or amber banner is
decorative red. Importing a Bootstrap-style alert would break the one thing that
makes this palette work.

So this spec gives you the system's own idiom, with severity carried by an
icon, a badge, or an action — not by a fill.

## Anatomy

Identical to a ListGroup row, which is the point.

| Part | Token |
|---|---|
| Fill | `muted-subtle` |
| Shape | `radius-pill` |
| Padding | `space-14` block, `space-16` inline |
| Gap | `space-14` |
| Icon | 16×16, top-aligned with a 2px nudge |
| Title | type style `label` |
| Description | type style `text` in `muted-foreground` |
| Trailing slot | Badge, chevron, or a 28px `secondary` Button |

## How severity is carried

| Severity | Treatment |
|---|---|
| Informational | `foreground` icon, no trailing marker |
| Warning | `foreground` icon plus a `secondary` Badge naming it |
| Destructive | `destructive` icon only — the fill stays `muted-subtle` |
| Success | a tick icon in `foreground` |

**The icon is the only thing that ever takes `destructive`.** Not the fill, not
the border, not the title. A 16px red icon is enough to find in a list of grey
rows, and it costs none of the system's signal.

There is no success green. The palette has one hue; a tick in `foreground`
carries it.

## If you need something louder

An alert that must stop someone is not a row — it is a dialog, and the action
inside it is a `destructive` Button. That is where this system puts emphasis:
on the control you press, not the container.

## Guidelines

Alerts stack with `space-8`, like ListGroup rows. More than two or three at once
and none of them get read.

A trailing Button is `secondary`, not `primary` — the alert is not the main
action on the page.

Use `role="status"` for informational alerts and `role="alert"` only for ones
that genuinely interrupt; `role="alert"` interrupts a screen reader mid-sentence.

Do not auto-dismiss anything carrying a warning or a destructive consequence.

## Not yet tokenised

The 2px icon nudge.
