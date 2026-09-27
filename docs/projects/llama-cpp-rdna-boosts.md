<!-- GENERATED from catalog/projects/llama-cpp-rdna-boosts.yaml by scripts/build.py — do not edit. -->

# stew675/llama-cpp-rdna-boosts

**llama.cpp performance patches for RDNA3 — the biggest prompt-processing uplift many 7900 XTX owners saw.**

**Use it if:** You run llama.cpp on an RDNA3 card and want faster prompt processing without switching runtimes.

| Field | Value |
|---|---|
| Status | `unverified` — Submitted but not yet reproduced by a maintainer or community volunteer. |
| Verification | `unverified` — Nobody outside the author has confirmed the setup or its numbers. |
| Kind | Patches applied on top of an existing runtime. |
| Hardware | RDNA3 (gfx1100); tested on Radeon RX 7900 XTX |
| Software | _not yet documented_ |
| Runtime | llama.cpp |
| Models tested | _not yet documented_ |
| Quantization | — |
| Provides | `custom_kernels`, `openai_api` |
| Topology | — |
| Not suitable for | GPUs outside RDNA3 (e.g. RDNA2, RDNA3.5, RDNA4) |
| Audience | `operator` — Comfortable with Docker, drivers and launch flags. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **stew675**.

**Quick start:**

Follow the [repository README](https://github.com/stew675/llama-cpp-rdna-boosts) — no pinned commands recorded yet.

**Known issues:** none recorded.

**Notes:** Also live as the rdna-boosts branch of stew675/llama.cpp. Members report a few hundred t/s of extra prompt processing (no normalized record yet).

## Evidence

No benchmark records yet. Run [BetterBench](betterbench.md) and submit the result.

## Links

[Repository](https://github.com/stew675/llama-cpp-rdna-boosts) · [Mirror](https://github.com/stew675/llama.cpp/tree/rdna-boosts) · [Record](../../catalog/projects/llama-cpp-rdna-boosts.yaml)
