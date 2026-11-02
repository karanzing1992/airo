# MAID M0 Groq Repair
Source branch bootstrap/maid-upstream-60206bd / original upstream MAID MIT pinned revision 60206bd164bbe271e74543cc616de5f2278da511.
Six genuine lint errors in four upstream components found on run 41416602952. Groq 120B proposes exact find/replace snippets with strict JSON schema; Python validator limits changes to the four component files, forbids lint suppressions, rejects ambiguous snippets. Deterministic Expo 57 ESLint bootstrap preserves dependencies and scripts.
Actions must prove true lint and Jest green before creating draft PR into source import branch PR #14. No automatic merge or release, no signing keys, no production host operations, no APK claim from the source PR. GitHub Actions and Groq free tiers only. Workflow may be disabled or reverted to stop.

## High-capability coding model change (2026-11-02)
Primary: Groq `qwen/qwen3.8-27b`, high reasoning, strict JSON schema and 3900 completion-token cap. Groq reports LiveCodeBench v6 90.3% and SWE-bench Pro 61.7%. Free-tier quotas apply; preview model access can change. GPT OSS 120B is a separately verified alternative, not an automatic paid fallback. No human review, lint or release gates are waived.
