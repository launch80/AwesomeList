<!-- GENERATED from catalog/projects/capicua-vllm-rocm-rdna4.yaml by scripts/build.py — do not edit. -->

# Capicua25x/vllm-rocm-rdna4

**RDNA4 vLLM fork — Qwen 3.8 27B MXFP4 at 200K context with MTP on 2× RX 9070 XT.**

**Use it if:** You have RDNA4 cards (RX 9070 XT or R9700-class) and want long-context MXFP4 serving with MTP.

| Field | Value |
|---|---|
| Status | `unverified` — Submitted but not yet reproduced by a maintainer or community volunteer. |
| Verification | `author_reported` — The author published the setup and results; not independently reproduced. |
| Kind | A fork of an existing inference runtime. |
| Hardware | RDNA4 (gfx1201); tested on Radeon RX 9070 XT, Radeon AI PRO R9700 |
| Software | _not yet documented_ |
| Runtime | vLLM |
| Models tested | Qwen 3.8 27B |
| Quantization | mxfp4 |
| Provides | `openai_api`, `mtp`, `speculative_decoding`, `long_context`, `continuous_batching` |
| Topology | dual_gpu |
| Not suitable for | GPUs outside RDNA4 (e.g. RDNA2, RDNA3, RDNA3.5) |
| Audience | `developer` — Comfortable building runtimes from source and applying patches. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **capicua25x**, shared by @Darkmoon.

**Quick start:**

Follow the [repository README](https://github.com/Capicua25x/vllm-rocm-rdna4) — no pinned commands recorded yet.

**Known issues:** none recorded.

## Evidence

| GPUs | Model | Quant | Context | Concurrency | Decode tok/s | Prefill tok/s | Runtime | Mode | Fields reported | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 2× Radeon RX 9070 XT | Qwen 3.8 27B MXFP4 | mxfp4 | 200K | not reported | ~140 (peak) | — | vLLM MTP | batched | 3/16 | list_entry |
| 2× Radeon RX 9070 XT | Qwen 3.8 27B MXFP4 | mxfp4 | 200K | 1 | ~50 | — | vLLM MTP | single_stream | 4/16 | list_entry |

## Links

[Repository](https://github.com/Capicua25x/vllm-rocm-rdna4) · [Record](../../catalog/projects/capicua-vllm-rocm-rdna4.yaml)
