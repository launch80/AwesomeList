<!-- GENERATED from catalog/projects/vllm-expert-cache.yaml by scripts/build.py — do not edit. -->

# davetha/vllm-expert-cache

**LRU/LFU expert-cache patch for vLLM so MoE models that would not fit can run on smaller rigs.**

**Use it if:** You want to serve a MoE model that does not fit in your VRAM and can accept some speed loss.

| Field | Value |
|---|---|
| Status | `unverified` — Submitted but not yet reproduced by a maintainer or community volunteer. |
| Verification | `unverified` — Nobody outside the author has confirmed the setup or its numbers. |
| Kind | Patches applied on top of an existing runtime. |
| Hardware | AMD, INTEL — architectures _not yet documented_ |
| Software | _not yet documented_ |
| Runtime | vLLM |
| Models tested | _not yet documented_ |
| Quantization | — |
| Provides | `moe_expert_cache`, `openai_api` |
| Topology | — |
| Not suitable for | — |
| Audience | `developer` — Comfortable building runtimes from source and applying patches. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **davetha**.

**Quick start:**

Follow the [repository README](https://github.com/davetha/vllm-expert-cache) — no pinned commands recorded yet.

**Known issues:** none recorded.

**Notes:** Includes porting docs for Intel. Target GPU architectures not yet recorded.

## Evidence

No benchmark records yet. Run [BetterBench](betterbench.md) and submit the result.

## Links

[Repository](https://github.com/davetha/vllm-expert-cache) · [Record](../../catalog/projects/vllm-expert-cache.yaml)
