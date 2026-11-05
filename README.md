<!-- PRIVATE / INTERNAL DRAFT. Not published. Going public still needs Day's explicit yes. Do not share until Day says yes. -->

# 8x 3090 launch cards

Measured notes for models on consumer RTX 3090s over PCIe (no NVLink). This repo stays private until Day gives an explicit yes.

Every active card has:

- the configuration the named protocol actually recorded,
- the launch command only when that run recorded one,
- numbers measured by Day on day-vault (see [hardware.md](hardware.md)).

No number on a card is estimated. If the cited protocol did not record a field, the card says so. It does not borrow a number from another row, another date, or another metric.

Nanbeige is not an active card. The Nanbeige vs Qwen draft and `scripts/card-001-nanbeige-vs-qwen-tp4.sh` are removed.

## Cards

| # | Card | Engine (as named in the Nov 1 quality row) | Cards | Status |
|---|------|--------------------------------------------|-------|--------|
| 1 | [Qwen3.8 Flash (Flash 6.05), EXL3 + MTP](cards/001-qwen3.8-flash-6.05-exl3-8gpu.md) | EXL3 + MTP | 8 | Nov 1 numbers filled. Serve command was not in the protocol files. |
| 2 | [Qwen3.8-27B Q8, llama.cpp + MTP](cards/002-qwen3.8-27b-q8-llamacpp-mtp-4gpu.md) | llama.cpp + MTP | 4 on the speed row; HumanEval+ for this checkpoint was 8 cards | Nov 1 numbers filled. Serve command was not in the protocol files. |

New card? Copy [cards/_TEMPLATE.md](cards/_TEMPLATE.md). Format rules are in [CONTRIBUTING.md](CONTRIBUTING.md).

## How the numbers are taken

Active cards cite the 1 November 2026 DayVault protocol, measured by Day on day-vault:

- [evidence/Benchmark-2026-11-01-SUMMARY.md](evidence/Benchmark-2026-11-01-SUMMARY.md)
- [evidence/Benchmark-2026-11-01-results.json](evidence/Benchmark-2026-11-01-results.json)

Throughput in that protocol (SUMMARY section 2): 2,400-token prompts, 256-token answers, 90-second window, at 1, 4, 8, and 16 clients. The figures are **end-to-end output tokens per second per user, including prefill and queue wait**.

They are not `median_decode_tokens_per_s`. That field is decode-only, drops queue time, and reads far higher. The SUMMARY's own example is 103 tokens/s at 16 clients. Do not put that field on a card as the user-facing speed.

The Nov 1 protocol is not comparable to the 28 October 2026 Table 1. The SUMMARY says the metrics are not the same. Do not merge the figures.

Older bench wording (prefill tok/s = input tokens / mean TTFT, decode tok/s = 1000 / mean TPOT, output tok/s = total output tokens / wall time) is not what the Nov 1 cards report. Those columns were not measured in that protocol.

[scripts/bench.py](scripts/bench.py) is a stub for a future OpenAI-compatible server. It did not produce the Nov 1 numbers.

Power cap for the protocol: 160 W per GPU, unlock off. See [hardware.md](hardware.md).

## What this is not

- Not a leaderboard. One rig, one dated protocol.
- Not a published repo. Going public still needs Day's explicit yes.

A paid pack with more models and tuned configs is planned. That writeup is not in this repo.

## License

MIT, see [LICENSE](LICENSE). Model weights keep their own licenses. The Nov 1 files do not record those licenses, so the cards do not invent them.
