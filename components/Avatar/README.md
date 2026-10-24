# Avatar

A circle with a hairline ring. In a stack the hairline becomes a 2px ring in the page colour.

## Anatomy

| Part | Token |
|---|---|
| Shape | `radius-full` |
| Size | 40px measured; 24 and 32 derived from the system's control heights |
| Fallback fill | `muted` |
| Fallback text/icon | `muted-foreground` |
| Initials | `badge` style (12 / 16 / 500); 14 / 20 at 40px |
| Ring, standalone | `shadow-hairline` |
| Ring, in a stack | 2px `ring-offset` |
| Stack overlap | −8px |

## The ring changes job between contexts

Standalone, an avatar carries `shadow-hairline` — a 1px `border` ring that keeps
a light photo from bleeding into a light surface.

In a **stack**, that ring is replaced by a **2px ring in `ring-offset`** — the
page colour. This is the same idea as the focus ring's offset: a band of
background that separates one circle from the one behind it. A hairline is too
thin to do that job at an 8px overlap.

`ring-offset` tracks `background`, so the stack works on a page. On a `card`,
override it to `card` — the ring must match whatever is actually behind the
stack, or it reads as a grey halo.

## Fallbacks, in order

Image → monogram → icon. Never an empty circle: a bare `muted` disc reads as a
loading state that never finished.

Monograms are one or two letters at weight 500 in `muted-foreground`, not a
colour generated from the name. This system has one hue and spends it on action
and data; tinting avatars by user id would spend it on decoration.

## Overflow

A stack ends with a `secondary` circle carrying `+N` — not `muted`, so it reads
as a control rather than another person. It is the same treatment as a Chip,
which is what it behaves like.

Show at most five faces before collapsing.

## Sizes

Only **40px** is measured from the reference. 24 and 32 match the system's
control heights and are there so an avatar can sit inside a 32px row or a Chip,
but they are conventions rather than extractions.

## Guidelines

Images are `background-size: cover` and centred; anything else distorts faces.

An avatar is not a button. If it opens a menu, wrap it — do not add a focus ring
to the circle itself, since the ring and the stack ring would collide.

Give every avatar real alternative text, or `aria-hidden` if the name is already
beside it.

## Not yet tokenised

The −8px overlap and the 2px stack ring.
