# MAID Autonomous Development Queue v1 — operational runbook

GitHub source: https://github.com/karanzing1992/airo
Original baseline PR: https://github.com/karanzing1992/airo/pull/14 (MIT upstream commit 60206bd164bbe271e74543cc616de5f2278da511)
First Groq OpenCode success: https://github.com/karanzing1992/airo/actions/runs/41411335880 ; draft PR #20
This workflow extends the proven pilot with a **scheduled bounded queue**, not a fully autonomous release certification.

## Existing assets and free/open/cost gate
OpenCode 1.19.3 MIT, MAID upstream MIT, GH Actions runner, Groq-hosted open-weight GPT OSS 120B subject to owner free-tier quotas. No new paid components or tokens added. One LLM call per selected issue cycle, one concurrent execution, 4h schedule, and hard timeouts. No inference happens when no eligible issue. Never silently upgrade billing or claim unlimited inference. Revert this source commit to disable the queue.

## Queue rules
- Workflow on GitHub default branch; schedule 17 minutes after every 4th UTC hour, owner-only `/maid-autonomous-run` issue comment on #1 or #2, or owner-only manual workflow_dispatch.
- Admission is a read-only job; denies unrelated comments and authors.
- Only pre-authored tasks in `docs/maid/AUTONOMOUS_ISSUE_POLICY.json` can be selected. GitHub issue bodies, PR text and comments are NEVER pasted into model prompt. Owner-created matching open issues only.
- M0 stage works on the pinned upstream source branch and fixes lint/dependency configuration only; it does not merge PR #14. Issue 2+ requires M0 upstream on default branch and upstream issue closed. All stages respect dependency closure.
- Stop if any existing `MAID AUTO:` PR remains open or a previous issue-specific auto PR exists, even if closed; no duplicate PRs on repeated schedules.
- AI tool sandbox forbids bash and webfetch; GitHub Actions itself still runs explicit shell, dependencies, network checks and GitHub operations. This is NOT unrestricted secure sandboxing or protection from all supply-chain vulnerabilities.
- Strict path/size/count, no symlinks/deletes/renames. M0 lint and Jest tests must run non-interactively and pass. PR is **draft only**.
- After test failures the issue is marked `maid:blocked`; no repeat spending until review. Separate existing draft PR #20 has its own editorial review and does not grant general source certification.

## Source and release gates
- Automatic code generation and test, PR publication only. NO automatic merge; no production Cloudflare/web release, root/host agents, keystores, personal media, account binding or APK publishing.
- No bypass of G0-G6 gates, independent security QA, device QA, Dell/Mac thermal constraints, or user approval for risk-relevant operations.
- When the issue PR is accepted/merged and source milestone issue closed, the schedule advances to the next dependency-satisfied stage.
- Issue #13 (signed APK/public release) is excluded from this coding queue and remains owner-gated. Stage #12's generated security tests cannot self-certify itself.
- GitHub Actions can be delayed or paused; its presence does not guarantee uninterrupted execution. Check Actions run receipts before claiming new capabilities.

## Stop, resume and recovery
- Disable workflow or revert it to stop future scheduled runs. GitHub Actions UI can cancel an active job. No automatic retry after a failed test.
- Check `maid:blocked` label and Actions error; submit a reviewed fix, remove label to re-enable, or manually dispatch after a correction.
- Keep source_sha, tested_sha, artifact_sha explicit; never claim signed APK or web application release without evidence.

## Groq tool-call compatibility fix (2026-11-02)
Original worker run 41414565727 correctly selected I01 and used a strong Groq model, but failed when the model emitted an OpenCode read tool call without its mandatory filePath. The fault was in LLM tool-call compatibility, not owner authorization or Groq credentials. The issue was blocked automatically; no code pushed.
The repair uses Groq API strict JSON schema (one files[] array with path and full file content) and a local deterministic writer without exposing AI read/bash/network tools. Path/symlink/dependency integrity validation and post-generation yarn lint + Jest remain mandatory. The backend is still Groq GPT OSS 120B and free-tier usage is bounded to one response per selected task. OpenCode remains available for separate approved interactive coding; structured writer is the unattended pipeline.

## Official Groq SDK transport correction
Second I01 run 41415260687 failed closed with HTTP 403 from Python stdlib urllib immediately, before model response. Historical MAD/Goa stack hit the same urllib/Cloudflare issue and solved it using the official Groq SDK. Autonomy now pins official open-source Python groq SDK v1.7.0 (Apache-2.0), runs through its httpx transport, and preserves strict JSON-schema output and deterministic path/diff tests. This correction does not increase model quota, allow shell tools or broaden write privileges. Provider runtime and first I01 draft PR are unverified until retried.
