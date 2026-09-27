<!-- GENERATED from catalog/projects/vllm-rdna2-qwen.yaml by scripts/build.py — do not edit. -->

# leapdragon/vllm-rdna2-qwen

**vLLM fork for 4× V620 — ~70 t/s with MTP=3 on Qwen3.8-Flash-Next W4A16.**

**Use it if:** You have a multi-V620 (RDNA2) server and want Qwen serving with MTP.

| Field | Value |
|---|---|
| Status | `unverified` — Submitted but not yet reproduced by a maintainer or community volunteer. |
| Verification | `author_reported` — The author published the setup and results; not independently reproduced. |
| Kind | A fork of an existing inference runtime. |
| Hardware | RDNA2 (gfx1030); tested on Radeon Pro V620 |
| Software | _not yet documented_ |
| Runtime | vLLM |
| Models tested | Qwen3.8-Flash-Next W4A16 |
| Quantization | w4a16 |
| Provides | `openai_api`, `mtp`, `speculative_decoding` |
| Topology | multi_gpu |
| Not suitable for | GPUs outside RDNA2 (e.g. RDNA3, RDNA3.5, RDNA4) |
| Audience | `developer` — Comfortable building runtimes from source and applying patches. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **leapdragon**, shared by @Schimazing.

**Built on by:** [leapdragon/vllm-rdna2-recipe](vllm-rdna2-recipe.md)

**Host:** Reported on a Zen 2 EPYC / PCIe Gen4 platform.

**Quick start:**

Follow the [repository README](https://github.com/leapdragon/vllm-rdna2-qwen) — no pinned commands recorded yet.

**Known issues:** none recorded.

## Evidence

| GPUs | Model | Quant | Context | Concurrency | Decode tok/s | Prefill tok/s | Runtime | Mode | Fields reported | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 4× Radeon Pro V620 | Qwen3.8-Flash-Next W4A16 | w4a16 | not reported | not reported | ~70 | — | vLLM MTP=3 | not_reported | 4/16 | list_entry |

## Links

[Repository](https://github.com/leapdragon/vllm-rdna2-qwen) · [Record](../../catalog/projects/vllm-rdna2-qwen.yaml)
