#!/usr/bin/env bash
# Card 001 run, copied verbatim from Local AI Lab (/workspace/hub/cards/nanbeige-vs-qwen-tp4.sh, Oct 28 2026). Not yet run.
# Paste the whole file into a shell on day-vault. Output: ~/bench/nanbeige-vs-qwen-tp4-<ts>/summary.json

bash <<'EOF'
# day-vault: Nanbeige4.3-33B vs Qwen3.8-27B, vLLM 0.32.0, BF16, TP=4 on GPUs 0-3.
# Rig as-is: 8x 3090 @160W (do not change), TR PRO 3945WX. Takes ~30-60 min incl. downloads.
set -euo pipefail
OUT=~/bench/nanbeige-vs-qwen-tp4-$(date +%Y%m%d-%H%M); mkdir -p "$OUT"
export CUDA_VISIBLE_DEVICES=0,1,2,3
python3 -c "import vllm;print(vllm.__version__)" > "$OUT/vllm_version.txt"
nvidia-smi --query-gpu=index,name,power.limit,pcie.link.gen.current,pcie.link.width.current,driver_version --format=csv > "$OUT/gpus.csv"
lscpu | grep -m1 "Model name" > "$OUT/cpu.txt"
for M in Nanbeige/Nanbeige4.3-33B Qwen/Qwen3.8-27B; do
  T=$(basename "$M")
  echo ">> $T: starting server"
  vllm serve "$M" --tensor-parallel-size 4 --dtype bfloat16 --max-model-len 65536 \
    --gpu-memory-utilization 0.92 --port 8000 > "$OUT/$T-server.log" 2>&1 &
  SRV=$!
  until curl -sf localhost:8000/v1/models >/dev/null; do
    sleep 5; kill -0 $SRV 2>/dev/null || { echo "server died, see $OUT/$T-server.log"; exit 1; }
  done
  nvidia-smi --query-gpu=index,power.draw,memory.used --format=csv,noheader,nounits -lms 500 > "$OUT/$T-gpu.csv" &
  SMI=$!
  # name input_len output_len concurrency num_prompts
  for cfg in "prefill8k 8192 1 1 8" "prefill32k 32768 1 1 4" "decode8k 8192 512 1 4" "decode32k 32768 512 1 4" "conc4_4k 4096 512 4 32"; do
    read -r N I O C P <<< "$cfg"
    echo ">> $T: $N"
    vllm bench serve --model "$M" --port 8000 --dataset-name random \
      --random-input-len $I --random-output-len $O --max-concurrency $C --num-prompts $P \
      --ignore-eos --percentile-metrics ttft,tpot,itl \
      --save-result --result-dir "$OUT" --result-filename "$T-$N.json"
  done
  kill $SMI; kill $SRV; wait $SRV 2>/dev/null || true; sleep 15
done
python3 - "$OUT" <<'PY'
import json,sys,glob,os,csv,collections
out=sys.argv[1]; res={"vllm":open(f"{out}/vllm_version.txt").read().strip(),"cpu":open(f"{out}/cpu.txt").read().split(":")[-1].strip(),"tp":4,"dtype":"bf16","models":{}}
for m in ["Nanbeige4.3-33B","Qwen3.8-27B"]:
  r={}
  for f in sorted(glob.glob(f"{out}/{m}-*.json")):
    n=os.path.basename(f)[len(m)+1:-5]; d=json.load(open(f))
    e={"ttft_ms_mean":round(d["mean_ttft_ms"],1),"tpot_ms_mean":round(d.get("mean_tpot_ms",0),2),"output_tok_s":round(d["output_throughput"],1)}
    if n.startswith("prefill"): e["prefill_tok_s"]=round(d["total_input_tokens"]/d["completed"]/(d["mean_ttft_ms"]/1000),1)
    if n.startswith("decode"): e["decode_tok_s_single_stream"]=round(1000/d["mean_tpot_ms"],1)
    r[n]=e
  g=collections.defaultdict(lambda:{"power_w":[],"vram_mib":[]})
  for row in csv.reader(open(f"{out}/{m}-gpu.csv")):
    try: i,p,v=[x.strip() for x in row]; g[i]["power_w"].append(float(p)); g[i]["vram_mib"].append(float(v))
    except ValueError: pass
  r["gpus"]={i:{"power_w_max":max(x["power_w"]),"power_w_mean":round(sum(x["power_w"])/len(x["power_w"]),1),"vram_mib_max":max(x["vram_mib"])} for i,x in g.items()}
  res["models"][m]=r
json.dump(res,open(f"{out}/summary.json","w"),indent=2); print(json.dumps(res,indent=2)); print("saved",f"{out}/summary.json")
PY
EOF
