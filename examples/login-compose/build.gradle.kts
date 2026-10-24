// The shape a Compose Multiplatform module needs to build this screen. Not run
// in this repo's CI: there is no Kotlin toolchain here and no network for
// Gradle. See README.md -- the screen is checked for token references only.
plugins {
    kotlin("multiplatform")
    id("org.jetbrains.compose")
    id("com.android.library")
}

kotlin {
    androidTarget()
    iosArm64(); iosSimulatorArm64()
    @OptIn(org.jetbrains.compose.ExperimentalComposeLibrary::class)
    js(IR) { browser() }

    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation(compose.runtime)
                implementation(compose.foundation)
                implementation(compose.material3)
            }
            // The generated tokens, consumed in place rather than copied.
            kotlin.srcDir("../../dist/kotlin")
        }
    }
}
