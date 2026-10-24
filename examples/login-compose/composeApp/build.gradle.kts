import org.jetbrains.compose.desktop.application.dsl.TargetFormat

plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.composeMultiplatform)
    alias(libs.plugins.composeCompiler)
}

kotlin {
    // Desktop (JVM) only, deliberately.
    //
    // This module exists to VERIFY the design system, and desktop is the only
    // target that compiles and renders headlessly on a Linux CI runner with no
    // device, simulator or SDK. Apple targets cannot build off a Mac at all,
    // and declaring them makes Gradle fetch the Kotlin/Native toolchain on a
    // host that can never use it.
    //
    // The source is plain Compose Multiplatform and is not desktop-specific.
    // To ship it, add the targets where you build:
    //
    //     androidTarget()                       // needs the Android SDK
    //     iosArm64(); iosSimulatorArm64()       // needs a Mac
    //     js(IR) { browser() }
    //
    jvm("desktop")

    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation(compose.runtime)
                implementation(compose.foundation)
                implementation(compose.material3)
                implementation(compose.ui)
            }
            // The generated tokens, compiled in place. Not copied, not vendored:
            // if the generator emits something that does not compile, this build
            // is what says so.
            kotlin.srcDir("../../../dist/kotlin")
        }
        val desktopMain by getting {
            dependencies { implementation(compose.desktop.currentOs) }
        }
        val desktopTest by getting {
            dependencies {
                implementation(kotlin("test"))
                @OptIn(org.jetbrains.compose.ExperimentalComposeLibrary::class)
                implementation(compose.uiTest)
                implementation(compose.desktop.currentOs)
            }
        }
    }
}

compose.desktop {
    application {
        mainClass = "design.f055.login.MainKt"
        nativeDistributions { targetFormats(TargetFormat.Dmg, TargetFormat.Deb) }
    }
}

tasks.withType<Test>().configureEach {
    // Skia renders in software; no display is needed, but AWT still wants to
    // be told that.
    systemProperty("java.awt.headless", "true")
    testLogging { showStandardStreams = true }
}
