# Kosmos-1 Android Date Converter

An Android app that calculates the two dates accepted by the original
**Kosmos-1 Biorhythm Computer and Calculator** (23 / 28 / 33-day cycles).

The date of interest is **prepopulated with today's date** on launch; the birth
date defaults to 30 years before today. Both can be changed with date pickers.

## The math

A Kosmos-1 accepts two-digit years from 1901 to 1999. The three biorhythm cycles
share a common period of `23 × 28 × 33 = 21,252` days. The app shifts **both**
dates backward by whole periods until both fit in that range. Because both
shift equally, the elapsed interval and the weekday are preserved.

This is the algorithm of [ronibandini/Kosmos-1](https://github.com/ronibandini/Kosmos-1)
translated to Kotlin.

Example: birth 1974-06-17, interest 2026-10-08 → `04 10 16` / `08 01 68`.

## Features

- Date pickers for both dates; "Use today" shortcut
- Current date prepopulated on start
- Exact Kosmos-1 output format `MM DD YY`
- Shows interval in days, number of 21,252-day periods, and an explanation
- Input validation with readable errors
- No permissions, no network, no ads

## Build

```bash
# Android SDK 35 + build-tools 35.0.0 required
export ANDROID_HOME=/path/to/android-sdk
./gradlew assembleDebug
# APK: app/build/outputs/apk/debug/app-debug.apk
```

Or open the folder in Android Studio and run on a device/emulator (API 26+).

## Verify the converter alone

`KosmosConverter.convert()` is a pure function and can be unit-tested with
JUnit; the README example is the reference case.
