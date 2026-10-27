#!/bin/bash
# ════════════════════════════════════════════════════════════════
#  发布到 HuggingFace Hub
#
#  前置：
#    1. 已创建 HF 数据集仓（用户名/waiyu-180）
#    2. 已拿到写权限 token：huggingface-cli login
#
#  用法：
#    HF_REPO=chengjian19740507-afk/waiyu-180 bash scripts/publish_hf.sh
# ════════════════════════════════════════════════════════════════
set -euo pipefail
cd "$(dirname "$0")/.."

REPO="${HF_REPO:-chengjian19740507-afk/waiyu-180}"

echo "▶ 检查登录状态"
huggingface-cli whoami >/dev/null 2>&1 || {
  echo "✗ 未登录，请先执行：huggingface-cli login"; exit 1;
}

echo "▶ 重建产物"
python3 scripts/build_dataset.py

echo "▶ 上传数据文件（排除代码仓自有文件）"
for p in data/sentences.jsonl data/vocab.jsonl data/sentences.parquet data/vocab.parquet \
         data/sentences data/vocab dataset_info.json README.md; do
  [ -e "$p" ] || continue
  echo "  → $p"
  huggingface-cli upload "$REPO" "$p" --repo-type dataset --exclude "*.gitattributes" >/dev/null
done

echo "✓ 已发布到 https://huggingface.co/datasets/$REPO"
echo
echo "下一步：去 HF 数据集页 Settings → Files，删除仓库里遗留的非数据文件（如 index.js）"
