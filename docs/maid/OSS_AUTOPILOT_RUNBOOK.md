# MAID Open-Source Autonomous Coding Worker — Pilot Runbook
Date: 2026-11-02 | Repo: karanzing1992/airo | Version: pilot-1 (not production release)

## Reference / reuse / cost gate
- [MAID upstream](https://github.com/Mobile-Artificial-Intelligence/maid), MIT, pinned 60206bd164bbe271e74543cc616de5f2278da511. Existing MAID Android source is in draft PR #14 and must not be overwritten.
- [OpenCode](https://github.com/anomalyco/opencode), MIT, CLI pinned 1.19.3; installed previously on Dell but its configured local Ollama endpoint was offline. This pilot instead uses an ephemeral GitHub-hosted runner to avoid Dell GitHub token access.
- [Ollama](https://github.com/ollama/ollama), MIT. Model [Qwen2.5-Coder 1.5B](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct), Apache-2.0. Verify license in the loaded source before distribution. Runs on GitHub-hosted CPU, no commercial model API or Copilot.
- [GitHub Actions](https://docs.github.com/actions), public-repository hosted CI subject to platform fair-use, storage, network and security limits; no inference guarantees or unlimited free compute.
- This is a small model for a narrowly scoped pilot. The future production coding worker must benchmark a stronger free model, preferably from verified owned local hardware or approved free provider, before writing security-sensitive code.

## Why this transport
Dell's gh CLI is not authenticated and Ollama service is inactive; using the token provided to GitHub Actions removes the need to store new long-lived GitHub credentials on Dell. The worker runs only on ephemeral GitHub runners; each run pulls a model and is CPU/time-limited. This is not a live Dell/Mac remote agent. Never run third-party issue-sourced commands using untrusted pull_request code with write token.

## What is installed
- .github/workflows/maid-oss-agent.yml: safe CI guards, local model smoke test on main push or workflow_dispatch, and exact-owner gated issue #16 pilot.
- opencode.json: localhost-only model, no API keys, no bash/web requests/external directory permission for the AI.
- scripts/maid_oss_guard.py and tests: negative authorization and allowed-diff validation.
- Issue #16: single doc-file coding pilot.

## Run and verify
1. Merge the workflow bootstrap PR after guard tests pass; a push on master should run the model-smoke and publish its result.
2. Comment the exact line /maid-oss on ISSUE #16 from karanzing1992. No other issue, non-owner, PR comment or suffixed command may trigger coding.
3. Inspect Github Actions job; verify successful real inference, actual docs/maid/AUTOPILOT_PILOT_RESULT.md diff, exactly one changed file, safe source SHA and successful draft PR creation.
4. Review PR; verify no claimed certification without test evidence; merge only after owner/QA approval.
5. Future iteration after pilot: replace pilot-only allowlist with issue dependency queue, capability requirements, CLI contract tests, Android/web CI and independent code-review gates. Never automatically deploy/sign/release before G5/G6 certification and host enrollment.
6. Status labels: PREPARED != RUNNING != TEST_PASSED != PR_CREATED != MERGED != RELEASED.

## Failure and recovery
- Ollama download/endpoint failure: fail job, no PR; do not retry indefinitely or spend on paid API.
- OpenCode unavailable / tool invocation failure: fail job with log; no unauthenticated fallback.
- GitHub workflow write permission unavailable: no PR; inspect Actions > General; preserve least privilege.
- Unexpected changed file: fail closed, do not push.
- Missing model or model cannot follow instructions: no unverified claims, record failure and adjust only in a reviewed PR.
- No forced Git operations or automated merging. No shared host service, token or Firefox session modified.
- Revert automation merge commit to roll back; leave existing MAID PR and docs intact. Issue #16 can be closed when independently certified.
