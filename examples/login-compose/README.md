# Login — Compose Multiplatform

The same login screen as the three HTML implementations, for KMP.

```sh
./gradlew :composeApp:desktopTest   # compile, lay out, assert, render PNGs
./gradlew :composeApp:run           # the screen in a window
```

Renders land in `composeApp/build/reports/f055/`.

## What is proven, and where

This was the one stack where the system was unproven. It is not any more — but
the proof does not happen in the sandbox this repo is developed in, and that is
worth being precise about rather than papering over.

| Check | Runs in the sandbox | Runs in CI | What it establishes |
|---|---|---|---|
| `scripts/check_kotlin_tokens.py` | yes | yes | every `F055…` name this source uses exists in `dist/kotlin` |
| `scripts/check_native_values.py` | yes | yes | the numbers in `dist/kotlin` and `dist/swift` match the flat token file |
| `:composeApp:desktopTest` | **no** | **yes** | the generated Kotlin compiles; the screen lays out; its geometry equals the tokens; it renders |

The sandbox cannot run the third because Maven Central, JetBrains Space and the
JetBrains CDN are all refused at its egress proxy — a 403 on CONNECT, logged by
the proxy itself, not a guess. GitHub Actions has no such restriction, so the
job runs there on every push and uploads both renders as artifacts.

## The test asserts against tokens, not numbers

```kotlin
assertDp(F055Control.button, submit.height, "submit button height")
```

Not `32.dp`. A literal would still pass after someone changed the token and
forgot this screen, which is the entire failure this is meant to catch. The
same test checks that `panelTitle` still carries negative tracking, since that
style exists precisely because it was hard-coded in six places first.

It also compiles `dist/kotlin/*.kt` as part of the module — `kotlin.srcDir`
points at the generated directory rather than copying it — so a generator that
emits Kotlin which does not compile fails here and nowhere else.

## What it still does not prove

The render is checked for being non-empty, not for being correct. Nothing
compares those PNGs to the HTML screens pixel by pixel, and nothing measures
their contrast the way `check_contrast.py` measures the other three. Colour and
radius are asserted statically, through the token values, rather than by
sampling the rendered image.

Android is not a build target here. Adding `androidTarget()` is two lines, but
it requires the Android SDK, which would mean installing it on every CI run.
The source is unchanged either way.

## Where it differs from the web, and why

Platform differences, not system differences:

| | Web | Compose |
|---|---|---|
| Focus ring | `ring` + `ring-offset`, drawn by the system | mapped onto Compose's focus indication and `TextField` indicator colours |
| Elevation | a hairline ring inside the shadow | `shadow()` plus `border()` — Compose has no ring, and a border affects layout where a ring does not |
| Links | `<a>` with `text-decoration` | `TextDecoration.Underline` plus an explicit `Role.Button`, because there is no anchor element |
| Tracking | `letter-spacing` in px | `letterSpacing` in sp, so it scales with the reader's font setting — closer to right on a phone, and a real difference from CSS |

`F055Elevation` documents the elevation trade-off at its own definition, so the
choice here is one the token file already made.

What travelled unchanged: `F055Control.button` is the same 32 the web calls
`h-(--control-button)`, `F055Radius.pill` the same 18, `type.panelTitle` the
same 18/28/500, and `colors.destructiveText` the same split between a
destructive fill and destructive ink.

There is no Google mark on the Google button, for the same reason as on the web:
drawing someone else's logo is not ours to do.

## What building this exposed

`panelTitle` did not exist. The centred-panel title — 18/28 weight 500 at
−0.45px — had been hard-coded in Dialog, Drawer, Toast, Placeholder and both
HTML logins, six places, while `title` (same size, weight 600, no tracking) sat
beside it in the token file and its usage note described the variant in prose.

Writing it a seventh time, in a stack with no CSS class to fall back on, is what
made that untenable. The generator had no `letterSpacing` support at all, so
naming the style meant adding tracking to all six outputs — including a
`…Tracking` constant for SwiftUI, where tracking is a view modifier rather than
part of a `Font`.
