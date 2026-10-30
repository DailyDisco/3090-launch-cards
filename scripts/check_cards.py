#!/usr/bin/env python3
"""Lint cards: required fields present, no em dashes, no invented-looking numbers left unlabeled."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQUIRED = ["Model", "Quant", "Engine", "Engine version", "TP / PP", "Context length",
            "Measured by", "Date measured", "## Launch command", "## Key flags and why",
            "## Results", "Prefill tok/s", "Decode tok/s", "TTFT", "## VRAM and power",
            "## Verified vs not verified"]

errors = []
for md in sorted(ROOT.rglob("*.md")):
    text = md.read_text()
    if "\u2014" in text:
        errors.append(f"{md.relative_to(ROOT)}: contains an em dash")
for card in sorted((ROOT / "cards").glob("[0-9]*.md")):
    text = card.read_text()
    for field in REQUIRED:
        if field not in text:
            errors.append(f"{card.name}: missing '{field}'")
    if "measured by day on day-vault" not in text.lower():
        errors.append(f"{card.name}: missing 'Measured by Day on day-vault'")
print("\n".join(errors) or "cards OK")
sys.exit(1 if errors else 0)
