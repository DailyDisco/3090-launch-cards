<!-- PRIVATE / INTERNAL DRAFT -->

# Hardware: day-vault

Facts as of Oct 28, 2026. Every card is measured on this box unless it says otherwise.

| Part | What's installed |
|------|------------------|
| GPUs | 8x NVIDIA RTX 3090, 24 GB each (192 GB VRAM total) |
| GPU power | each card power-capped at 160 W |
| Interconnect | PCIe only, no NVLink |
| Motherboard | Gigabyte MC62-G40 (7 PCIe slots, one bifurcated to fit 8 cards) |
| CPU | AMD Threadripper PRO 3945WX, 12 cores / 24 threads |
| RAM | 224 GiB DDR4 |
| Storage | 500 GB NVMe + 4 TB NVMe |
| PSUs | ASRock 1600 W + MSI 850 W |

Notes:

- A Threadripper PRO 3975WX is owned but not installed. If it goes in, cards measured before and after must say which CPU they used.
- PCIe link gen and width per card are captured by the bench script (`gpus.csv`) on every run. Because one slot is bifurcated, two cards share a slot's lanes. Which GPU indices those are: TBD (from Day's `gpus.csv`).
- Driver and CUDA version: TBD (captured per run in `gpus.csv` and `vllm_version.txt`).
- The 160 W cap is part of the setup. Cards do not raise it for benchmarks.
