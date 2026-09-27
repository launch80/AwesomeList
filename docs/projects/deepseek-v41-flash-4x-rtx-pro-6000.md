<!-- GENERATED from catalog/projects/deepseek-v41-flash-4x-rtx-pro-6000.yaml by scripts/build.py — do not edit. -->

# 0xSero/deepseek-v4.1-flash-4x-rtx-pro-6000

**DeepSeek-V4.1-Flash on 4× RTX Pro 6000 at ~200 t/s TG / 7k PP at 8k context.**

**Use it if:** You have a 4× RTX Pro 6000 (Blackwell) box and want to serve DeepSeek-V4.1-Flash.

| Field | Value |
|---|---|
| Status | `unverified` — Submitted but not yet reproduced by a maintainer or community volunteer. |
| Verification | `author_reported` — The author published the setup and results; not independently reproduced. |
| Kind | Step-by-step deployment documentation or stack guide. |
| Hardware | NVIDIA Blackwell; tested on RTX Pro 6000 Blackwell; 4+ GPUs required |
| Software | _not yet documented_ |
| Runtime | vLLM |
| Models tested | DeepSeek-V4.1-Flash |
| Quantization | — |
| Provides | `openai_api` |
| Topology | multi_gpu |
| Not suitable for | GPUs outside NVIDIA Blackwell (e.g. RDNA2, RDNA3, RDNA3.5); Fewer than 4 GPUs |
| Audience | `operator` — Comfortable with Docker, drivers and launch flags. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **0xSero**, shared by @mldatascientist.

**Quick start:**

Follow the [repository README](https://github.com/0xSero/deepseek-v4.1-flash-4x-rtx-pro-6000) — no pinned commands recorded yet.

**Known issues:** none recorded.

## Evidence

| GPUs | Model | Quant | Context | Concurrency | Decode tok/s | Prefill tok/s | Runtime | Mode | Fields reported | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 4× RTX Pro 6000 Blackwell | DeepSeek-V4.1-Flash | — | 8K | not reported | ~200 | ~7,000 | not reported | not_reported | 2/16 | list_entry |

## Links

[Repository](https://github.com/0xSero/deepseek-v4.1-flash-4x-rtx-pro-6000) · [Record](../../catalog/projects/deepseek-v41-flash-4x-rtx-pro-6000.yaml)
