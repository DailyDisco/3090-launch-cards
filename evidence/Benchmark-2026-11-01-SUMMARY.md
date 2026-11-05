# Benchmark — 1 November 2026

Three suites on day-vault, 8x RTX 3090, 160 W caps, unlock off. **This is a
different protocol from the October tables** (see the last section). Do not compare
these figures to Table 1 in `Benchmark-2026-10-28/SUMMARY.md`; the metrics are not the same.

- `REPORT.pdf` — the same content, formatted for reading.
- `results.json` — every number below, machine-readable.
- `evidence/` — the source summaries the numbers were taken from.

## 1. Quality — HumanEval+ (158 problems)

Official tests plus one assertion per extra input, about 122,000 checks. Thinking on,
greedy, one sample, thinking capped at 16k, answer budget 65k, eight cards. The official
solutions score 158/158 against this set, so the harness is sound.

| Model | Engine | Passed | Wrong |
|---|---|---|---|
| Qwen 27B Uncensored Q8 | llama.cpp + MTP | 150 | 8 |
| Qwen 27B Q8 | llama.cpp + MTP | 149 | 9 |
| GLM 5.3 Flash | EXL3 + MTP | 147 | 11* |
| Qwen Flash 4.05 | EXL3 + MTP | 147 | 11 |
| DeepSeek V4.1 Flash | Maya | 147 | 11 |
| Qwen Flash 6.05 | EXL3 + MTP | 145 | 13* |

\* Non-passes, itemised: one GLM sample timed out inside the grader sandbox; one Flash 6.05
answer came back empty. Wrong counts for other rows are ordinary wrong answers. Every row
was regraded from its saved samples three times or more and reproduces exactly; the grade
JSONs, including the GLM regrade runs, are archived in `evidence/quality/grades/`.

Five problems separate the top six configurations. Quality is not the deciding variable here.

An earlier pass scored the 27B rows at 143–147 because they ran with an 8k answer budget and
were cut off mid-answer on 8–11 problems. Those figures are superseded by the table above.

## 2. Throughput — 1, 4, 8, 16 clients

2,400-token prompts, 256-token answers, 90-second window. These are **end-to-end output
tokens per second per user**, including prefill and queue wait.

| Configuration | Cards | 1 | 4 | 8 | 16 | Peak total |
|---|---|---|---|---|---|---|
| Flash 6.05, EXL3 | 8 | 57 | 10.0 | 6.0 | 2.8 | 57 |
| Flash 6.05, EXL3 | 6 | 57 | 11.4 | 6.0 | 2.8 | 57 |
| Flash Uncensored IQ4_XS | 6 | 51 | 19.9 | 10.0 | 5.0 | 80 |
| Flash 6.05, Strata Q8 | 8 | 43 | 10.7 | 5.3 | 2.7 | 43 |
| Flash 6.05, Maya | 8 | 34 | 9.2 | 4.6 | 2.3 | 37 |
| GLM 5.3, EXL3 + MTP | 8 | 48 | 7.8 | 3.2 | 2.1 | 48 |
| GLM 5.3, Maya | 8 | 26 | 10.7 | 4.6 | 2.7 | 43 |
| DeepSeek V4.1, Strata | 8 | 28 | 7.1 | 3.6 | 1.8 | 28 |
| DeepSeek V4.1, Maya | 8 | 23 | 5.7 | 2.8 | 1.4 | 23 |
| Qwen 27B Q8 | 4 | 43 | 17.1 | 8.5 | 4.3 | 68 |
| Qwen 27B Q8 | 2 | 28 | 12.8 | 7.1 | 3.6 | 57 |
| Qwen 27B Uncensored Q8 | 4 | 40 | 17.1 | 8.5 | 4.3 | 68 |

**Metric warning.** The raw probe also records `median_decode_tokens_per_s`. That field
measures the decode phase only and excludes queue time; it reads far higher (for example
103 tokens/s at 16 clients) and does not describe what a user experiences. Every number in
this document uses the aggregate/per-user fields instead.

## 3. Long sessions — cold 20k to 175k

Unique prompt per session, so nothing is served from cache. Time to first token is the
figure that decides whether a session feels usable.

| Lane | Sessions | Context | First token | After that |
|---|---|---|---|---|
| Flash 6.05, 6 cards | 1 | 175k | 120 s | 139 tok/s |
| Flash 6.05, 6 cards | 2 | 175k | 241 s | 92 tok/s |
| Flash 6.05, 6 cards | 2 | 130k | 178 s | 56 tok/s |
| Flash 6.05, 6 cards | 4 | 130k | 268 s | 18 tok/s |
| Flash 6.05, 6 cards | 4 | 50k | 131 s | 23 tok/s |
| Flash 6.05, 6 cards | 4 | 20k | 50 s | 16 tok/s |
| Qwen 27B Q8, 2 cards | 1 | 130k | 255 s | 32 tok/s |
| Qwen 27B Q8, 2 cards | 2 | 65k | 193 s | 13 tok/s |
| Qwen 27B Q8, 2 cards | 2 | 50k | 138 s | 11 tok/s |
| Qwen 27B Q8, 2 cards | 4 | 20k | 97 s | 1.8 tok/s |

Flash prefills at a ceiling of about 1,450 tokens a second regardless of how many sessions
are open, so concurrent giant sessions queue behind each other. The 27B on two cards
prefills roughly three times slower and cannot be configured above 131k at all.

## 4. Prefix cache

| Request | Prompt tokens | Cached | Time |
|---|---|---|---|
| Cold, 130k | 130,022 | 0 | 86.9 s |
| Same prompt again | 130,022 | 129,792 | 0.4 s |
| Different 130k prompt | 129,330 | 0 | 87.4 s |

A continuing conversation is nearly free to re-send; only the new turn is prefilled. The
multi-minute waits above are the cost of starting a session or reopening an evicted one.
Flash carries 393k tokens of cache for a 262k context, which is why two 130k sessions
coexist and four thrash.

## How this differs from the October snapshots

`Benchmark-2026-10-28` reports Chat / Agent / Busy workloads with tok/s per watt, measured
by `openai_probe`. This snapshot reports HumanEval+ pass counts, sweep levels at fixed
client counts, and session-size prefill. The two protocols are not interchangeable, and
none of the figures here should be merged into Table 1.

## Known gaps

- Multi-turn cache behaviour under eviction, when sessions outnumber the cache.
- GLM and DeepSeek cannot be tested above 65k: their servers are configured at 67,584.
- GLM on Strata: no model pack exists.
- Quality rests on one 158-problem suite, which separates these models by only a few points.
