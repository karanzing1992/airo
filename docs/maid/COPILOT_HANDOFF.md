# Assignment / Copilot handoff
This repository `karanzing1992/airo` was empty and is now designated an isolated staging workspace for the MAID Manager. Do not change any unrelated repository.
Canonical source docs: PRODUCT_SCOPE_V1, WEB_MOBILE_PARITY, INTEGRATIONS_AND_MODELS, CERTIFICATION_AND_AUTONOMY.
Default branch: master; upstream MAID pinned SHA 60206bd164bbe271e74543cc616de5f2278da511.
First Copilot task: import upstream MAID as a reviewable PR without history rewrites and produce an Android baseline test/build receipt. Keep original license and UI features; do not make manager claims yet.
Second: implement shared protocols/identity/Cloudflare staging; only after first PR verified.
Use .github/agents/maid-builder.agent.md and .github/copilot-instructions.md. Code agent eligibility and assignment must be verified; an open issue without actual bot assignee is merely queued for owner action.
Delivery: signed distinct APK, universal and ARM64, downloadable GitHub Releases, plus authenticated web app. This is gated on real CI, device and production security evidence.
