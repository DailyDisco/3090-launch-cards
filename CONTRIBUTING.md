<!-- PRIVATE / INTERNAL DRAFT -->

# Contributing a card

One card = one model + one quant + one engine + one TP/PP layout. Comparisons of two models under identical settings may share a card (see card 001).

## Rules

1. **Measured, not estimated.** Every number comes from a run on the rig named in the card. If it has not been run, write `TBD (Day's run)`. No numbers from model cards, blog posts or other people's rigs in the Results table.
2. **Exact command.** The launch command must be the one that produced the numbers, copy-pasteable.
3. **Every non-default flag gets a reason.** Say what it does and what breaks without it.
4. **Record versions.** Engine version, driver, and the checkpoint repo name.
5. **Keep raw results.** Link or attach the `summary.json` and the per-test JSON files.
6. **Say what you could not verify.** Each card ends with a "Verified vs not verified" list.
7. **No client names.** Cards never mention who asked for a config or where it is used.
8. **Plain style.** Short sentences, no hype, no em dashes.

## File naming

`cards/NNN-<model-slug>-<quant>-tp<N>.md`, for example `cards/002-qwen3.8-27b-awq-int4-tp2.md`.

## Required fields

Start from [cards/_TEMPLATE.md](cards/_TEMPLATE.md). Required:

- Model (HF repo, linked), model license, architecture
- Quant and checkpoint repo
- Engine and exact version
- TP / PP and which GPUs
- Exact launch command
- Key flags and why
- Context length served
- Prefill and decode tok/s, with the concurrency they were taken at
- TTFT
- VRAM per GPU
- Power per GPU
- Date measured
- `Measured by Day on day-vault` (or the rig that measured it, with its own hardware file)

## Checks before a PR

```bash
python3 scripts/check_cards.py   # every card has the required fields and no em dashes
```
