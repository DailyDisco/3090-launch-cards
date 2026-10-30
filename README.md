<!-- PRIVATE / INTERNAL DRAFT. Not published. No GitHub repo exists yet. Do not share until Day says yes. -->

# 8x 3090 launch cards

Copy-paste vLLM and SGLang launch commands for new open models on consumer RTX 3090s over PCIe (no NVLink), at 2, 4 and 8 cards.

Every card has:

- the exact launch command,
- the flags that matter and the problem each one prevents,
- numbers measured by Day on one real rig (day-vault, see [hardware.md](hardware.md)).

No number on a card is estimated. If a field says `TBD (Day's run)`, it has not been measured yet.

## Cards

| # | Card | Engine | TP | Status |
|---|------|--------|----|--------|
| 1 | [Nanbeige4.3-33B vs Qwen3.8-27B, BF16](cards/001-nanbeige4.3-33b-vs-qwen3.8-27b-tp4.md) | vLLM 0.32.0 | 4 | command ready, numbers TBD |

New card? Copy [cards/_TEMPLATE.md](cards/_TEMPLATE.md). Format rules are in [CONTRIBUTING.md](CONTRIBUTING.md).

## How the numbers are taken

- [scripts/card-001-nanbeige-vs-qwen-tp4.sh](scripts/card-001-nanbeige-vs-qwen-tp4.sh): the one-paste run for card 1. It starts each server, runs `vllm bench serve` (random data, `--ignore-eos`), logs power and VRAM every 500 ms, and writes `summary.json`.
- [scripts/bench.py](scripts/bench.py): a small engine-agnostic stub for future cards. It works against any OpenAI-compatible server (vLLM, SGLang) and records tok/s, TTFT, VRAM and power to JSON.

Definitions used on every card:

- **Prefill tok/s** = input tokens / mean TTFT. Includes queueing, so treat it as a floor.
- **Decode tok/s (single stream)** = 1000 / mean TPOT, one request in flight.
- **Output tok/s at concurrency N** = total output tokens / wall time with N requests in flight.
- **Power** = `nvidia-smi power.draw` per GPU, sampled every 500 ms. All cards are capped at 160 W.

## What this is not

- Not a leaderboard. One rig, one set of settings, dated.
- Not quality evals. Speed and fit only.

## License

MIT, see [LICENSE](LICENSE). Model weights keep their own licenses (listed per card).

A paid pack with more models and tuned configs is planned. See [PAID_PACK.md](PAID_PACK.md) (internal).
