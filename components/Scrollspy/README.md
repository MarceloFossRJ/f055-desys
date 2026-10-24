# Scrollspy

Nav, with the active item driven by scroll position rather than by routing.

## Provenance

**Derived — and it is a behaviour, not a new look.** The reference has no
scrollspy. It also needs no new visual: the active item is Nav's `muted` pill
with its weight shift, unchanged.

This spec exists to record the behaviour and the two places it differs from Nav,
not to introduce a component.

## What is actually different from Nav

Two things, both small.

**1. Nested items are indented, not grouped.** A document outline has depth,
where a sidebar nav has groups. A second-level item takes `space-24` left
padding and drops to `muted-foreground` — it does not get its own group label.

**2. `aria-current="true"`, not `"page"`.** The person has not navigated
anywhere; they are reading a section of the page they are already on.

Everything else — item height, padding, the `muted` active fill, the 400 → 500
weight shift, the `space-2` gap — is Nav's.

## No rail

The common scrollspy treatment is a vertical line with a moving indicator. This
system has no rail idiom anywhere — it marks state with fills and weight, not
with bars beside things. Adding one here would introduce a pattern that appears
nowhere else.

The `muted` pill is enough.

## The behaviour

Use an `IntersectionObserver`, not scroll-offset arithmetic. Observe each
section with a root margin that biases toward the top of the viewport, so the
heading nearest the top wins rather than whichever section covers the most
pixels.

Three rules that make it feel right:

- **Only one item is active.** If two sections are visible, the upper one wins.
- **Clicking an item scrolls and sets the active state immediately**, then lets
  the observer take over once the scroll settles. Waiting for the observer makes
  the click feel unacknowledged.
- **The last section needs a floor.** A short final section may never reach the
  top of the viewport; when the page is scrolled to the bottom, force the last
  item active.

## Guidelines

Two levels of depth at most. Three is an outline, not a nav.

Hide it below the width where it would sit under the content. A scrollspy
stacked above an article is just a table of contents — which is fine, but then
it should not track scroll, because the person cannot see both.

Respect `prefers-reduced-motion` on the click-to-scroll: jump rather than smooth
scroll.

## Not yet tokenised

Item height (32), the `space-24` indent for nested items.
