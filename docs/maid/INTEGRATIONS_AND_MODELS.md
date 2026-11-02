# Integration and Model Adapter Design — complete coverage
## Registry
Each integration is an independently versioned manifest: id, owner, display metadata, transports (MCP, HTTP/OpenAPI, local agent, OAuth), capability descriptions (read, write, admin, high-risk), auth mechanisms, credentials owner, scoped tool schemas, UI forms, health checks, quotas, model requirements and revocation hooks. Register centrally, render in both Android and web from same schema. No Android APK rebuild required for new server integrations unless native hardware capabilities change.

## Initial connector acceptance targets
- Dell Development Yard: inventory, jobs, safe shell with approvals, process/system/service metadata, Python/Node QA, code changes, Git, browser automation, recovery safety, receipts.
- Mac MAD Yard: inventory, FFmpeg/media/video services, browser automation, business workflows, system health/thermal, receipts.
- Model providers: OpenAI-compatible, Groq, Gemini, Ollama on host, local GGUF on phone, optional Cloudflare Workers AI, LiteLLM external. Provider credentials only server-side or secure on-device for user-selected direct API usage.
- Developer: GitHub repo/issues/PR/checks/releases and Cloudflare deploy/metrics, role authorization. Avoid auto-production deploy until QA/owner signoff.
- WordPress: WP Manager authorized site discovery and scoped read/write actions, explicit site selection.
- Workspace and knowledge: Google Drive/Docs/Sheets, optional Gmail/Calendar, filesystem, R2, RAG, task artifact index; honor connection and owner permissions.
- Media: FFmpeg, open-licensed media retrieval with attribution/license manifest, audio transcription, TTS, image and video processing with actual tool receipts.
- Notification: in-app, Web Push, Android notification, optional Telegram/email with opt-in.

## Router
Virtual `auto` selects model based on modality, tool support, risk, classification, throughput, quality evidence, cost/free quota, context, latency and provider health. A low-cost small model first except complex reasoning / security / code review. For high-risk machine modifications, model reasoning cannot override policy or owner approval. Model routing and execution scheduling separate. Stronger model escalation on confidence/verification failures. Provider fallback requires compatible modality/context; never silently drop images, files, function calls, or authorization scopes. Return explainable route metadata.

## Multimodal data
Text, images, documents, voice audio, screenshots, artifact media, tool receipts. Exact mime types, payload size, max lengths and long-running transcoding are backend policy. Large blobs go direct to R2 with signed URL and virus/size scanning; never echo credentials into prompts. Consent/retention flags, per-project ACL and secure deletion policy.

## Required tests
- New manifest appears in both interfaces; discovery and version changes do not break old app
- Unauthorized connector denied; reduced scopes reduce tools displayed and callable
- OAuth expiration/refresh/revocation; no credentials in API logs or screenshots
- Model overload, 429, vision mismatch, provider outage, context overflow, malicious tool prompt
- Two hosts offline/one host offline, task replay, signed receipt substitution, cross-project isolation
