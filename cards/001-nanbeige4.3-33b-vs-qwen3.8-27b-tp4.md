<!-- PRIVATE / INTERNAL DRAFT. Every number is TBD until Day runs scripts/card-001-nanbeige-vs-qwen-tp4.sh. -->

# Card 001: Nanbeige4.3-33B vs Qwen3.8-27B, BF16, vLLM TP=4

Same engine, same settings, same 4 cards. Which 30B-class model is faster on 3090s over PCIe?

Measured by Day on day-vault. Status: command ready, every number TBD.

| Field | Nanbeige4.3-33B | Qwen3.8-27B |
|-------|-----------------|-------------|
| Model | [`Nanbeige/Nanbeige4.3-33B`](https://huggingface.co/Nanbeige/Nanbeige4.3-33B) | [`Qwen/Qwen3.8-27B`](https://huggingface.co/Qwen/Qwen3.8-27B) |
| Model license | Apache-2.0 | Apache-2.0 |
| Architecture | `LlamaForCausalLM`, dense, 52 layers, 56 attn heads / 8 KV heads, head_dim 128 | `Qwen3_5ForConditionalGeneration`, dense hybrid: 48 linear-attention (Gated DeltaNet) + 16 full-attention layers, 24 attn heads / 4 KV heads, head_dim 256, vision tower, MTP head |
| Parameters (BF16, from HF safetensors index) | 33,118,977,024 | 27,781,427,952 (includes vision tower) |
| Quant | BF16 (official checkpoint) | BF16 (official checkpoint) |
| Native context | 524,288 | 262,144 |
| Engine | vLLM | vLLM |
| Engine version | 0.32.0 (exact build: TBD, from `vllm_version.txt`) | same |
| TP / PP | TP=4, PP=1 | TP=4, PP=1 |
| GPUs used | 0,1,2,3 | 0,1,2,3 |
| Context length (served) | 65,536 | 65,536 |
| Measured by | Day on day-vault ([hardware.md](../hardware.md)) | same |
| Date measured | TBD (Day's run) | TBD (Day's run) |
| Raw results | `~/bench/nanbeige-vs-qwen-tp4-<ts>/summary.json` (TBD) | same |

Arithmetic, not measurement: BF16 weights are about 66.2 GB (Nanbeige) and 55.6 GB (Qwen) in total, so roughly 16.6 GB and 13.9 GB per GPU at TP=4 before KV cache and CUDA graphs. Both head counts divide evenly by 4 (Nanbeige 56/8, Qwen 24/4 attention and 16/48 linear-attention heads), so TP=4 is a valid split for both.

## Launch command

Run once per model (the script does both, one after the other):

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3
vllm serve Nanbeige/Nanbeige4.3-33B --tensor-parallel-size 4 --dtype bfloat16 --max-model-len 65536 \
  --gpu-memory-utilization 0.92 --port 8000
```

```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3
vllm serve Qwen/Qwen3.8-27B --tensor-parallel-size 4 --dtype bfloat16 --max-model-len 65536 \
  --gpu-memory-utilization 0.92 --port 8000
```

Full one-paste benchmark: [scripts/card-001-nanbeige-vs-qwen-tp4.sh](../scripts/card-001-nanbeige-vs-qwen-tp4.sh) (about 30 to 60 min including downloads).

## Key flags and why

| Flag | Why |
|------|-----|
| `CUDA_VISIBLE_DEVICES=0,1,2,3` | Pins the run to the first four cards so the other four stay free and results are repeatable. Which of these share the bifurcated slot: TBD (see `gpus.csv`). |
| `--tensor-parallel-size 4` | Splits each layer across 4 cards. A 33B BF16 model does not fit on fewer than 3 x 24 GB, and TP must divide the head counts, so 4 is the smallest clean split. |
| `--dtype bfloat16` | Both checkpoints ship in BF16. Ampere (sm86) supports BF16 natively, so no conversion. |
| `--max-model-len 65536` | Caps context so the KV cache fits next to the weights. Without it vLLM tries the native 512K (Nanbeige) or 262K (Qwen) and can refuse to start because the KV cache cannot hold one full-length request. 64K covers the 32K tests with room to spare. |
| `--gpu-memory-utilization 0.92` | Share of each card's 24 GB vLLM may use for weights + KV. Leaves about 2 GB per card for CUDA graphs, NCCL buffers and the display/driver. |
| `--port 8000` | Fixed port the bench client and health check use. |

Flags deliberately left off for this card (kept identical across both models for a fair comparison):

- `--reasoning-parser qwen3`, `--enable-auto-tool-choice --tool-call-parser qwen3_coder`: both official model cards use these for chat and tools. They do not change speed on a random-token bench with `--ignore-eos`, so they are omitted here. Add them for real use.
- `--speculative-config '{"method":"mtp","num_speculative_tokens":3}'` (Qwen MTP head): would make Qwen faster but Nanbeige has no MTP head, so it would not be like-for-like. Candidate for a separate card.
- `--language-model-only` (Qwen): skips the vision tower and frees VRAM for KV cache. Left off so Qwen runs as shipped. Candidate for a separate card.
- `--kv-cache-dtype fp8`: not used on Ampere for this card. Whether it helps on 3090s: not verified.
- `--disable-custom-all-reduce`: exists in vLLM; only needed if the server hangs or errors at all-reduce over PCIe without P2P. Not needed unless the run fails.

## Results

Bench: `vllm bench serve --dataset-name random --ignore-eos --percentile-metrics ttft,tpot,itl`. Definitions in the [README](../README.md#how-the-numbers-are-taken). Prefill tok/s = input tokens / mean TTFT, so it includes queueing.

### Nanbeige4.3-33B

| Test | Input / output tokens | Concurrency | Prompts | Prefill tok/s | Decode tok/s (single stream) | Output tok/s (total) | TTFT mean (ms) | TPOT mean (ms) |
|------|-----------------------|-------------|---------|---------------|------------------------------|----------------------|----------------|----------------|
| prefill8k | 8192 / 1 | 1 | 8 | TBD (Day's run) | n/a | TBD (Day's run) | TBD (Day's run) | n/a |
| prefill32k | 32768 / 1 | 1 | 4 | TBD (Day's run) | n/a | TBD (Day's run) | TBD (Day's run) | n/a |
| decode8k | 8192 / 512 | 1 | 4 | n/a | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) |
| decode32k | 32768 / 512 | 1 | 4 | n/a | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) |
| conc4_4k | 4096 / 512 | 4 | 32 | n/a | n/a | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) |

### Qwen3.8-27B

| Test | Input / output tokens | Concurrency | Prompts | Prefill tok/s | Decode tok/s (single stream) | Output tok/s (total) | TTFT mean (ms) | TPOT mean (ms) |
|------|-----------------------|-------------|---------|---------------|------------------------------|----------------------|----------------|----------------|
| prefill8k | 8192 / 1 | 1 | 8 | TBD (Day's run) | n/a | TBD (Day's run) | TBD (Day's run) | n/a |
| prefill32k | 32768 / 1 | 1 | 4 | TBD (Day's run) | n/a | TBD (Day's run) | TBD (Day's run) | n/a |
| decode8k | 8192 / 512 | 1 | 4 | n/a | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) |
| decode32k | 32768 / 512 | 1 | 4 | n/a | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) |
| conc4_4k | 4096 / 512 | 4 | 32 | n/a | n/a | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) |

## VRAM and power

Sampled every 500 ms with `nvidia-smi` while each server was up (includes idle time between tests). Cards capped at 160 W.

| GPU | Nanbeige VRAM max (MiB) | Nanbeige power mean / max (W) | Qwen VRAM max (MiB) | Qwen power mean / max (W) |
|-----|-------------------------|-------------------------------|---------------------|---------------------------|
| 0 | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) |
| 1 | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) |
| 2 | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) |
| 3 | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) |

KV cache size at startup (`GPU KV cache size` line in `<model>-server.log`): Nanbeige TBD (Day's run), Qwen TBD (Day's run).

PCIe gen / width per card (from `gpus.csv`): TBD (Day's run).

## Gotchas

- None recorded yet. Fill in only what actually happens on the run.

## Verified vs not verified

Verified (Oct 28, 2026):

- `Nanbeige/Nanbeige4.3-33B` exists on Hugging Face (created Oct 24, 2026), Apache-2.0, `LlamaForCausalLM`, BF16, 524,288 native context. Its model card gives a vLLM command with `--tensor-parallel-size 4 --gpu-memory-utilization 0.8 --enable-auto-tool-choice --reasoning-parser qwen3 --tool-call-parser qwen3_coder`, and an SGLang command with `--tp-size 4 --mem-fraction-static 0.8`.
- `Qwen/Qwen3.8-27B` exists on Hugging Face, Apache-2.0, `Qwen3_5ForConditionalGeneration`, BF16, 262,144 native context. The official vLLM recipe (recipes.vllm.ai/Qwen/Qwen3.8-27B) lists vLLM 0.17.0+ and `transformers>=5.8.0`, plus the MTP `--speculative-config`, `--language-model-only` and `--kv-cache-dtype fp8` flags.
- vLLM 0.32.0 is the current PyPI release (Oct 18, 2026). `--max-model-len`, `--gpu-memory-utilization`, `--disable-custom-all-reduce`, `--kv-cache-dtype`, `--language-model-only`, `--speculative-config` appear in vLLM's engine-args docs.
- Head counts and parameter counts above come from each repo's `config.json` and safetensors metadata.

Not verified:

- That either model actually loads and runs under vLLM 0.32.0 on sm86 (3090). No recipe or model card shows a 3090 or Ampere run. This card's run is the test.
- Nanbeige's model card loads the tokenizer with `trust_remote_code=True, use_fast=False` in Transformers. The repo has no custom Python files, so vLLM should not need `--trust-remote-code`, but this is unconfirmed until the server starts.
- Whether the installed `transformers` on day-vault is 5.8.0 or newer, which the vLLM recipe lists for Qwen3.8's processor. If the Qwen server fails at startup, check this first.
- Whether `--kv-cache-dtype fp8` works or helps on Ampere.
- Which GPU indices sit on the bifurcated slot.
