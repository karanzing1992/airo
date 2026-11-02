# MAID Unified Function Matrix — mandatory parity
Legend: P = required tested capability; N = native-specific function and defined browser substitute; F = future optional enhancement. Every P must be in both clients or a release-blocking defect.

| Feature | Android MAID | Mobile web PWA | Desktop web | Definition of acceptance |
|---|---|---|---|---|
| Owner sign-in / session revoke | P | P | P | logout/revoke across devices |
| Chat stream, stop, history, search | P | P | P | shared project history & cross-device sync |
| Model `auto`, routing reason, override | P | P | P | same backend decisions across surfaces |
| Local GGUF on phone | N | N (remote-model alternative) | N (remote-model alternative) | original MAID offline behavior preserved |
| Text / code / markdown / structured tool cards | P | P | P | identical task semantics |
| Attachment pick / images / document uploads | P | P | P | verified permissions + encrypted transport |
| Camera and screenshot ingest | P | P | P | native capture vs browser selection/capture |
| STT / speech controls / TTS / transcripts | P | P | P | permission denial gracefully handled |
| Voice interrupt / pause / playback | P | P | P | at least push-to-talk P0, full duplex optional later |
| Dell/Mac live status, resources and lanes | P | P | P | no invented online status |
| Jobs: create/observe/pause/cancel/resume | P | P | P | receipt-based transitions |
| Owner approvals for dangerous commands | P | P | P | refusal, expiry, revocation covered |
| Integrations catalog + OAuth/admin tools | P | P | P | common manifest and permissions |
| Add/remove MCP connectors | P | P | P | backend registration with approval |
| Project workspaces and RAG retrieval | P | P | P | ACL isolation and document provenance |
| Tool audit, traces, log views | P | P | P | scoped detailed view, redact secrets |
| Task artifacts / media preview / download | P | P | P | hash checks + short-lived signed URLs |
| Push notifications | N | N | N | use supported native / Web Push or in-app alerts |
| Dark/light theme, accessibility, localization | P | P | P | keyboard, screen readers, reduced motion |
| Offline messaging / pending queue UI | P | P | P | honest stale state; commands require auth |
| Device keyring / biometric unlock | N | N | N | secure platform local storage or passkey |
| Emergency stop / disconnect all hosts | P | P | P | revocation independent of LLM |
| Admin usage limits / provider quota | P | P | P | quotas and hard-stop policy available |
| Integration plugin UI from manifests | P | P | P | new connector can appear without app rewrite |

Release gates: test phone widths 320/360/390/430, tablet 768, desktop 1024/1280/1440+; Android physical ARM64, Web Chromium+Firefox+WebKit, portrait/landscape where supported. Provide screenshots, accessibility and functional evidence for every P and all N substitutes.
