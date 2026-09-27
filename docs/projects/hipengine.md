<!-- GENERATED from catalog/projects/hipengine.yaml by scripts/build.py — do not edit. -->

# shisa-ai/hipEngine

**From-scratch RX 7900 XTX inference engine with ~5.7x near-lossless KV compression and MTP.**

**Use it if:** You have an RX 7900 XTX and want maximum context (up to 232K at Q4_K_M) from a single card.

| Field | Value |
|---|---|
| Status | `unverified` — Submitted but not yet reproduced by a maintainer or community volunteer. |
| Verification | `author_reported` — The author published the setup and results; not independently reproduced. |
| Kind | A from-scratch inference engine. |
| Hardware | RDNA3 (gfx1100); tested on Radeon RX 7900 XTX |
| Software | _not yet documented_ |
| Runtime | custom engine |
| Models tested | _not yet documented_ |
| Quantization | gguf_q4_k_m |
| Provides | `kv_compression`, `mtp`, `speculative_decoding`, `long_context` |
| Topology | single_gpu |
| Not suitable for | GPUs outside RDNA3 (e.g. RDNA2, RDNA3.5, RDNA4) |
| Audience | `developer` — Comfortable building runtimes from source and applying patches. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **lhl**.

**Quick start:**

Follow the [repository README](https://github.com/shisa-ai/hipEngine) — no pinned commands recorded yet.

**Known issues:** none recorded.

**Notes:** v0.5.0 adds DMS KV compression (author reports 100% top-1, 0.001 KLD). Shared in #rx7900.

## Evidence

No benchmark records yet. Run [BetterBench](betterbench.md) and submit the result.

## Links

[Repository](https://github.com/shisa-ai/hipEngine) · [Record](../../catalog/projects/hipengine.yaml)
