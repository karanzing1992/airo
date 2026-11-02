# MAID Yard Manager — Complete Product / Engineering Scope v1.0
Date: 2026-11-02. Owner repository: karanzing1992/airo. Planned public entry point: Cloudflare Access protected (not publicly executable).
Upstream source: Mobile-Artificial-Intelligence/maid at pinned commit `60206bd164bbe271e74543cc616de5f2278da511`; MIT LICENSE and notices must survive import. Do not overwrite existing tracked files until baseline is captured. Application renamed with distinct package ID, icons, app signing keys.

## Mission
One independent AI manager to operate Dell Dev Tool Yard and Mac MAD Yard from Android MAID, Android mobile browsers and desktop web. Model-agnostic, multimodal, project-aware, modular and safely autonomous. ChatGPT neither required nor a privileged runtime dependency. Source code and CI in GitHub; cloud coordination on free-tier Cloudflare as feasible. No recurring paid service without owner's separate approval.

## Product principles (non-negotiable)
- Feature-complete parity for MANAGER FUNCTIONS on Android app, mobile web, desktop web: chat, voice conversation, image attachment and review, file handling, integrations catalog, workflows, host status, tasks, agent traces, search/memory, model routing, approvals, notifications, connection administration, RAG, project dashboards, settings and audit history. Native-only abilities (offline on-phone GGUF, microphone/background notifications where supported, biometrics, device storage) have clearly marked browser equivalents or graceful unsupported states; do not falsely claim hardware-parity.
- Existing MAID local llama.cpp GGUF, downloads, inference, model parameter controls, history import/export and provider plugins must remain functional; use original source/README/license. Preserve existing accessible UI, add manager mode.
- Secure by default: Internet-exposed control plane does NOT grant direct root, arbitrary shell, or broad machine credentials. Device agents connect outward using scoped authorization; no inbound open SSH. Every action recorded, with explicit owner approval gates for privileged/destructive changes, no machine enrollment by model.
- Every adapter separate; no vendor or model hardcoding. Read-only discover first; tools labeled by scopes and permission classification. No stealth remote control or privileged bypass.
- Evidence first. UI status and release badges must derive from verified API/CI receipts. Pass/fail/unknown distinct. No fabricated tests, timings, uptime or deployment URLs.
- Open source first, free or existing free-tier resources. Enforce usage caps and quotas, thermal admission and budget circuit breakers.

## Architecture and modules
1. `apps/android`: MAID React Native/Expo with client adapters to MAID local/provider chat and manager API. Migrate/retain upstream directory structure carefully.
2. `apps/web`: responsive React/Expo Web or lightweight React/Next alternative after compatibility spike. Desktop 3-pane ops console, mobile adaptive shell/PWA; same backend contracts and feature registry. Native inference not assumed in web.
3. `services/control-plane`: Cloudflare Worker TypeScript API, Zero Trust/identity, SSE or WebSocket, tenant scoped rules, frontend static serving, small request orchestration. Worker free CPU 10ms/request; do not run Python LangGraph or heavy workloads in Worker.
4. `services/graph`: LangGraph.js state machines for manager/planning/execution approvals, checkpoints persisted via adapter to D1/DO; observable tool stages; one graph per task or conversation; bounded resumable turns. Distinguish provider request waiting from CPU.
5. `services/yard-agent`: versioned independent per-machine Linux agent, outbound mTLS or scoped signed requests, job polling/stream, host capabilities, per-lane serialized workers and recovery lane; machine-local SQLite journal, per-command timeout/resource/thermal governance; support working if controller reconnects.
6. `packages/protocol`: typed versioned schemas for message, conversation, task, event, capability, artifact, tool call, approval, host, health, identity, receipts, error envelope. Generate web and RN clients from one contract.
7. `packages/model-router`: virtual model `auto`, capability/complexity classifier, deterministic policies, quota and cost-aware selection, fallback, health load balancing, overrides and dry-run explainability. Groq, Gemini, OpenAI-compatible, Ollama/llama.cpp, LiteLLM (external only), Workers AI adapters. Validate against available quotas; no promise of unlimited free inference.
8. `packages/integrations`: dynamic MCP/HTTP/OpenAPI/CLI adapters and manifest registry, OAuth where applicable, secret vault, scope diff, disable/revoke, approvals, audit, per-provider capability discovery, metadata versioning; separate UI declarations for common display on web/android.
9. `services/memory`: D1 canonical metadata and checkpoints; R2 attachments; optional private per-project RAG with pluggable embeddings, retrieval provenance, ACL, retention and consent.
10. `packages/security`: owner/role grants, host-bound signed challenges, token rotation, replay rejection, audit receipt/HMAC signing, policy DSL and privileged-action approval service.
11. `packages/ui-contracts`: shared navigation roles, reusable task/tool result render specs, notifications, accessibility, localization, theme and activity monitor.
12. `infra/cloudflare`: Workers, D1, DO, R2, Access, optional Tunnel (restricted), IaC, isolated environments, minimal permissions, secrets only in platform vault.
13. `docs/release`: runbooks, credential bootstrap (never store credentials), QA receipts, provenance, rollbacks, user manual.

## Product surfaces / functions
**Home:** unified MAID assistant + project selector, current active tasks, approvals badge, Dell & Mac online/offline, routing health.
**Chat:** streaming multimodal responses, stop/regenerate, system prompt personas, sessions/history, export/import, search, markdown/code and references, message-level model/provider/tracing.
**Voice:** tap-to-talk and optional session voice, STT, TTS, input/output selection, interrupt, transcript and accessibility captions. Permission denial and offline modes handled.
**Vision:** image/camera/screenshot attachment, visual model selection, file permissions, safe handling of PII.
**File work:** upload/download, types PDF/text/image/audio (others behind converters), per-conversation references, document analysis, artifacts preview and integrity hashes, retention/deletion.
**Tasks:** active/queued/blocked/review/done/failed/cancelled, multi-host subtasks, dependencies, timeouts, replay and resumed status, owner approvals, evidence and provenance; prevent completion claims on mere HTTP 200.
**Host operations:** read-only inventory/health/resource thermal, processes/services, safe command/diagnostic preview, guarded write/task controls, remote browser automation with automatic termination, logs and screenshot previews with access boundaries.
**Integrations:** browse/add/test/disable/revoke connectors, dynamic MCP tools, capability scopes, approvals, health, rate budget, audit; integration updates ship without Android redeploy where protocol compatible.
**Models:** local MAID picker + `Auto` mode, routing reason, provider fallback, capability/vision/audio requirement; no GPU scaling claims from model routing. Host admission separately.
**Projects:** separate Dell and Mac subprojects, game engine, CRM, WP Manager, Moksha etc, isolated memory and permissions. No implicit ingestion of private user data.
**Notifications:** browser/PWA and Android push if service supported, in-app alerts, email/Telegram through plugins with explicit consent. No unattended cloud delivery promise until provisioned.
**Admin:** audit trail, human role/host access, active sessions/devices, secrets metadata only, revocation, retention, export, circuit breakers and emergency STOP.

## Operational execution policies
- Independent agent identities per host; Dell and Mac can each operate when the other is offline. Cloud control can queue task requests even if both offline.
- Idempotency key = tenant+task+step+attempt; terminal receipts signed by host; no blind retries for side-effectful commands; negative reads do not certify success.
- Root/privileged access only through explicit owner-approved guarded workflow with host-local authorization; least-privilege default.
- Thermal limits, memory pressure, CPU cap, browser auto-close, idle shutdown; desktop/remote preview is a time-limited capability.
- Host agent connection is different from the current ChatGPT-specific SSH tunnel. Install dedicated MAID identity; do not reuse existing opaque credentials or presume connector tokens accessible.
- Remote endpoint public URL protected by identity and policy, not openly callable. CORS, CSRF, upload size, SSRF, injection, secret exfil and open redirect protections tested.
- Break-glass stop/revoke controls must not depend on the LLM.

## Compatibility / availability policy
All common manager features appear on mobile app and responsive web; no hidden integrations on a single surface. Common integration manifests drive both. Android local GGUF runs on-device. Web shows the same models as remotely selectable; offline browser inference is optional R&D and not a release blocker. Desktop browser remote screen access must be owner-authorized and limited.

## Milestone deliverables
M0 upstream import, license check, baseline Android CI, tests and App version.
M1 shared protocol, identity, Cloudflare API, durable messages and streaming.
M2 secure yard agents on Dell and Mac with host receipts, task execution, health, recovery.
M3 model router with actual fallback, capability select, quotas/telemetry.
M4 full parity web + Android manager UI, project/task dashboards, approvals and integrations catalog.
M5 voice, vision, file workflows, memory/RAG, notifications and audit.
M6 zero-trust security, independent QA, E2E host/mobile/browser testing, signed APK and web release, release ledger and rollback.

## Done criteria
- Owner installs separately named signed ARM64 and universal MAID Yard Manager APKs with checksum and correct minimum SDK; handles clean install and upgrade.
- Publicly accessible but identity-protected HTTPS mobile + desktop web works from outside LAN without ChatGPT.
- Authenticated user can chat, search, upload, invoke vision/voice and access all manager functions, connector management and task audit on both surfaces.
- Independent Dell+Mac heartbeat, scoped command, queued job completion, cancel, approval denial, replay and outage recovery tests pass.
- `auto` routes text/code/vision by actual capability, falls back by health, enforces quota and reports selected route.
- Upstream local GGUF and standard remote provider features remain operational on Android.
- Signed release artifacts and SBOM, SHA256, provenance, install evidence, smoke test reports, security pass, rollback documentation published.
- No production credentials in repo/APK/logs; no unresolved P0/P1 security blockers. Operator can revoke agent access without relying on AI.
