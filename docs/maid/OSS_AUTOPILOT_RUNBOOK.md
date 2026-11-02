# MAID Groq GPT OSS 120B Autopilot — Runbook v2
Date: 2026-11-02 | Repository: karanzing1992/airo | Source-only workflow (not a certified Android manager release)

## Reuse and cost gate
- MAID original: https://github.com/Mobile-Artificial-Intelligence/maid , MIT, pinned revision `60206bd164bbe271e74543cc616de5f2278da511`; draft import PR #14 retained unchanged.
- OpenCode: https://github.com/anomalyco/opencode , MIT, CLI 1.19.3, already used in Dell pilot and native Groq integration.
- Groq hosted inference: https://console.groq.com/docs/coding-with-groq , model ID `openai/gpt-oss-120b` (strong production-tier coding and tool-using model). Open weight but Groq hosting is proprietary provider-managed. API usage may cost money outside free allowances: run only with an existing approved free-tier key and stay within quotas. No auto-upgrade, no paid subscription configured by this workflow.
- GitHub Actions: https://docs.github.com/actions , free public repository actions subject to platform quotas. No extra host machine or private repo credentials for pilot.

## Why we switched
Prior GitHub Actions run 41408524811 successfully invoked local Ollama model Qwen2.5 Coder 1.5B, but it printed a JSON pseudo-task instead of creating the requested file. The strict diff gate correctly failed and nothing was pushed. The user explicitly requested a strong Groq model. Groq GPT OSS 120B is now the only configured agent backend, not an automatic fallback to Ollama.

## Credentials
Set repository **Actions secret** `GROQ_API_KEY` for `karanzing1992/airo` from the owner's already-authorized Groq account. Only GitHub protected jobs on `master` receive the key. Do NOT paste keys in issues, PRs, source files, app config, chat or stdout. GitHub workflow token for publishing pilot PR is ephemeral and scoped to `contents: write` and `pull-requests: write`. The credential is **not** automatically copied from ChatGPT, Cloudflare, Dell or another GitHub repo. Without an authorized secret the smoke and pilot fail closed.

## Execution
1. All changes proposed in a separate PR. PR checks include exact-owner issue validation tests and configuration/negative safeguards; secrets are never exposed during PR tests.
2. After review and merge into `master`, the workflow runs **real Groq inference smoke** on the merged source SHA. A successful YAML validation alone is not an inference test. Investigate 401/403, 429, model retired, or quota outage without upgrading billing.
3. Once smoke passes, the repository owner can post exactly `/maid-oss` on https://github.com/karanzing1992/airo/issues/16 . This is the sole enabled issue: not production issue queue.
4. GitHub Actions validates actor/sender/issue/comment; agent must create one specific Markdown file `docs/maid/AUTOPILOT_PILOT_RESULT.md`. Both the file's existence and the sole allowed diff are validated before any push.
5. If the guard succeeds, a **draft** PR is created. Review changes, CI and GitHub logs; no automatic merges or Android release.
6. Only after this gate succeeds may broader issue-dependency automation be designed and independently certified. Feature parity, real Dell/Mac agents, security and APK release are separate issues.

## Owner gates and rollback
No production launch, machine agent enrollment, root operations, Firebase/Android signing or release approval is implicit. Revert the Groq pilot commit to disable this worker. If missing credentials, stop; do not install another inference service, use another project token, or claim success. The model may make inaccurate changes, so tool permission prevents shell/network execution and the one-file allowlist prevents unauthorized writes from being published. This is a development pilot, not a sandbox for third-party issues.
