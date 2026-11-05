# Hardware: day-vault

8x NVIDIA RTX 3090, each power-capped at 160 W. The 1 November 2026 DayVault protocol ran on this box with those caps and unlock off.

| Part | What's installed |
|------|------------------|
| GPUs | 8x NVIDIA RTX 3090, 24 GB each (192 GB VRAM total) |
| GPU power | each card power-capped at 160 W. Nov 1 protocol: unlock off. |
| Interconnect | PCIe only, no NVLink |
| Motherboard | Gigabyte MC62-G40 (7 PCIe slots, one bifurcated to fit 8 cards) |
| CPU | AMD Threadripper PRO 3945WX, 12 cores / 24 threads |
| RAM | 224 GiB DDR4 |
| Storage | 500 GB NVMe + 4 TB NVMe |
| PSUs | ASRock 1600 W + MSI 850 W |

Notes:

- GPU count, the 160 W cap, and unlock off are from the Nov 1 protocol (SUMMARY header and results.json `hardware`), measured by Day on day-vault.
- CPU, board, RAM, storage, PSUs, and the lack of NVLink are the 28 October 2026 inventory. The Nov 1 files do not restate those rows.
- A Threadripper PRO 3975WX is owned but not installed. If it goes in, cards measured before and after must say which CPU they used.
- PCIe link gen and width per card were not in the Nov 1 files. Which GPU indices share the bifurcated slot: not recorded there.
- Driver and CUDA version: not recorded in the Nov 1 protocol.
- The 160 W cap is part of the setup. Cards do not raise it for benchmarks.
