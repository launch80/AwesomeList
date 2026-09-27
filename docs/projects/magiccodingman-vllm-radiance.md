<!-- GENERATED from catalog/projects/magiccodingman-vllm-radiance.yaml by scripts/build.py — do not edit. -->

# magiccodingman/vllm-radiance

**Radiance rebased onto current vLLM main with DFlash2 and MXFP4 work merged in.**

**Use it if:** You have an R9700 and want the Radiance-specific paths on a newer vLLM/PyTorch/ROCm stack, and can debug an experimental build.

| Field | Value |
|---|---|
| Status | `experimental` — Promising proof of concept or work in progress; expect manual debugging. |
| Verification | `unverified` — Nobody outside the author has confirmed the setup or its numbers. |
| Kind | A fork of an existing inference runtime. |
| Hardware | RDNA4 (gfx1201); tested on Radeon AI PRO R9700 |
| Software | AMD PyTorch 2.12 / Triton 3.7.1 / AITER 0.1.20 / ROCm 7.14 (as stated by the author). |
| Runtime | vLLM |
| Models tested | _not yet documented_ |
| Quantization | mxfp4 |
| Provides | `openai_api`, `dflash`, `speculative_decoding` |
| Topology | — |
| Not suitable for | GPUs outside RDNA4 (e.g. RDNA2, RDNA3, RDNA3.5) |
| Audience | `developer` — Comfortable building runtimes from source and applying patches. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **slurp**.

**Builds on:** [StillDeadcode/vllm-radiance](vllm-radiance.md)

**Quick start:**

Follow the [repository README](https://github.com/magiccodingman/vllm-radiance) — no pinned commands recorded yet.

**Known issues:** none recorded.

**Notes:** Also mirrored on GitLab.

## Evidence

No benchmark records yet. Run [BetterBench](betterbench.md) and submit the result.

## Links

[Repository](https://github.com/magiccodingman/vllm-radiance) · [Record](../../catalog/projects/magiccodingman-vllm-radiance.yaml)
