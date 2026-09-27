<!-- GENERATED from catalog/projects/int8-vllm.yaml by scripts/build.py — do not edit. -->

# curvedinf/int8-vllm

**INT8-optimized vLLM — Qwen3.8-27B C8 at 972 t/s TG / 5,680 PP on 4× MI100.**

**Use it if:** You have MI100s (CDNA1) and want high-throughput INT8 serving.

| Field | Value |
|---|---|
| Status | `unverified` — Submitted but not yet reproduced by a maintainer or community volunteer. |
| Verification | `author_reported` — The author published the setup and results; not independently reproduced. |
| Kind | A fork of an existing inference runtime. |
| Hardware | CDNA (gfx908); tested on Instinct MI100 |
| Software | _not yet documented_ |
| Runtime | vLLM |
| Models tested | Qwen3.8-27B C8 |
| Quantization | int8 |
| Provides | `openai_api`, `custom_kernels` |
| Topology | multi_gpu |
| Not suitable for | GPUs outside CDNA (e.g. RDNA2, RDNA3, RDNA3.5) |
| Audience | `developer` — Comfortable building runtimes from source and applying patches. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **curvedinf**, shared by @mldatascientist.

**Builds on:** [curvedinf/int8-aiter](int8-aiter.md)

**Quick start:**

Follow the [repository README](https://github.com/curvedinf/int8-vllm) — no pinned commands recorded yet.

**Known issues:** none recorded.

## Evidence

| GPUs | Model | Quant | Context | Concurrency | Decode tok/s | Prefill tok/s | Runtime | Mode | Fields reported | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 4× Instinct MI100 | Qwen3.8-27B C8 | int8 | not reported | not reported | 972 | 5,680 | vLLM | not_reported | 2/16 | [reddit](https://www.reddit.com/r/LocalLLaMA/comments/1vz9hqa/qwen38_27b_c8_at_972_tg_5680_pp_on_4x_mi100_rig/) |

## Links

[Repository](https://github.com/curvedinf/int8-vllm) · [Write-up](https://www.reddit.com/r/LocalLLaMA/comments/1vz9hqa/qwen38_27b_c8_at_972_tg_5680_pp_on_4x_mi100_rig/) · [Record](../../catalog/projects/int8-vllm.yaml)
