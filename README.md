# AIRO / MAID Yard Manager

Development workspace for an independent, multimodal AI manager spanning Android MAID, mobile and desktop web, and secure Dell/Mac yard agents.

Status: development specification and autonomous delivery setup. No production functionality is claimed until the release gates in `docs/maid/` pass.

Upstream: https://github.com/Mobile-Artificial-Intelligence/maid (MIT license). The upstream code must be imported with the LICENSE and attribution intact, on a reviewable branch, before any derivative APK release.

`main` is for reviewed releases; Copilot changes arrive by pull requests and CI evidence. Architecture: LangGraph.js + Cloudflare Workers/D1/Durable Objects/R2; cross-platform clients; independent authenticated per-host agents; pluggable model router and integrations.
