# AUTOPILOT Pilot Result

## Objective
Document the outcome of the MAID Groq GPT‑OSS‑120B autopilot pilot. The pilot’s purpose is to prove that a single‑file, guarded GitHub‑Actions workflow can invoke the strong Groq model, generate a Markdown file, and validate the exact changed-file scope before opening a draft PR. The model's text is not guaranteed deterministic.

## Architecture
1. **GitHub Actions workflow** – runs on `master` when the issue comment `/maid-oss` is posted. The workflow:
   - Checks that the comment actor matches the repository owner.
   - Loads the secret `GROQ_API_KEY` (owner‑authorized Groq token).
   - Calls the Groq endpoint `openai/gpt-oss-120b` with the fixed owner-approved prompt embedded in the workflow; the issue number and comment are only authorization inputs.
   - Writes **only** `docs/maid/AUTOPILOT_PILOT_RESULT.md` and nothing else.
2. **Guarded diff** – before any push the CI step verifies that the PR contains exactly one file addition with the expected path and that the diff touches no other paths. If the guard fails, the run aborts.
3. **Draft PR creation** – on successful guard a draft PR is opened for human review. No automatic merge occurs.

## Model
The pilot uses Groq’s hosted inference model `openai/gpt-oss-120b`. This is the selected 120-billion-parameter open-weight model endpoint for the pilot. Inference runs on Groq's hosted service and is subject to the account's free-tier quotas and terms. This verification does not establish paid usage or a paid plan.

## Security
- **Owner authorization** – the only credential required is the `GROQ_API_KEY` stored as a protected GitHub Actions secret. The secret is injected only into the protected `master` workflow; it never appears in logs, source files, or issue comments.
- **Write‑allowlist** – CI enforces a strict one‑file allowlist (`docs/maid/AUTOPILOT_PILOT_RESULT.md`). All other file writes are rejected, preventing accidental or malicious repository modifications.
- **Agent tool restrictions** – the OpenCode configuration denies bash, webfetch and access outside the workspace. GitHub Actions itself still runs scripted shell/network commands for dependencies, Groq inference and Git operations. These restrictions limit the AI agent but do not constitute a comprehensive sandbox or eliminate all execution risk.

## Test Plan
1. **Local model sanity check (historical)** – The previous pilot using a local Ollama Qwen2.5‑Coder 1.5B produced a JSON task instead of the requested file, demonstrating the need for a stronger model.
2. **Smoke test** – The earlier merged workflow smoke run [41409424998](https://github.com/karanzing1992/airo/actions/runs/41409424998) successfully completed OpenCode inference with Groq and checked for the exact text `MAID_GROQ_120B_READY`. It did not validate a Markdown API response body or separately archive an HTTP status code.
3. **Guard verification** – CI confirms that the diff contains exactly one new file at the expected location and that the file content matches the Markdown schema defined here.
4. **Human review** – A repository maintainer reviews the draft PR, checks the generated Markdown for completeness, and manually merges if satisfied.
5. **Evidence collection** – GitHub Actions [pilot run 41411335880](https://github.com/karanzing1992/airo/actions/runs/41411335880) records the model invocation step, strict diff guard and successful draft PR creation. This PR's one-file diff is the output artifact. No separate Groq request-ID archive or full API response attestation was created.

## Open Blockers
- **Quota / rate‑limit uncertainty** – The pilot relies on the owner’s free‑tier Groq quota. If the quota is exhausted or the model is retired, the workflow will return 429/403 errors and the pilot cannot complete.
- **Evidence limitations** – The only observable artifact is the generated Markdown file and CI logs. There is no external checksum or cryptographic attestation of the model’s internal reasoning.
- **Future verification steps** – Add a sanitized structured receipt recording source SHA, model identifier, elapsed time, request status and relevant provider request ID where legitimately available. Do not archive complete prompts, private code or raw API payloads into public artifacts. Replaying a stochastic model response is not a cryptographic guarantee.
- **Model retirement risk** – Should Groq discontinue `openai/gpt-oss-120b`, the workflow would need to be re‑targeted to a replacement model before any further pilots can run.

*Pilot execution status: verified success for owner-triggered Groq → OpenCode → validated single-file draft PR only. Independent editorial review corrected this record on the same draft branch. Android/web integration, real Dell/Mac manager control, software security certification, final production deployment and signed APK release have not been completed.*
