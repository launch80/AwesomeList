<!-- GENERATED from catalog/projects/vllm-radlight.yaml by scripts/build.py — do not edit. -->

# hifi/vllm-radlight

**Lightweight vLLM variant; median decode above 70 t/s on one R9700 with Qwen3.8-27B at 192K context.**

**Use it if:** You run a single R9700 and want long-context Qwen serving from a lighter vLLM variant with published bench results.

| Field | Value |
|---|---|
| Status | `unverified` — Submitted but not yet reproduced by a maintainer or community volunteer. |
| Verification | `author_reported` — The author published the setup and results; not independently reproduced. |
| Kind | A fork of an existing inference runtime. |
| Hardware | RDNA4 (gfx1201); tested on Radeon AI PRO R9700 |
| Software | _not yet documented_ |
| Runtime | vLLM |
| Models tested | Qwen3.8-27B |
| Quantization | — |
| Provides | `openai_api`, `long_context` |
| Topology | single_gpu |
| Not suitable for | GPUs outside RDNA4 (e.g. RDNA2, RDNA3, RDNA3.5) |
| Audience | `developer` — Comfortable building runtimes from source and applying patches. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **hifi**.

**Quick start:**

Follow the [repository README](https://codeberg.org/hifi/vllm-radlight) — no pinned commands recorded yet.

**Known issues:** none recorded.

## Evidence

| GPUs | Model | Quant | Context | Concurrency | Decode tok/s | Prefill tok/s | Runtime | Mode | Fields reported | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 1× Radeon AI PRO R9700 | Qwen3.8-27B | — | 192K | not reported | ~70 (median) | — | vLLM | not_reported | 2/16 | list_entry |

## Links

[Repository](https://codeberg.org/hifi/vllm-radlight) · [Record](../../catalog/projects/vllm-radlight.yaml)
