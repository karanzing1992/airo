# Autonomous Delivery / Independent Certification
## Driver
GitHub Copilot coding agent executes tightly scoped GitHub issues and submits PRs. The direct issue assignment requires Copilot cloud agent entitlement and appropriate GitHub API/user permissions; verify assignment and created PR. GitHub Actions runs test/lint/build and independent verification. A task is NOT done merely because Copilot posts a comment or opens a PR.
No blanket merge of security-sensitive changes; production promotion and privileged agent enrollment require owner authorization.

## Issue dependency order
I01 M0 bootstrap: import pinned upstream code and original LICENSE in new `upstream-import` branch, preserve README/package setup; create baseline build CI, record provenance.
I02 Contracts: schema and generated typed clients; cross-platform fixtures.
I03 Cloud API: identity, state, streaming, secure API tests; deploy staging via free-tier constraints.
I04 LangGraph: durable graph orchestration, task state and crash recovery.
I05 Agents: Dell/Mac outbound control channel, tasks, receipts, least privilege, negative tests.
I06 Models: policy router, auto model, provider adapters, fallback/quotas, audit.
I07 Android: MAID reuse, manager feature shell, auth, chat, projects, approvals and model info; preserve local GGUF.
I08 Web: mobile+desktop full-parity frontend, PWA, responsive QA and accessibility.
I09 Integrations: manifest registry and cross-platform catalog, test/install/revoke, OAuth.
I10 Multimodal: voice/vision/files/artifacts and browser-safe substitutes.
I11 Memory+notifications: per-project RAG, search, provenance, queued alerts, privacy.
I12 Security/QA: independent adversarial and negative tests, mobile+browser+host receipts, smoke testing.
I13 Release: deploy authenticated web, sign APK AAB, publish checksums/SBOM, rollback, user documentation.

## Autonomy design
- Issue = isolated working branch, independently reviewable PR, explicit acceptance tests and evidence.
- Do not run dependent issues until their prerequisites are merged and certified; parallelize only disjoint tasks with interface contracts.
- Automated CI on every PR; add test matrix across Android release build, web build/browser, backend tests, policy/authorization and contract suites.
- Automated PR reviewer checks with codeowner protections; on failure Copilot repairs same PR, not unverified reruns elsewhere.
- Require invariant: `source_sha == tested_sha == released_sha`. Never certify a stale unrelated SHA.
- User can invoke STOP; cancel queued tasks and remove agent credentials from central control plane.
- Agent may not invent GitHub issues marked accepted, call fake demo receipts 'live', manipulate tests, or self-approve high-risk changes.
- Lockfile pinning and provenance; CI secrets configured in GitHub Actions, never in issues/repo.
- Owner intervention limited to account authorization/Copilot entitlement, cloud credential setup, host installation consent, Android signing secrets, and approval of privileged actions and final production promotion.

## Per-gate evidence bundle
`docs/maid/receipts/GATE-N.json` includes {gate, timestamp, repo, branch, source_sha, job_urls, tests_passed, tests_failed, host_id, device, runtime, artifact_sha256, reviewer, verdict, blockers}. Unknown is NOT passed.
G0 baseline upstream commit and LICENSE, Android unit/test/build and artifact reproducibility.
G1 identity, cloud endpoint authentication, backend contract and durable session tests.
G2 Dell/Mac live health, scope, queued job, reboot/offline, idempotency and signed receipt verified.
G3 automatic model text/code/image routing, quotas, compatible fallback tests.
G4 mobile app and all web viewports feature parity (matrix), voice, document, integrations.
G5 independent security/negative/failover/retention and privacy verification.
G6 app signing, universal+ARM64 APK + AAB, web production URL, checksum, SBOM, release notes, physical Android installation, rollback readiness.

## Release/artifacts
Keep GitHub release artifact names `maid-yard-<version>-arm64.apk`, `maid-yard-<version>-universal.apk`, `maid-yard-<version>.aab`, `sha256sums.txt`, `sbom.json`, `release-ledger.json`.
The upstream build workflow depends on original signing keys. For derivative app create distinct signing key stored only in GitHub environment secrets and package identifier; do not reuse upstream package/signing identity or pretend upstream APK is custom.
Do not publish or deploy with G5 fail. All versions must preserve upstream MIT license.
