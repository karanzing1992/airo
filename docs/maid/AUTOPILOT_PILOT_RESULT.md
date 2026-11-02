# AUTOPILOT Pilot Result

## Objective
Document the outcome of the MAID Groq GPT‑OSS‑120B autopilot pilot. The pilot’s purpose is to prove that a single‑file, guarded GitHub‑Actions workflow can invoke the strong Groq model, generate a deterministic Markdown result, and have that result validated by CI before any repository changes are merged.

## Architecture
1. **GitHub Actions workflow** – runs on `master` when the issue comment `/maid-oss` is posted. The workflow:
   - Checks that the comment actor matches the repository owner.
   - Loads the secret `GROQ_API_KEY` (owner‑authorized Groq token).
   - Calls the Groq endpoint `openai/gpt-oss-120b` with the prompt generated from the issue description.
   - Writes **only** `docs/maid/AUTOPILOT_PILOT_RESULT.md` and nothing else.
2. **Guarded diff** – before any push the CI step verifies that the PR contains exactly one file addition with the expected path and that the diff touches no other paths. If the guard fails, the run aborts.
3. **Draft PR creation** – on successful guard a draft PR is opened for human review. No automatic merge occurs.

## Model
The pilot uses Groq’s hosted inference model `openai/gpt-oss-120b`. It is the strongest production‑tier coding model available on Groq, offering the full 120‑billion‑parameter capacity of the OpenAI OSS release. The model weights are public, but inference is provided as a managed service; usage is billed to the owner’s Groq account and subject to quota limits.

## Security
- **Owner authorization** – the only credential required is the `GROQ_API_KEY` stored as a protected GitHub Actions secret. The secret is injected only into the protected `master` workflow; it never appears in logs, source files, or issue comments.
- **Write‑allowlist** – CI enforces a strict one‑file allowlist (`docs/maid/AUTOPILOT_PILOT_RESULT.md`). All other file writes are rejected, preventing accidental or malicious repository modifications.
- **No external execution** – the sandbox disables shell and network calls other than the Groq API, eliminating the risk of arbitrary code execution.

## Test Plan
1. **Local model sanity check (historical)** – The previous pilot using a local Ollama Qwen2.5‑Coder 1.5B produced a JSON task instead of the requested file, demonstrating the need for a stronger model.
2. **Smoke test** – After merging the PR, the workflow performs a lightweight inference call that must return a non‑error response (status 200) and a well‑formed Markdown payload.
3. **Guard verification** – CI confirms that the diff contains exactly one new file at the expected location and that the file content matches the Markdown schema defined here.
4. **Human review** – A repository maintainer reviews the draft PR, checks the generated Markdown for completeness, and manually merges if satisfied.
5. **Evidence collection** – Logs from the GitHub Actions run (including request IDs, response timestamps, and any error codes) are archived as proof of a successful Groq inference.

## Open Blockers
- **Quota / rate‑limit uncertainty** – The pilot relies on the owner’s free‑tier Groq quota. If the quota is exhausted or the model is retired, the workflow will return 429/403 errors and the pilot cannot complete.
- **Evidence limitations** – The only observable artifact is the generated Markdown file and CI logs. There is no external checksum or cryptographic attestation of the model’s internal reasoning.
- **Future verification steps** – To increase confidence, the next iteration should capture the full HTTP response payload (including request ID) and store it as an artifact, allowing independent replay or audit.
- **Model retirement risk** – Should Groq discontinue `openai/gpt-oss-120b`, the workflow would need to be re‑targeted to a replacement model before any further pilots can run.

*This document records the pilot result without asserting any production deployment or certification status.*
