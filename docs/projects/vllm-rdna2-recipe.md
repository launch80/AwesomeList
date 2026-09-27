<!-- GENERATED from catalog/projects/vllm-rdna2-recipe.yaml by scripts/build.py — do not edit. -->

# leapdragon/vllm-rdna2-recipe

**Deployment recipe for vLLM on RDNA2, including a fix for prefill blocking generation.**

**Use it if:** You are deploying vLLM on V620s and want the documented steps plus the concurrency fix.

| Field | Value |
|---|---|
| Status | `unverified` — Submitted but not yet reproduced by a maintainer or community volunteer. |
| Verification | `author_reported` — The author published the setup and results; not independently reproduced. |
| Kind | Step-by-step deployment documentation or stack guide. |
| Hardware | RDNA2 (gfx1030); tested on Radeon Pro V620 |
| Software | _not yet documented_ |
| Runtime | vLLM |
| Models tested | _not yet documented_ |
| Quantization | — |
| Provides | `openai_api`, `continuous_batching` |
| Topology | multi_gpu |
| Not suitable for | GPUs outside RDNA2 (e.g. RDNA3, RDNA3.5, RDNA4) |
| Audience | `operator` — Comfortable with Docker, drivers and launch flags. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **leapdragon** · Contributors: wsantos.

**Builds on:** [leapdragon/vllm-rdna2-qwen](vllm-rdna2-qwen.md)

**Quick start:**

Follow the [repository README](https://github.com/leapdragon/vllm-rdna2-recipe) — no pinned commands recorded yet.

**Known issues:** none recorded.

## Evidence

| GPUs | Model | Quant | Context | Concurrency | Decode tok/s | Prefill tok/s | Runtime | Mode | Fields reported | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 4× Radeon Pro V620 | not reported | — | not reported | 8 | ~150 | — | vLLM | batched | 2/16 | list_entry |

## Links

[Repository](https://github.com/leapdragon/vllm-rdna2-recipe) · [Record](../../catalog/projects/vllm-rdna2-recipe.yaml)
