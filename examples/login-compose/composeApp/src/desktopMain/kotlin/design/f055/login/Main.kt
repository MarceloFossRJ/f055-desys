package design.f055.login

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application
import androidx.compose.ui.window.rememberWindowState
import design.f055.tokens.F055Theme

/** `./gradlew :composeApp:run` — the screen in a window, for looking at it. */
fun main() = application {
    Window(
        onCloseRequest = ::exitApplication,
        state = rememberWindowState(width = 760.dp, height = 760.dp),
        title = "F055 — Login",
    ) {
        // Fonts are deliberately not bundled here. F055Colors.kt says in its own
        // doc comment that falling back to FontFamily.Default is a visible
        // downgrade; this window shows exactly that, which is the honest default
        // for an example that ships no font files.
        F055Theme(dark = isSystemInDarkTheme()) {
            LoginScreen()
        }
    }
}
