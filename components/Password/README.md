# Password

An Input with a masked value, and room for an action beside the label.

## Anatomy

| Part | Token |
|---|---|
| Field | Input, unchanged: `input`, `radius-pill`, 32px, `space-10` lead |
| Masking | `-webkit-text-security: disc` |
| Label | type style `label`, but at `line-height: 1` |
| Label-to-field gap | `space-12` |
| Action link | 12 / 16 / 500, uppercase, **0.6px letter-spacing**, `muted-foreground` |
| Reveal toggle | 16×16, `muted-foreground`; `foreground` when revealed |

## The label row is a row, not a label

The reference pairs the label with a **Forgot?** link on the same line,
`justify-content: space-between`. That is the pattern — an action that belongs
to the field sits beside its label, not under the field where it would compete
with help text.

Two details from the reference worth keeping: the label drops to
`line-height: 1` so it aligns optically with the smaller link, and the gap to
the field is `space-12` rather than the `space-6` an ordinary Input uses,
because the row is taller.

## The action link adds letter-spacing

`Forgot?` is the `eyebrow` style **plus 0.6px of letter-spacing** — the only
place in the reference that adds tracking. At 12px uppercase in a tight row it
stops the word reading as a solid block. If you add more label-row actions, keep
the tracking consistent with this one.

## The reveal toggle is derived

The reference masks the value and offers no way to unmask it. The toggle here
follows the system's rules — 16px icon in `muted-foreground`, `foreground` when
active, sitting in the Input's trailing slot — but it is an addition.

It is a real `<button>` with `aria-pressed` and a label that states what
pressing it will do. Revealing is not a focus change: keep the caret where it
was.

## Guidelines

Never mask a value the person is being asked to confirm by typing twice. Either
offer reveal, or drop the confirm field — masking both is how typos survive.

Do not block paste. Password managers paste.

For a new password, pair with PasswordStrength. For an existing one, do not —
telling someone their current password is weak at the sign-in screen is noise
they cannot act on.

## Not yet tokenised

Field height (32), toggle size (16), the 0.6px tracking.
