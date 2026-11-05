#!/usr/bin/env python3
"""Engine-agnostic bench stub (STUB, internal draft).

Hits an OpenAI-compatible server with streaming completions, samples nvidia-smi
every 500 ms, and writes one JSON file with:
  ttft_ms, prefill_tok_s, decode_tok_s, output_tok_s, vram_mib, power_w.

It never invents numbers: if a value cannot be measured it is written as null.
This stub did not produce the 1 November 2026 DayVault cards. Those numbers are
in evidence/Benchmark-2026-11-01-SUMMARY.md and
evidence/Benchmark-2026-11-01-results.json (end-to-end per-user tok/s).

Usage (illustration only, not a measured Nov 1 invocation):
  python3 scripts/bench.py --model <served-model-name> --input-len 8192 --output-len 512 \
      --concurrency 1 --num-prompts 4 --out results/run.json
Stdlib only.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import random
import subprocess
import threading
import time
import urllib.request


def sample_gpus(stop: threading.Event, samples: list[dict], interval_s: float) -> None:
    """Poll nvidia-smi for power and memory until stop is set."""
    cmd = ["nvidia-smi", "--query-gpu=index,power.draw,memory.used",
           "--format=csv,noheader,nounits"]
    while not stop.is_set():
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=5).stdout
            t = time.time()
            for line in out.strip().splitlines():
                i, p, m = (x.strip() for x in line.split(","))
                samples.append({"t": t, "gpu": int(i), "power_w": float(p), "vram_mib": float(m)})
        except (OSError, ValueError, subprocess.SubprocessError):
            pass  # no GPU / no nvidia-smi: leave samples empty, report null
        stop.wait(interval_s)


def make_prompt(n_tokens: int, seed: int) -> str:
    """Rough random prompt. Token count is approximate; server usage is what gets recorded."""
    rng = random.Random(seed)
    words = ["alpha", "bravo", "delta", "omega", "sigma", "kappa", "lambda", "theta"]
    return " ".join(rng.choice(words) for _ in range(n_tokens))


def one_request(base: str, model: str, prompt: str, max_tokens: int) -> dict:
    body = json.dumps({
        "model": model, "prompt": prompt, "max_tokens": max_tokens, "stream": True,
        "ignore_eos": True, "temperature": 0,
        "stream_options": {"include_usage": True},
    }).encode()
    req = urllib.request.Request(f"{base}/v1/completions", data=body,
                                 headers={"Content-Type": "application/json"})
    t0 = time.perf_counter()
    t_first = None
    usage = {}
    with urllib.request.urlopen(req, timeout=3600) as resp:
        for raw in resp:
            line = raw.decode().strip()
            if not line.startswith("data:") or line == "data: [DONE]":
                continue
            chunk = json.loads(line[5:])
            if chunk.get("usage"):
                usage = chunk["usage"]
            if t_first is None and chunk.get("choices") and chunk["choices"][0].get("text"):
                t_first = time.perf_counter()
    t_end = time.perf_counter()
    return {"t0": t0, "t_first": t_first, "t_end": t_end,
            "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens")}


def mean(xs: list[float]) -> float | None:
    return round(sum(xs) / len(xs), 2) if xs else None


def summarize(reqs: list[dict], wall_s: float, gpu: list[dict]) -> dict:
    ttft = [(r["t_first"] - r["t0"]) * 1000 for r in reqs if r["t_first"]]
    prefill = [r["prompt_tokens"] / (r["t_first"] - r["t0"])
               for r in reqs if r["t_first"] and r["prompt_tokens"]]
    decode = [(r["completion_tokens"] - 1) / (r["t_end"] - r["t_first"])
              for r in reqs if r["t_first"] and (r["completion_tokens"] or 0) > 1
              and r["t_end"] > r["t_first"]]
    out_tokens = sum(r["completion_tokens"] or 0 for r in reqs)
    per_gpu: dict[int, dict] = {}
    for s in gpu:
        g = per_gpu.setdefault(s["gpu"], {"power_w": [], "vram_mib": []})
        g["power_w"].append(s["power_w"])
        g["vram_mib"].append(s["vram_mib"])
    return {
        "ttft_ms_mean": mean(ttft),
        "prefill_tok_s_mean": mean(prefill),
        "decode_tok_s_per_stream_mean": mean(decode),
        "output_tok_s_total": round(out_tokens / wall_s, 2) if wall_s > 0 and out_tokens else None,
        "gpus": {i: {"power_w_mean": mean(g["power_w"]), "power_w_max": max(g["power_w"]),
                     "vram_mib_max": max(g["vram_mib"])} for i, g in sorted(per_gpu.items())},
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base-url", default="http://localhost:8000")
    ap.add_argument("--model", required=True)
    ap.add_argument("--input-len", type=int, default=8192)
    ap.add_argument("--output-len", type=int, default=512)
    ap.add_argument("--concurrency", type=int, default=1)
    ap.add_argument("--num-prompts", type=int, default=4)
    ap.add_argument("--sample-ms", type=int, default=500)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    stop, samples = threading.Event(), []
    th = threading.Thread(target=sample_gpus, args=(stop, samples, a.sample_ms / 1000), daemon=True)
    th.start()
    prompts = [make_prompt(a.input_len, i) for i in range(a.num_prompts)]
    t0 = time.perf_counter()
    with cf.ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        reqs = list(ex.map(lambda p: one_request(a.base_url, a.model, p, a.output_len), prompts))
    wall = time.perf_counter() - t0
    stop.set()
    th.join()

    result = {
        "measured_by": "Day on day-vault",
        "date": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "params": vars(a),
        "summary": summarize(reqs, wall, samples),
        "requests": reqs,
    }
    with open(a.out, "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
