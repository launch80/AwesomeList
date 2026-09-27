<!-- GENERATED from catalog/projects/mi210-vllm.yaml by scripts/build.py — do not edit. -->

# davetha/mi210-vllm

**vLLM build with the AITER patches for MI210, including a full INT8 Qwen3.8-27B recipe.**

**Use it if:** You have an MI210 and want a ready docker-run recipe for INT8 Qwen serving.

| Field | Value |
|---|---|
| Status | `unverified` — Submitted but not yet reproduced by a maintainer or community volunteer. |
| Verification | `unverified` — Nobody outside the author has confirmed the setup or its numbers. |
| Kind | A fork of an existing inference runtime. |
| Hardware | CDNA2 (gfx90a); tested on Instinct MI210 |
| Software | Docker |
| Runtime | vLLM |
| Models tested | Qwen3.8-27B INT8 |
| Quantization | int8 |
| Provides | `openai_api`, `custom_kernels` |
| Topology | — |
| Not suitable for | GPUs outside CDNA2 (e.g. RDNA2, RDNA3, RDNA3.5) |
| Audience | `operator` — Comfortable with Docker, drivers and launch flags. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **davetha**.

**Builds on:** [davetha/aiter-cdna2](aiter-cdna2.md)

**Built on by:** [davetha/mi210-llm-stack](mi210-llm-stack.md)

**Quick start:**

Follow the [repository README](https://github.com/davetha/mi210-vllm) — no pinned commands recorded yet.

**Known issues:** none recorded.

## Evidence

No benchmark records yet. Run [BetterBench](betterbench.md) and submit the result.

## Links

[Repository](https://github.com/davetha/mi210-vllm) · [Record](../../catalog/projects/mi210-vllm.yaml)
