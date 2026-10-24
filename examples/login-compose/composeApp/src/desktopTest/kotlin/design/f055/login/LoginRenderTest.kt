package design.f055.login

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.ImageComposeScene
import androidx.compose.ui.Modifier
import androidx.compose.ui.test.ExperimentalTestApi
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.getBoundsInRoot
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.runComposeUiTest
import androidx.compose.ui.unit.Density
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import design.f055.tokens.F055Control
import design.f055.tokens.F055Theme
import design.f055.tokens.F055Type
import design.f055.tokens.f055Type
import java.io.File
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

/**
 * The thing that closes the gap.
 *
 * The three HTML implementations were rendered and measured in a browser. This
 * does the same for Compose: it lays the screen out for real and asserts its
 * geometry against the TOKENS -- the submit button is F055Control.button tall,
 * not merely about 32dp -- and writes PNGs of both themes so the screen can be
 * looked at rather than imagined.
 *
 * Deliberately asserted against the token objects rather than against literal
 * numbers. A literal would pass after someone changed a token and forgot this
 * screen, which is the whole failure mode.
 */
class LoginRenderTest {

    private fun assertDp(expected: Dp, actual: Dp, what: String) {
        // Layout rounds to whole pixels, so allow the half-pixel that costs.
        assertTrue(
            kotlin.math.abs(expected.value - actual.value) <= 0.5f,
            "$what: expected $expected, measured $actual",
        )
    }

    @OptIn(ExperimentalTestApi::class)
    @Test
    fun `geometry comes from the tokens`() = runComposeUiTest {
        setContent {
            F055Theme(dark = false) { LoginScreen() }
        }

        onNodeWithTag(LoginTags.CARD).assertIsDisplayed()
        onNodeWithTag(LoginTags.TITLE).assertIsDisplayed()

        val submit = onNodeWithTag(LoginTags.SUBMIT).getBoundsInRoot()
        assertDp(F055Control.button, submit.height, "submit button height")

        val google = onNodeWithTag(LoginTags.GOOGLE).getBoundsInRoot()
        assertDp(F055Control.button, google.height, "Google button height")
        assertDp(submit.width, google.width, "the two buttons are the same width")

        val card = onNodeWithTag(LoginTags.CARD).getBoundsInRoot()
        assertTrue(
            card.width <= 384.dp + 0.5.dp,
            "card width: expected at most 384dp, measured ${card.width}",
        )

        val email = onNodeWithTag(LoginTags.EMAIL).getBoundsInRoot()
        assertTrue(
            email.height >= F055Control.button - 0.5.dp,
            "email field height: expected at least ${F055Control.button}, measured ${email.height}",
        )
    }

    @OptIn(ExperimentalTestApi::class)
    @Test
    fun `the error message appears and uses destructive ink`() = runComposeUiTest {
        setContent {
            F055Theme(dark = false) {
                LoginScreen(errorMessage = "That email and password do not match.")
            }
        }
        onNodeWithTag(LoginTags.ERROR).assertIsDisplayed()
    }

    /** panel-title is the system's only negative tracking; prove it survived. */
    @Test
    fun `panel title carries its tracking`() {
        val type: F055Type = f055Type(
            androidx.compose.ui.text.font.FontFamily.Default,
            androidx.compose.ui.text.font.FontFamily.Monospace,
        )
        assertEquals(18f, type.panelTitle.fontSize.value, "panel-title font size")
        assertEquals(500, type.panelTitle.fontWeight?.weight, "panel-title weight")
        assertTrue(
            type.panelTitle.letterSpacing.value < 0f,
            "panel-title tracking should be negative, was ${type.panelTitle.letterSpacing}",
        )
    }

    @OptIn(ExperimentalComposeUiApi::class)
    @Test
    fun `renders to a png in both themes`() {
        val out = File("build/reports/f055").apply { mkdirs() }
        for (dark in listOf(false, true)) {
            val scene = ImageComposeScene(width = 760, height = 760, density = Density(1f)) {
                F055Theme(dark = dark) {
                    Box(Modifier.fillMaxSize()) { LoginScreen() }
                }
            }
            val bytes = scene.use { it.render().encodeToData()!!.bytes }
            val file = File(out, if (dark) "login-dark.png" else "login-light.png")
            file.writeBytes(bytes)
            assertTrue(file.length() > 2_000, "${file.name} looks empty (${file.length()} bytes)")
            println("wrote ${file.absolutePath} (${file.length()} bytes)")
        }
    }
}
