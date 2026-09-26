<base target="_blank">

<h1 align="center">
<b>Awesome Launch80 List</b> <img src="https://awesome.re/badge-flat.svg"/></h1>

<p>
A community-compiled index of open-source repositories (2+ stars) built and shared by members of the
<a href="https://discord.gg/launch80">Launch80 Discord</a>.
</p>

<p>
<i>Every repo below was posted to the Launch80 Discord by (or on behalf of) the person who owns it —
shared to help the broader community make progress. Entries credit the builder and the Discord
member who shared it.</i>
</p>

## Index

[Inference Servers & Forks](#inference-servers--forks) ⁕ [vLLM / Radiance Ecosystem](#vllm--radiance-ecosystem) ⁕ [Kernel & Performance Libraries](#kernel--performance-libraries) ⁕ [Launchers & Deployment Recipes](#launchers--deployment-recipes) ⁕ [Multi-GPU & Platform Setups](#multi-gpu--platform-setups) ⁕ [Benchmarks & Evaluation](#benchmarks--evaluation) ⁕ [Monitoring & Tooling](#monitoring--tooling) ⁕ [Agent Harnesses & Dev Tools](#agent-harnesses--dev-tools) ⁕ [Other Community Projects](#other-community-projects) ⁕ [Related Codeberg Work](#related-codeberg-work)

---

## Inference Servers & Forks

Community-owned forks and from-scratch engines, grouped by hardware. Only repos with more than
one star are listed — star counts verified 2026-09-24.

### Radeon AI PRO R9700 / RDNA4 (gfx1201)

- [magiccodingman/vllm-radiance](https://github.com/magiccodingman/vllm-radiance) - Experimental fork of the vLLM Radiance stack, rebased onto current vLLM main with AMD PyTorch 2.12 / Triton 3.7.1 / AITER 0.1.20 / ROCm 7.14, preserving R9700-specific Radiance paths, with DFlash2 and MXFP4 work merged in. Built by **slurp** (also mirrored on GitLab).
- [Capicua25x/vllm-rocm-rdna4](https://github.com/Capicua25x/vllm-rocm-rdna4) - RDNA4 fork of vLLM that unlocks large gains on 2× RX 9070 XT (and R9700-class) cards — e.g. Qwen 3.8 27B MXFP4 @ 200K context with MTP, ~50 t/s single-job and up to ~140 t/s batched. Built by **capicua25x**, shared by @Darkmoon.

### Radeon RX 7900 / RDNA3 (gfx1100)

- [shisa-ai/hipEngine](https://github.com/shisa-ai/hipEngine) - From-scratch inference engine for the RX 7900 XTX; v0.5.0 adds DMS with ~5.7x near-lossless KV compression (100% top-1, 0.001 KLD), fits up to 232K context at Q4_K_M, with MTP support. Built by **lhl**, shared in #rx7900.
- [stew675/llama-cpp-rdna-boosts](https://github.com/stew675/llama-cpp-rdna-boosts) - llama.cpp performance patches for RDNA3 (also live as the `rdna-boosts` branch of [stew675/llama.cpp](https://github.com/stew675/llama.cpp/tree/rdna-boosts)); the best uplift many members saw on 7900 XTX, including a few hundred t/s of extra prompt-processing speed. Built by **stew675**.
- [mkadrlik/vllm-radiance-p2p](https://github.com/mkadrlik/vllm-radiance-p2p) - vLLM Radiance adapted for 2× RX 7900 with P2P; ~53 t/s on an AWQ Qwen3.8-27B across the pair. Built by **Froz**.

### Radeon Pro V620 / RDNA2 (gfx1030)

- [charlie12345/rocmfp4-llama](https://github.com/charlie12345/rocmfp4-llama) - llama.cpp with ROCmFP4 support for RDNA2/Strix; the recipe members use on V620 (build with `scripts/build-rdna2.sh`, pair with Q4_0_ROCMFP4 GGUFs + MTP draft). Built by **charlie12345**, shared by @celer.
- [opengfx1030/vllm-rdna](https://github.com/opengfx1030/vllm-rdna) - WIP fork merging community vLLM RDNA2 work (including leapdragon's) into a shared gfx1030 community org repo. Built by **BlivionIaG**.
- [leapdragon/vllm-rdna2-qwen](https://github.com/leapdragon/vllm-rdna2-qwen) - vLLM fork for 4× V620; ~70 t/s with MTP=3 on Qwen3.8-Flash-Next W4A16 on a Zen 2 EPYC / PCIe Gen4 platform. Built by **leapdragon**, shared by @Schimazing.
- [leapdragon/vllm-rdna2-recipe](https://github.com/leapdragon/vllm-rdna2-recipe) - Deployment recipe for RDNA2 vLLM; received @wsantos's fix for prefill blocking generation (~150 t/s aggregate across 8 concurrent streams on 4× V620) via PR.

### CDNA datacenter (MI210 / MI100 / MI250X)

- [davetha/mi210-vllm](https://github.com/davetha/mi210-vllm) - vLLM build that pulls in the AITER patches for MI210; includes a full INT8 Qwen3.8-27B recipe (docker run + env vars). Built by **davetha**.
- [curvedinf/int8-vllm](https://github.com/curvedinf/int8-vllm) - INT8-optimized vLLM running Qwen3.8-27B C8 at **972 t/s TG / 5,680 PP on 4× MI100**. Built by **curvedinf** (4× MI100 rig), shared by @mldatascientist. ([Reddit writeup](https://www.reddit.com/r/LocalLLaMA/comments/1vz9hqa/qwen38_27b_c8_at_972_tg_5680_pp_on_4x_mi100_rig/))
- [curvedinf/int8-aiter](https://github.com/curvedinf/int8-aiter) - The INT8 AITER kernels behind the 4× MI100 972 t/s result. Built by **curvedinf**, shared by @mldatascientist.

### Intel Arc

- [davetha/krea2-intel-arc-b580](https://github.com/davetha/krea2-intel-arc-b580) - Krea2 image-model test harness on Intel Arc B580 (not vLLM/llama.cpp, but a useful datapoint for Arc owners). Built by **davetha**.

---

## vLLM / Radiance Ecosystem

- [https://codeberg.org/StillDeadcode/vllm-radiance] - Stilldeadcode Radiance
- [GGZ14/vllm-mxfp4](https://github.com/GGZ14/vllm-mxfp4) - MXFP4 fast path built on top of the Radiance vLLM image with online conversion; R9700s hitting **5,809 tok/s prefill / 276 tok/s decode** on NVFP4 Qwen3.8-27B. Built by **The_Candle_Watcher** (GGZ14). Codeberg mirror: [codeberg.org/ggz14/radiance-vllm-mxfp4](https://codeberg.org/ggz14/radiance-vllm-mxfp4).
- [mattbucci/2x-R9700-RDNA4-GFX1201-sglang-inference](https://github.com/mattbucci/2x-R9700-RDNA4-GFX1201-sglang-inference) - SGLang builds for 2× R9700 (gfx1201); the community's starting point for SGLang on RDNA4. Built by **mattbucci**, shared by @blakelemons.
- [0xSero/deepseek-v4.1-flash-4x-rtx-pro-6000](https://github.com/0xSero/deepseek-v4.1-flash-4x-rtx-pro-6000) - DeepSeek-V4.1-Flash running on 4× RTX Pro 6000 at ~200 t/s TG / 7k PP at 8k context. Built by **0xSero**, shared by @mldatascientist.
- [tonyd2wild/Minimax-M3-NVFP-3x-DGX-Sparks-TP-3](https://github.com/tonyd2wild/Minimax-M3-NVFP-3x-DGX-Sparks-TP-3) - MiniMax-M3 NVFP4 on 3× DGX Spark with TP=3. Shared by @The_Candle_Watcher.

---

## Kernel & Performance Libraries

- [davetha/aiter-cdna2](https://github.com/davetha/aiter-cdna2) - Binary patching of AMD's AITER (AI Tensor Engine for ROCm, officially CDNA3+ only) to unlock fast paths on **CDNA2** — the enabler for much of the MI210 performance work. Built by **davetha**.
- [davetha/vllm-expert-cache](https://github.com/davetha/vllm-expert-cache) - LRU/LFU expert-cache patch for vLLM MoE serving: keeps only the hot experts resident, letting models that would otherwise not fit run on smaller rigs; includes porting docs for Intel. Built by **davetha**.

---

## Launchers & Deployment Recipes

- [zzpanic/qwen3.6-vllm-gfx1201-launchers](https://github.com/zzpanic/qwen3.6-vllm-gfx1201-launchers) - The de-facto standard launcher scripts for single-R9700 vLLM + DFlash2 setups; the most-recommended starting point in #r9700. Built by **zzpanic**.
- [BMorgan1296/qwen3.6-vllm-gfx1201-launchers](https://github.com/BMorgan1296/qwen3.6-vllm-gfx1201-launchers) - Fork of the zzpanic launchers with fixes and DFlash changes contributed in-server. Built by **Bman1296**.
- [malicz/vllm-gfx1201-launchers](https://github.com/malicz/vllm-gfx1201-launchers) - Single-R9700 Radiance + MXFP4 setup with Dockerfile, model-download steps, MTP conversion, and patches (e.g. `patch_dflash_w4a16_kv.py`); ~81 t/s decode / 2,380 prefill on Qwen3.8-27B MXFP4 @ 160K. Built by **malicz** (built on Deadcode's & Brian's work).
- [davetha/mi210-llm-stack](https://github.com/davetha/mi210-llm-stack) - Full MI210 LLM stack documentation, including a model-weight matrix with per-tier serving recommendations. Built by **davetha**, shared by @mldatascientist.

---

## Multi-GPU & Platform Setups

- [bkvargyas/dual-r9700-vllm-proxmox](https://github.com/bkvargyas/dual-r9700-vllm-proxmox) - 2× R9700 on Proxmox with PCI passthrough and P2P on EPYC, including RCCL patches to fix P2P bugs and full benchmark results. Built by **bkvargyas**.
- [mattbucci/2x-R9700-RDNA4-GFX1201-sglang-inference](https://github.com/mattbucci/2x-R9700-RDNA4-GFX1201-sglang-inference) - 2× R9700 SGLang setup (see also [vLLM/Radiance Ecosystem](#vllm--radiance-ecosystem)). Built by **mattbucci**.

---

## Benchmarks & Evaluation

- [GGZ14/BetterBench](https://github.com/GGZ14/BetterBench) - The community's go-to benchmark suite for vLLM/llama.cpp endpoints (incl. a graded code corpus, `--runs N`, `--quick` mode). Built by **The_Candle_Watcher** (GGZ14).
- [Amalia-LLM/pheb](https://github.com/Amalia-LLM/pheb) - Open-source portion of a European-Portuguese legal LLM eval: ~800 questions/workflows graded by lawyers over a 21k-article Portuguese law corpus. Built by **Carlos Rolo**.

---

## Monitoring & Tooling

- [Dyluhn/R9V](https://github.com/Dyluhn/R9V) - GPU monitoring/inspection tool for the R9700 — actively maintained in-server, with regressions tracked and fixed within hours of being reported. Built by **Dyluhn**.
- [BlivionIaG/v620_toolbox](https://github.com/BlivionIaG/v620_toolbox) - Toolbox of scripts and utilities for Radeon Pro V620 boxes. Built by **BlivionIaG**.

---

## Agent Harnesses & Dev Tools

- [cztomsik/clown-circus](https://github.com/cztomsik/clown-circus) - Minimal agent harness where the model writes its own prompts to minimize perplexity and "over-thinking"; includes reasoning-trace inspection. Built by **cztomsik**.
- [Alloyium-ai/alloyium](https://github.com/Alloyium-ai/alloyium) - Real-time communication between agents using existing Claude/ChatGPT subscriptions. Built by **atcsecure**.

---

## Other Community Projects

- [LibreShockwave/LibreShockwave](https://github.com/LibreShockwave/LibreShockwave) - A Ruffle-equivalent for Adobe Shockwave, running old Shockwave content in modern browsers. Built by **Alex** (member).
- [webbrain-one/webbrain](https://github.com/webbrain-one/webbrain) - Community-shared knowledge project mentioned in #hang-out. Shared by @xza.nomad.

---

## Related Codeberg Work

Much of the Launch80 stack lives on Codeberg rather than GitHub — included here for completeness:

- [codeberg.org/StillDeadcode/vllm-radiance](https://codeberg.org/StillDeadcode/vllm-radiance) - The **Radiance** vLLM image for gfx1201 (the base most forks above build on); Docker images at [hub.docker.com/r/stilldeadcode/vllm-radiance](https://hub.docker.com/r/stilldeadcode/vllm-radiance). Built by **Deadcode**.
- [codeberg.org/StillDeadcode/libr4d](https://codeberg.org/StillDeadcode/libr4d) - gfx1201-specialized HIP kernel library (pure HIP, llama.cpp-friendly), community-contributed. Built by **Deadcode** and contributors.
- [codeberg.org/hifi/vllm-radlight](https://codeberg.org/hifi/vllm-radlight) - Lightweight vLLM variant; median decode >70 t/s on a single R9700 with Qwen3.8-27B @ 192K context. Built by **hifi**, with published bench results.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). If you built something and shared it in the Discord, add yourself — or open an issue and we'll add it.

## License

[CC0-1.0](LICENSE) — do whatever you want with the list itself.
