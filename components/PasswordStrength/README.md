# PasswordStrength

Four segments and a word. The word does the work.

## Provenance

**Derived.** The reference has no strength meter. More importantly, it has no
palette for one — which is the whole design problem here.

## The problem: there is no green

A conventional strength meter runs red → amber → green. This system has **one
hue**. There is no success colour, no warning colour, and `primary` red means
action or data — so a green-to-red ramp cannot be built without inventing two
hues the system does not have.

Nor can the chart ramp stand in: it runs light red to dark red, which would
make a strong password *more* red than a weak one, in a system where red is the
alert colour.

## The answer: count and a word, with one exception

| Strength | Segments | Segment colour | Label |
|---|---|---|---|
| Weak | 1 | `destructive` | `destructive` |
| Fair | 2 | `foreground` | `foreground` |
| Good | 3 | `foreground` | `foreground` |
| Strong | 4 | `foreground` | `foreground` |

**How many segments are filled carries the meaning; the word states it.** Only
the weak state takes `destructive`, because a weak password is a real problem —
the same rule Alert uses, where `destructive` marks genuine trouble and nothing
else.

Unfilled segments are `track` — the same token as a slider's empty groove, which
is exactly what they are.

## The label is required, not optional

Remove the word and this meter is unreadable: four identical grey bars with some
filled tells a colourblind user, or anyone glancing, nothing at all. Since the
system cannot carry strength in hue, the text is the primary channel and the
bar is the secondary one.

That is the right order anyway. "Fair — add a number or symbol" is actionable;
an amber bar is not.

## Anatomy

| Part | Token |
|---|---|
| Segment | 4px tall, `radius-pill`, `flex: 1` |
| Segment gap | `space-4` |
| Empty segment | `track` |
| Filled segment | `foreground`, or `destructive` at weak |
| Label | `badge` style (12 / 16 / 500) |
| Hint | `caption` in `muted-foreground` |
| Gap | `space-6` |

Segment height matches Slider's track at 4px, deliberately — both are thin
horizontal indicators and should read as the same family.

## Guidelines

Four segments. Fewer cannot express a middle; more implies a precision no
strength estimator has.

Score with a real estimator (zxcvbn or similar), not a regex checking for a
capital and a digit. A rule-based meter rates `Passw0rd!` strong and
`correct horse battery staple` weak, which is backwards.

Show it only while setting a password, never at sign-in.

Never block submission on it. It is advice.

## Not yet tokenised

Segment count (4). The segment height is `--control-track`.
