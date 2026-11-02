# Upstream MAID source attribution
Original repository: https://github.com/Mobile-Artificial-Intelligence/maid
Pinned baseline revision: 60206bd164bbe271e74543cc616de5f2278da511
Upstream license: MIT (see LICENSE).
This derivative preserves the original authorship attribution and will use its own package identifier and signing keys for future releases.

## M0 validation trace

- Original pinned source: `60206bd164bbe271e74543cc616de5f2278da511` (MIT).
- Groq Qwen 3.8 27B selected for coding, with high reasoning and free-tier quotas.
- React Hooks lint defects fixed in source PR #28, merged into this import branch at `299b05baea47d6c7eeaa3513b68d821d2477c761`.
- Real Expo lint and Jest passed in GitHub Actions run 41423350728.
- Android debug APK build from this source must pass the independent `.github/workflows/maid-android-debug-apk.yml` workflow before release acceptance; source tests do not themselves certify a compiled APK.
- An M0 debug APK is not a certified, signed MAID Yard Manager build.
