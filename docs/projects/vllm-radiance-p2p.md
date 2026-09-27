<!-- GENERATED from catalog/projects/vllm-radiance-p2p.yaml by scripts/build.py — do not edit. -->

# mkadrlik/vllm-radiance-p2p

**vLLM Radiance adapted for 2× RX 7900 with P2P.**

**Use it if:** You have two RX 7900-series cards with P2P and want to serve a 27B AWQ model across the pair.

| Field | Value |
|---|---|
| Status | `unverified` — Submitted but not yet reproduced by a maintainer or community volunteer. |
| Verification | `author_reported` — The author published the setup and results; not independently reproduced. |
| Kind | A fork of an existing inference runtime. |
| Hardware | RDNA3 (gfx1100); tested on Radeon RX 7900 XTX, Radeon RX 7900 XT; 2+ GPUs required |
| Software | _not yet documented_ |
| Runtime | vLLM |
| Models tested | Qwen3.8-27B AWQ |
| Quantization | awq |
| Provides | `openai_api`, `p2p` |
| Topology | dual_gpu_p2p |
| Not suitable for | GPUs outside RDNA3 (e.g. RDNA2, RDNA3.5, RDNA4); Fewer than 2 GPUs |
| Audience | `developer` — Comfortable building runtimes from source and applying patches. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **Froz**.

**Builds on:** [StillDeadcode/vllm-radiance](vllm-radiance.md)

**Quick start:**

Follow the [repository README](https://github.com/mkadrlik/vllm-radiance-p2p) — no pinned commands recorded yet.

**Known issues:** none recorded.

## Evidence

| GPUs | Model | Quant | Context | Concurrency | Decode tok/s | Prefill tok/s | Runtime | Mode | Fields reported | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2× Radeon RX 7900 (XTX or XT, unspecified) (P2P) | Qwen3.8-27B AWQ | awq | not reported | not reported | ~53 | — | vLLM | not_reported | 2/16 | list_entry |

## Links

[Repository](https://github.com/mkadrlik/vllm-radiance-p2p) · [Record](../../catalog/projects/vllm-radiance-p2p.yaml)
