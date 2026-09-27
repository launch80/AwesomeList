<!-- GENERATED from catalog/projects/dual-r9700-vllm-proxmox.yaml by scripts/build.py — do not edit. -->

# bkvargyas/dual-r9700-vllm-proxmox

**2× R9700 on Proxmox with PCI passthrough and P2P on EPYC, with RCCL patches and benchmarks.**

**Use it if:** You are building a dual-R9700 server under Proxmox and need working P2P inside the VM.

| Field | Value |
|---|---|
| Status | `unverified` — Submitted but not yet reproduced by a maintainer or community volunteer. |
| Verification | `author_reported` — The author published the setup and results; not independently reproduced. |
| Kind | Host/platform configuration (virtualization, P2P, topology). |
| Hardware | RDNA4 (gfx1201); tested on Radeon AI PRO R9700; 2+ GPUs required |
| Software | proxmox |
| Runtime | vLLM |
| Models tested | _not yet documented_ |
| Quantization | — |
| Provides | `p2p`, `openai_api`, `tensor_parallel` |
| Topology | dual_gpu_p2p |
| Not suitable for | GPUs outside RDNA4 (e.g. RDNA2, RDNA3, RDNA3.5); Fewer than 2 GPUs |
| Audience | `developer` — Comfortable building runtimes from source and applying patches. |
| Last verified | never |
| Last commit checked | — |
| Listed since | 2026-09-24 |

Built by **bkvargyas**.

**Host:** EPYC host.

**Quick start:**

Follow the [repository README](https://github.com/bkvargyas/dual-r9700-vllm-proxmox) — no pinned commands recorded yet.

**Known issues:** none recorded.

**Notes:** Includes RCCL patches that fix P2P bugs and full benchmark results (not yet normalized into benchmark records).

## Evidence

No benchmark records yet. Run [BetterBench](betterbench.md) and submit the result.

## Links

[Repository](https://github.com/bkvargyas/dual-r9700-vllm-proxmox) · [Record](../../catalog/projects/dual-r9700-vllm-proxmox.yaml)
