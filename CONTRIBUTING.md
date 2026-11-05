<!-- PRIVATE / INTERNAL DRAFT. Going public still needs Day's explicit yes. -->

# Contributing a card

One card = one model + one quant + one engine + one GPU layout. Card 001 is Flash 6.05 on 8 cards. Card 002 is Qwen 27B Q8, with the speed row at 4 cards and the HumanEval+ row at 8 cards called out separately. Do not put a second model on an active card.

## Rules

1. **Measured, not estimated.** Every number comes from a run on the rig named in the card. If the cited protocol did not measure a field, write `not measured in this protocol`. Do not fill it from a model card, a blog, another rig, or a different metric. `median_decode_tokens_per_s` is not a stand-in for end-to-end per-user tok/s.
2. **Exact command, or say it is missing.** The launch command must be the one that produced the numbers. If the protocol files do not contain it, say that. Do not write a plausible command and present it as the measured one. Unverified flags are omitted or marked unverified.
3. **Every recorded non-default flag gets a reason.** Say what it does and what breaks without it. If no flags were recorded, write that.
4. **Record versions.** Engine version, driver, and the checkpoint repo name, or `not recorded in this protocol` when the files are silent.
5. **Keep raw results.** Link the SUMMARY and the results JSON for the protocol the card cites.
6. **Say what you could not verify.** Each card ends with a "Verified vs not verified" list.
7. **No client names.** Cards never mention who asked for a config or where it is used.
8. **Plain style.** Short sentences, no hype, no em dashes.
9. **Stay private.** Do not publish the repo. Going public still needs Day's explicit yes.

## File naming

`cards/NNN-<model-slug>-<quant>-<layout>.md`

Examples: `cards/001-qwen3.8-flash-6.05-exl3-8gpu.md`, `cards/002-qwen3.8-27b-q8-llamacpp-mtp-4gpu.md`.

Use the card count when the protocol reports cards and does not name TP.

## Required fields

Start from [cards/_TEMPLATE.md](cards/_TEMPLATE.md). Required:

- Model (name the protocol uses; link a checkpoint repo only when the protocol or the card's own run names it)
- Model license, architecture
- Quant and checkpoint repo, or an explicit note that the repo was not recorded
- Engine and exact version (EXL3, llama.cpp, vLLM, SGLang, or whatever was run)
- TP / PP when known, otherwise the card count the protocol reports
- Launch command, or a clear statement that it was not recorded
- Key flags and why
- Context length served, or `not recorded in this protocol`
- The metrics the protocol actually measured, with the concurrency they were taken at
- TTFT when the protocol recorded it, in the unit the protocol used
- VRAM per GPU and power per GPU, or `not measured in this protocol`
- Date measured
- `Measured by Day on day-vault` (or the rig that measured it, with its own hardware file)

## Checks before a PR

```bash
python3 scripts/check_cards.py   # every card has the required fields and no em dashes
```
