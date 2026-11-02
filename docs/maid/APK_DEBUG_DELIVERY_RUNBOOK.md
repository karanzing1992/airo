# MAID M0 Android Debug APK — Source-bound delivery
Date 2026-11-02. Repository karanzing1992/airo.
Pipeline: .github/workflows/maid-android-debug-apk.yml

## Stages
- Pull request containing imported MAID upstream source and reviewed Qwen/Groq React lint repair; run full frozen dependency installation, non-suppressed Expo lint, complete Jest, deterministic Android prebuild + Gradle assembleDebug.
- Fail closed on any lint, test or native build error; no upload after failure.
- Upload a development APK + SHA256SUMS + RECEIPT.json tied to exact GitHub source SHA and workflow run.
- Manual release approval, genuine security certification, host control, Android keystore and production signing are **not** included. An upstream M0 debug APK is not a completed MAID Yard Manager application.
- This is free GitHub Actions hosted infrastructure subject to project limits. No Groq tokens needed for APK compilation; Groq Qwen 3.8 27B is the development source-coding model.
- APK is retrievable from the verified Actions artifact link, subject to GitHub Actions artifact retention and repository permissions.
- No GitHub Release tag, Play Store publication or external deployment is performed.
