# Login — Compose Multiplatform

The same login screen as the three HTML implementations, for KMP: Android, iOS
and web from one source.

## This one is not verified, and you should treat it differently

There is no Kotlin toolchain in this repo's sandbox — no `kotlinc`, no Gradle,
and no network for Gradle to fetch anything with. **This screen has never been
compiled or run.** The other three implementations were built, rendered at
1440px, looked at, and measured against WCAG AA; this one was not.

That is an honest gap, not a formality. A screenshot is missing from this README
for the same reason.

What *is* checked, on every build, is the part a design system is responsible
for. `scripts/check_kotlin_tokens.py` verifies that every `F055Radius.x`,
`F055Control.x`, `colors.x` and `type.x` in this source exists in `dist/kotlin`:

```
Kotlin tokens: 55 references across 1 source file(s).
Every F055 token referenced from Kotlin exists in dist/kotlin.
```

It catches a token renamed in `tokens/` and not followed through here, or one
written from memory that never existed — which is the failure this repo keeps
finding. It does not catch a Compose mistake, a type error, or a screen that
does not lay out. **Do not read a pass as "it works."**

## Running it

Drop `LoginScreen.kt` into a Compose Multiplatform project that has
`dist/kotlin/` on its source path, wrap it in the generated theme, and give it
real font files — `FontFamily.Default` is a visible downgrade, which
`F055Colors.kt` says in its own doc comment:

```kotlin
F055Theme(dark = isSystemInDarkTheme(), sans = robotoFamily, mono = geistMonoFamily) {
    LoginScreen(onSubmit = { email, password -> viewModel.signIn(email, password) })
}
```

## Where it differs from the web, and why

Platform differences, not system differences:

| | Web | Compose |
|---|---|---|
| Focus ring | `ring` + `ring-offset`, drawn by the system | mapped onto Compose's own focus indication and `TextField` indicator colours |
| Elevation | a hairline ring inside the shadow | `shadow()` plus `border()`, because Compose has no ring — and a border affects layout where a ring does not |
| Underlined links | `<a>` with `text-decoration` | `TextDecoration.Underline` on the style |

`F055Elevation` documents the elevation trade-off at its definition, so the
choice here is the one the token file already made.

The things that did travel unchanged: `F055Control.button` is the same 32dp the
web calls `h-(--control-button)`, `F055Radius.pill` the same 18, `type.panelTitle`
the same 18/28/500 at −0.45dp tracking, and `colors.destructiveText` the same
split between a destructive fill and destructive ink.

## What building this exposed

`panelTitle` did not exist when this screen was started. The centred-panel title
— 18/28 weight 500 at −0.45px — had been hard-coded in Dialog, Drawer, Toast,
Placeholder and both HTML logins, six places, while `title` (the same size at
weight 600, no tracking) sat in the token file next to it. Its usage note even
described the variant in prose: *"Drop to weight 500 with letterSpacing −0.45px
for centred empty-state titles."*

Writing it a seventh time, in a stack that cannot fall back on a CSS class, was
what made that untenable. The generator had no `letterSpacing` support at all,
so adding the style meant adding tracking to all six outputs: `letter-spacing`
in CSS, a field on the Python dataclass and the Ruby struct, `letterSpacing` on
the Compose `TextStyle`, and a `…Tracking` constant for SwiftUI, where tracking
is a view modifier rather than part of a `Font`.

There is no Google mark on the Google button, for the same reason as on the web.
