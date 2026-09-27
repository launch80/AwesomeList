<!-- GENERATED from catalog/benchmarks/benchmark-results.jsonl by scripts/build.py — do not edit. -->

# Benchmarks

Author-reported numbers, normalized. Tables are sorted by hardware, **not** by speed: a number is
only comparable to another measured with the same mode, context, prompt/output length and
concurrency. **Fields reported** counts how many of the key workload fields the source stated
(`hardware.gpu_count`, `hardware.interconnect`, `hardware.host_cpu`, `platform.os`, `platform.kernel`, `platform.rocm`, `runtime.version`, `runtime.commit`, `model.artifact`, `model.quantization`, `workload.context_length`, `workload.prompt_tokens`, `workload.output_tokens`, `workload.concurrency`, `command`, `measured_on`).

Raw data: [`catalog/benchmarks/benchmark-results.jsonl`](../catalog/benchmarks/benchmark-results.jsonl) ·
schema: [`schemas/benchmark.schema.json`](../schemas/benchmark.schema.json).

## Decode — single stream

One request at a time: what a single user feels.

| Project | GPUs | Model | Quant | Context | Concurrency | Decode tok/s | Runtime | Mode | Fields reported | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| [Capicua25x/vllm-rocm-rdna4](projects/capicua-vllm-rocm-rdna4.md) | 2× Radeon RX 9070 XT | Qwen 3.8 27B MXFP4 | mxfp4 | 200K | 1 | ~50 | vLLM MTP | single_stream | 4/16 | list_entry |

## Decode — batched (aggregate)

Total decode throughput across concurrent requests.

| Project | GPUs | Model | Quant | Context | Concurrency | Decode tok/s | Runtime | Mode | Fields reported | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| [Capicua25x/vllm-rocm-rdna4](projects/capicua-vllm-rocm-rdna4.md) | 2× Radeon RX 9070 XT | Qwen 3.8 27B MXFP4 | mxfp4 | 200K | not reported | ~140 (peak) | vLLM MTP | batched | 3/16 | list_entry |
| [leapdragon/vllm-rdna2-recipe](projects/vllm-rdna2-recipe.md) | 4× Radeon Pro V620 | not reported | — | not reported | 8 | ~150 | vLLM | batched | 2/16 | list_entry |

## Prefill

Prompt-processing speed. Mode is shown per row.

| Project | GPUs | Model | Quant | Context | Concurrency | Prefill tok/s | Runtime | Mode | Fields reported | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| [curvedinf/int8-vllm](projects/int8-vllm.md) | 4× Instinct MI100 | Qwen3.8-27B C8 | int8 | not reported | not reported | 5,680 | vLLM | not_reported | 2/16 | [reddit](https://www.reddit.com/r/LocalLLaMA/comments/1vz9hqa/qwen38_27b_c8_at_972_tg_5680_pp_on_4x_mi100_rig/) |
| [malicz/vllm-gfx1201-launchers](projects/malicz-gfx1201-launchers.md) | 1× Radeon AI PRO R9700 | Qwen3.8-27B MXFP4 | mxfp4 | 160K | not reported | ~2,380 | vLLM | not_reported | 3/16 | list_entry |
| [GGZ14/vllm-mxfp4](projects/vllm-mxfp4.md) | Radeon AI PRO R9700 (count not reported) | Qwen3.8-27B NVFP4 (online MXFP4 conversion) | nvfp4 | not reported | not reported | 5,809 | vLLM | not_reported | 1/16 | list_entry |
| [0xSero/deepseek-v4.1-flash-4x-rtx-pro-6000](projects/deepseek-v41-flash-4x-rtx-pro-6000.md) | 4× RTX Pro 6000 Blackwell | DeepSeek-V4.1-Flash | — | 8K | not reported | ~7,000 | not reported | not_reported | 2/16 | list_entry |

## Decode — concurrency not reported

The source did not say whether this was one stream or many. Do not compare these with the tables above; if you can reproduce one with BetterBench, submit a record with `mode` set.

| Project | GPUs | Model | Quant | Context | Concurrency | Decode tok/s | Runtime | Mode | Fields reported | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| [curvedinf/int8-vllm](projects/int8-vllm.md) | 4× Instinct MI100 | Qwen3.8-27B C8 | int8 | not reported | not reported | 972 | vLLM | not_reported | 2/16 | [reddit](https://www.reddit.com/r/LocalLLaMA/comments/1vz9hqa/qwen38_27b_c8_at_972_tg_5680_pp_on_4x_mi100_rig/) |
| [malicz/vllm-gfx1201-launchers](projects/malicz-gfx1201-launchers.md) | 1× Radeon AI PRO R9700 | Qwen3.8-27B MXFP4 | mxfp4 | 160K | not reported | ~81 | vLLM | not_reported | 3/16 | list_entry |
| [GGZ14/vllm-mxfp4](projects/vllm-mxfp4.md) | Radeon AI PRO R9700 (count not reported) | Qwen3.8-27B NVFP4 (online MXFP4 conversion) | nvfp4 | not reported | not reported | 276 | vLLM | not_reported | 1/16 | list_entry |
| [hifi/vllm-radlight](projects/vllm-radlight.md) | 1× Radeon AI PRO R9700 | Qwen3.8-27B | — | 192K | not reported | ~70 (median) | vLLM | not_reported | 2/16 | list_entry |
| [0xSero/deepseek-v4.1-flash-4x-rtx-pro-6000](projects/deepseek-v41-flash-4x-rtx-pro-6000.md) | 4× RTX Pro 6000 Blackwell | DeepSeek-V4.1-Flash | — | 8K | not reported | ~200 | not reported | not_reported | 2/16 | list_entry |
| [mkadrlik/vllm-radiance-p2p](projects/vllm-radiance-p2p.md) | 2× Radeon RX 7900 (XTX or XT, unspecified) (P2P) | Qwen3.8-27B AWQ | awq | not reported | not reported | ~53 | vLLM | not_reported | 2/16 | list_entry |
| [leapdragon/vllm-rdna2-qwen](projects/vllm-rdna2-qwen.md) | 4× Radeon Pro V620 | Qwen3.8-Flash-Next W4A16 | w4a16 | not reported | not reported | ~70 | vLLM MTP=3 | not_reported | 4/16 | list_entry |
