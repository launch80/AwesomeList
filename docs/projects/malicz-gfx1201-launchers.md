<!-- GENERATED from catalog/projects/malicz-gfx1201-launchers.yaml by scripts/build.py — do not edit. -->

# malicz/vllm-gfx1201-launchers

**Single-R9700 Radiance + MXFP4 setup — Dockerfile, model download, MTP conversion and patches.**

**Use it if:** You have one R9700 and want a complete Docker-based MXFP4 setup with 160K context.

| Field | Value |
|---|---|
| Status | `unverified` — Submitted but not yet reproduced by a maintainer or community volunteer. |
| Verification | `author_reported` — The author published the setup and results; not independently reproduced. |
| Kind | Launch scripts / configs for an existing runtime. |
| Hardware | RDNA4 (gfx1201); tested on Radeon AI PRO R9700 |
| Software | Docker |
| Runtime | vLLM |
| Models tested | Qwen3.8-27B MXFP4 |
| Quantization | mxfp4 |
| Provides | `openai_api`, `mtp`, `dflash`, `speculative_decoding`, `long_context` |
| Topology | single_gpu |
| Not suitable for | GPUs outside RDNA4 (e.g. RDNA2, RDNA3, RDNA3.5) |
| Audience | `operator` — Comfortable with Docker, drivers and launch flags. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **malicz**.

**Builds on:** [StillDeadcode/vllm-radiance](vllm-radiance.md)

**Quick start:**

Follow the [repository README](https://github.com/malicz/vllm-gfx1201-launchers) — no pinned commands recorded yet.

**Known issues:** none recorded.

**Notes:** Built on Deadcode's and Brian's work; includes patches such as patch_dflash_w4a16_kv.py.

## Evidence

| GPUs | Model | Quant | Context | Concurrency | Decode tok/s | Prefill tok/s | Runtime | Mode | Fields reported | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 1× Radeon AI PRO R9700 | Qwen3.8-27B MXFP4 | mxfp4 | 160K | not reported | ~81 | ~2,380 | vLLM | not_reported | 3/16 | list_entry |

## Links

[Repository](https://github.com/malicz/vllm-gfx1201-launchers) · [Record](../../catalog/projects/malicz-gfx1201-launchers.yaml)
