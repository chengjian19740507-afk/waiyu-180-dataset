#!/bin/bash
# ════════════════════════════════════════════════════════════════
#  发布到 npm registry（包名：waiyu-180）
#
#  前置：npm whoami  能出用户名（即已登录）
#  发布后建议开启 provenance：
#    npm publish --provenance --access public
# ════════════════════════════════════════════════════════════════
set -euo pipefail
cd "$(dirname "$0")/.."

echo "▶ 检查登录"
npm whoami >/dev/null 2>&1 || { echo "✗ 未登录，请先执行：npm adduser"; exit 1; }
echo "  当前账号：$(npm whoami)"

echo "▶ 重建产物"
python3 scripts/build_dataset.py >/dev/null

echo "▶ 版本"
VER=$(node -p "require('./package.json').version")
echo "  waiyu-180@$VER"

echo "▶ 发布"
npm publish --access public --provenance

echo "✓ 已发布：https://www.npmjs.com/package/waiyu-180"
echo
echo "后续：记得在 GitHub 仓加 tag v$VER，并在 npm 页回链仓库"
