<!-- GENERATED from catalog/projects/vllm-mxfp4.yaml by scripts/build.py — do not edit. -->

# GGZ14/vllm-mxfp4

**MXFP4 fast path on top of the Radiance image, with online conversion of NVFP4 checkpoints.**

**Use it if:** You have R9700s and want the highest reported prefill and decode numbers for 27B-class 4-bit models.

| Field | Value |
|---|---|
| Status | `unverified` — Submitted but not yet reproduced by a maintainer or community volunteer. |
| Verification | `author_reported` — The author published the setup and results; not independently reproduced. |
| Kind | A fork of an existing inference runtime. |
| Hardware | RDNA4 (gfx1201); tested on Radeon AI PRO R9700 |
| Software | Docker |
| Runtime | vLLM |
| Models tested | Qwen3.8-27B NVFP4 |
| Quantization | mxfp4, nvfp4 |
| Provides | `openai_api`, `custom_kernels` |
| Topology | — |
| Not suitable for | GPUs outside RDNA4 (e.g. RDNA2, RDNA3, RDNA3.5) |
| Audience | `developer` — Comfortable building runtimes from source and applying patches. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **The_Candle_Watcher**.

**Builds on:** [StillDeadcode/vllm-radiance](vllm-radiance.md)

**Quick start:**

Follow the [repository README](https://github.com/GGZ14/vllm-mxfp4) — no pinned commands recorded yet.

**Known issues:** none recorded.

## Evidence

| GPUs | Model | Quant | Context | Concurrency | Decode tok/s | Prefill tok/s | Runtime | Mode | Fields reported | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| Radeon AI PRO R9700 (count not reported) | Qwen3.8-27B NVFP4 (online MXFP4 conversion) | nvfp4 | not reported | not reported | 276 | 5,809 | vLLM | not_reported | 1/16 | list_entry |

## Links

[Repository](https://github.com/GGZ14/vllm-mxfp4) · [Mirror](https://codeberg.org/ggz14/radiance-vllm-mxfp4) · [Record](../../catalog/projects/vllm-mxfp4.yaml)
