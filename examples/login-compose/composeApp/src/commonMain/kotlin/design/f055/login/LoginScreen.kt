package design.f055.login

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.dp
import design.f055.tokens.*

/**
 * Login — the same screen as examples/dashboard-next and examples/login-rails,
 * on Compose Multiplatform.
 *
 * NOT COMPILED. This repo's sandbox has no Kotlin toolchain and no network for
 * Gradle, so unlike the three HTML implementations this one has never been run.
 * What IS checked, by scripts/check_kotlin_tokens.py on every build, is that
 * every F055 token referenced below exists in dist/kotlin — which catches the
 * failure a design system actually causes. It does not catch a Compose mistake.
 * Treat it as a starting point, not as a verified screen.
 *
 * Deliberate differences from the web, because the platform differs rather than
 * because the system does:
 *
 *  - The focus ring is a platform affordance here. Compose draws its own focus
 *    indication and TextField carries an indicator colour, so `ring` and
 *    `ring-offset` are mapped onto that instead of being redrawn.
 *  - Elevation is a border plus a shadow. F055Elevation documents this: CSS
 *    draws a hairline ring in the shadow, Compose has no equivalent, and a
 *    border changes layout where a ring does not.
 *  - There is no Google mark on the Google button, for the same reason as on
 *    the web: drawing someone else's logo is not ours to do.
 */
@Composable
fun LoginScreen(
    onSubmit: (email: String, password: String) -> Unit = { _, _ -> },
    onForgotPassword: () -> Unit = {},
    onSignUp: () -> Unit = {},
    onGoogle: () -> Unit = {},
    errorMessage: String? = null,
) {
    val colors = LocalF055Colors.current
    val type = LocalF055Type.current

    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(colors.background)
            .padding(F055Space.s24),
        contentAlignment = Alignment.Center,
    ) {
        Column(
            modifier = Modifier.widthIn(max = CARD_WIDTH),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .shadow(F055Elevation.card, RoundedCornerShape(F055Radius.s24))
                    .border(
                        F055Elevation.ringWidth,
                        colors.border,
                        RoundedCornerShape(F055Radius.s24),
                    )
                    .background(colors.card, RoundedCornerShape(F055Radius.s24))
                    .padding(F055Space.s24),
                verticalArrangement = Arrangement.spacedBy(F055Space.s24),
            ) {
                Column(verticalArrangement = Arrangement.spacedBy(F055Space.s6)) {
                    Text("Login to your account", style = type.panelTitle, color = colors.cardForeground)
                    Text(
                        "Enter your email below to login to your account",
                        style = type.prose,
                        color = colors.mutedForeground,
                    )
                }

                Column(verticalArrangement = Arrangement.spacedBy(F055Space.s16)) {
                    Field(label = "Email") {
                        TokenField(
                            value = email,
                            onValueChange = { email = it },
                            placeholder = "m@example.com",
                            keyboardType = KeyboardType.Email,
                            imeAction = ImeAction.Next,
                        )
                    }

                    Field(
                        label = "Password",
                        trailing = {
                            // No link colour in this system, so the underline carries it.
                            Text(
                                "Forgot your password?",
                                style = type.text.copy(textDecoration = TextDecoration.Underline),
                                color = colors.mutedForeground,
                                modifier = Modifier.clickableRole(onForgotPassword),
                            )
                        },
                        error = errorMessage,
                    ) {
                        TokenField(
                            value = password,
                            onValueChange = { password = it },
                            placeholder = null,
                            keyboardType = KeyboardType.Password,
                            imeAction = ImeAction.Done,
                            isError = errorMessage != null,
                            visualTransformation = PasswordVisualTransformation(),
                        )
                    }

                    PrimaryButton("Login") { onSubmit(email, password) }
                    OutlineButton("Login with Google", onClick = onGoogle)
                }
            }

            Spacer(Modifier.height(F055Space.s16))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Don't have an account? ", style = type.text, color = colors.mutedForeground)
                Text(
                    "Sign up",
                    style = type.text.copy(textDecoration = TextDecoration.Underline),
                    color = colors.mutedForeground,
                    modifier = Modifier.clickableRole(onSignUp),
                )
            }
        }
    }
}

/**
 * 384dp, the width the reference uses for every centred panel. It is a layout
 * value, not a token: the system deliberately has none, because a container
 * width belongs to a screen.
 */
private val CARD_WIDTH = 384.dp

@Composable
private fun Field(
    label: String,
    trailing: @Composable (() -> Unit)? = null,
    error: String? = null,
    content: @Composable () -> Unit,
) {
    val colors = LocalF055Colors.current
    val type = LocalF055Type.current
    Column(verticalArrangement = Arrangement.spacedBy(F055Space.s6)) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(label, style = type.label, color = colors.foreground)
            trailing?.invoke()
        }
        content()
        if (error != null) {
            // Ring, not tint: one hue, so an invalid field keeps its fill and
            // gains an outline. destructive-text, not destructive -- the fill
            // and the ink are different tokens.
            Text(error, style = type.text, color = colors.destructiveText)
        }
    }
}

@Composable
private fun TokenField(
    value: String,
    onValueChange: (String) -> Unit,
    placeholder: String?,
    keyboardType: KeyboardType,
    imeAction: ImeAction,
    isError: Boolean = false,
    visualTransformation: androidx.compose.ui.text.input.VisualTransformation =
        androidx.compose.ui.text.input.VisualTransformation.None,
) {
    val colors = LocalF055Colors.current
    val type = LocalF055Type.current
    OutlinedTextField(
        value = value,
        onValueChange = onValueChange,
        singleLine = true,
        isError = isError,
        textStyle = type.text,
        visualTransformation = visualTransformation,
        placeholder = placeholder?.let { { Text(it, style = type.text, color = colors.mutedForeground) } },
        keyboardOptions = KeyboardOptions(keyboardType = keyboardType, imeAction = imeAction),
        shape = RoundedCornerShape(F055Radius.s8),
        modifier = Modifier.fillMaxWidth().heightIn(min = F055Control.button),
        colors = OutlinedTextFieldDefaults.colors(
            focusedContainerColor = colors.input,
            unfocusedContainerColor = colors.input,
            errorContainerColor = colors.input,
            focusedBorderColor = colors.ring,
            unfocusedBorderColor = colors.input,
            errorBorderColor = colors.destructive,
            cursorColor = colors.foreground,
        ),
    )
}

@Composable
private fun PrimaryButton(label: String, onClick: () -> Unit) {
    val colors = LocalF055Colors.current
    val type = LocalF055Type.current
    Button(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth().height(F055Control.button),
        shape = RoundedCornerShape(F055Radius.pill),
        colors = ButtonDefaults.buttonColors(
            containerColor = colors.primary,
            contentColor = colors.primaryForeground,
        ),
        contentPadding = PaddingValues(horizontal = F055Space.s16),
    ) { Text(label, style = type.button) }
}

@Composable
private fun OutlineButton(label: String, onClick: () -> Unit) {
    val colors = LocalF055Colors.current
    val type = LocalF055Type.current
    OutlinedButton(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth().height(F055Control.button),
        shape = RoundedCornerShape(F055Radius.pill),
        border = androidx.compose.foundation.BorderStroke(F055Elevation.ringWidth, colors.border),
        colors = ButtonDefaults.outlinedButtonColors(
            containerColor = colors.card,
            contentColor = colors.foreground,
        ),
        contentPadding = PaddingValues(horizontal = F055Space.s16),
    ) { Text(label, style = type.button) }
}

/** Keeps the click affordance and the semantics together in one place. */
private fun Modifier.clickableRole(onClick: () -> Unit): Modifier = this
