<!-- Copy to cards/NNN-<model>-<quant>-tp<N>.md. Replace every <...>. Leave unmeasured values as `TBD (Day's run)`. -->

# Card NNN: <model> <quant>, <engine> TP=<N>

Measured by Day on day-vault.

| Field | Value |
|-------|-------|
| Model | `<org/repo>` ([Hugging Face](https://huggingface.co/<org/repo>)) |
| Model license | <license from the HF repo> |
| Architecture | <architectures from config.json> |
| Quant | <BF16 / FP8 / AWQ INT4 / ...> (checkpoint: `<org/repo>`) |
| Engine | <vLLM / SGLang> |
| Engine version | <exact version, from `vllm_version.txt` or `python -c "import sglang;print(sglang.__version__)"`> |
| TP / PP | TP=<N>, PP=<M> |
| GPUs used | <CUDA_VISIBLE_DEVICES> |
| Context length (served) | <--max-model-len / --context-length> |
| Measured by | Day on day-vault ([hardware.md](../hardware.md)) |
| Date measured | TBD (Day's run) |
| Raw results | `<path to summary.json>` |

## Launch command

```bash
<exact command, copy-pasteable, no placeholders except the model path if local>
```

## Key flags and why

| Flag | Why |
|------|-----|
| `<flag>` | <what it does and the error or slowdown it prevents> |

## Results

Bench: `<bench command or script>`. Definitions are in the [README](../README.md#how-the-numbers-are-taken).

| Test | Input / output tokens | Concurrency | Prefill tok/s | Decode tok/s | Output tok/s (total) | TTFT mean (ms) | TPOT mean (ms) |
|------|-----------------------|-------------|---------------|--------------|----------------------|----------------|----------------|
| <name> | <in> / <out> | <c> | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) |

## VRAM and power

| GPU | VRAM max (MiB) | Power mean (W) | Power max (W) |
|-----|----------------|----------------|---------------|
| <i> | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) |

KV cache size reported at startup (`GPU KV cache size: ... tokens` in the server log): TBD (Day's run).

## Gotchas

- <errors hit and the fix, only things that actually happened on the run>

## Verified vs not verified

- <which repo names, flags and versions were checked against official docs, and which were not>
