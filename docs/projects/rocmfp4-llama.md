<!-- GENERATED from catalog/projects/rocmfp4-llama.yaml by scripts/build.py — do not edit. -->

# charlie12345/rocmfp4-llama

**llama.cpp with ROCmFP4 support for RDNA2 and Strix — the recipe V620 owners use.**

**Use it if:** You have a V620 (RDNA2) or a Strix APU and want 4-bit llama.cpp serving with an MTP draft.

| Field | Value |
|---|---|
| Status | `unverified` — Submitted but not yet reproduced by a maintainer or community volunteer. |
| Verification | `unverified` — Nobody outside the author has confirmed the setup or its numbers. |
| Kind | A fork of an existing inference runtime. |
| Hardware | RDNA2, RDNA3.5 (gfx1030, gfx1151); tested on Radeon Pro V620, Ryzen AI Max (Strix Halo) iGPU |
| Software | _not yet documented_ |
| Runtime | llama.cpp |
| Models tested | _not yet documented_ |
| Quantization | gguf_q4_0_rocmfp4 |
| Provides | `openai_api`, `mtp`, `speculative_decoding` |
| Topology | — |
| Not suitable for | GPUs outside RDNA2, RDNA3.5 (e.g. RDNA3, RDNA4, CDNA) |
| Audience | `operator` — Comfortable with Docker, drivers and launch flags. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **charlie12345**, shared by @celer.

**Quick start:**

```sh
./scripts/build-rdna2.sh
# then serve a Q4_0_ROCMFP4 GGUF with an MTP draft model

```

**Known issues:** none recorded.

## Evidence

No benchmark records yet. Run [BetterBench](betterbench.md) and submit the result.

## Links

[Repository](https://github.com/charlie12345/rocmfp4-llama) · [Record](../../catalog/projects/rocmfp4-llama.yaml)
