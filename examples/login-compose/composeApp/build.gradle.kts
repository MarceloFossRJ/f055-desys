import org.jetbrains.compose.desktop.application.dsl.TargetFormat

plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.composeMultiplatform)
    alias(libs.plugins.composeCompiler)
}

kotlin {
    // Desktop (JVM) is what CI builds, because it is the only target that
    // renders headlessly without a device or a simulator. iOS and web are
    // declared because the source is the same; Android needs the SDK, which
    // would make every CI run install it -- add androidTarget() when you have
    // one locally.
    jvm("desktop")
    iosArm64()
    iosSimulatorArm64()
    js(IR) { browser() }

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
