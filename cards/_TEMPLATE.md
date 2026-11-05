<!-- Copy to cards/NNN-<model>-<quant>-<layout>.md. Replace every <...>. Leave unmeasured values as `TBD (Day's run)`. -->

# Card NNN: <model> <quant>, <engine>, <layout>

Measured by Day on day-vault.

| Field | Value |
|-------|-------|
| Model | `<org/repo>` ([Hugging Face](https://huggingface.co/<org/repo>)) |
| Model license | <license from the HF repo> |
| Architecture | <architectures from config.json> |
| Quant | <BF16 / FP8 / AWQ INT4 / ...> (checkpoint: `<org/repo>`) |
| Engine | <vLLM / SGLang / EXL3 / llama.cpp / ...> |
| Engine version | <exact version from that engine's own version command, or `not recorded in this protocol`> |
| TP / PP | <TP=<N>, PP=<M>, or the card count when the protocol does not name a split> |
| GPUs used | <CUDA_VISIBLE_DEVICES> |
| Context length (served) | <served context, or `not recorded in this protocol`> |
| Measured by | Day on day-vault ([hardware.md](../hardware.md)) |
| Date measured | TBD (Day's run) |
| Raw results | `<path to summary.json>` |

## Launch command

```bash
<exact command that produced the numbers, copy-pasteable, no placeholders except the model path if local>
```

If the protocol did not record the command, do not invent one. Say it was not recorded, and list only the engine, quant, and GPU count the protocol named. A vLLM line is not a stand-in for an EXL3 or llama.cpp run.

## Key flags and why

| Flag | Why |
|------|-----|
| `<flag>` | <what it does and the error or slowdown it prevents> |

## Results

Bench: `<bench command or script>`. Definitions are in the [README](../README.md#how-the-numbers-are-taken).

| Test | Input / output tokens | Concurrency | Prefill tok/s | Decode tok/s | Output tok/s (total) | TTFT mean (ms) | TPOT mean (ms) |
|------|-----------------------|-------------|---------------|--------------|----------------------|----------------|----------------|
| <name> | <in> / <out> | <c> | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) |

If the run used another protocol, replace this table with that protocol's metrics. Write `not measured in this protocol` for columns it did not record. Do not relabel end-to-end per-user tok/s as decode tok/s, and do not report `median_decode_tokens_per_s` as the user-facing speed.

## VRAM and power

| GPU | VRAM max (MiB) | Power mean (W) | Power max (W) |
|-----|----------------|----------------|---------------|
| <i> | TBD (Day's run) | TBD (Day's run) | TBD (Day's run) |

KV cache size reported at startup (`GPU KV cache size: ... tokens` in the server log): TBD (Day's run).

## Gotchas

- <errors hit and the fix, only things that actually happened on the run>

## Verified vs not verified

- <which repo names, flags and versions were checked against official docs, and which were not>
