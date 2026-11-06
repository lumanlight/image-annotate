#!/usr/bin/env bash
# 在任意新机器上重建本技能的 venv（venv 机器/架构相关，不能跨机器拷贝）
# 用法: bash setup.sh
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---- 系统依赖 preflight（pip 装不来的东西）----
missing=0
if ! ldconfig -p 2>/dev/null | grep -q 'libcairo\.so\.2'; then
  echo "✗ 缺 libcairo2（cairosvg 渲染必需）：sudo apt-get install -y libcairo2" >&2; missing=1
fi
if ! fc-list 2>/dev/null | grep -qi 'Noto Sans CJK'; then
  echo "✗ 缺中文字体（中文会变豆腐块）：sudo apt-get install -y fonts-noto-cjk" >&2; missing=1
fi
[ "$missing" = 0 ] || { echo "先装上面缺的系统包再跑本脚本。" >&2; exit 1; }

# ---- 建 venv：优先 uv，退回标准库 venv + pip ----
if [ ! -x "$here/venv/bin/python" ]; then
  if command -v uv >/dev/null 2>&1; then
    # 某些环境 ~/.cache 不可写 → uv 会报 "Read-only file system"，改用临时缓存目录
    if ! [ -w "${XDG_CACHE_HOME:-$HOME/.cache}" ]; then
      export UV_CACHE_DIR="$(mktemp -d)"
      echo "· 缓存目录不可写，改用临时 UV_CACHE_DIR=$UV_CACHE_DIR"
    fi
    uv venv --python 3.12 "$here/venv"
    uv pip install --python "$here/venv/bin/python" -r "$here/requirements.txt"
  else
    echo "· 未找到 uv，改用标准库 venv + pip（可能需要 python3-venv）"
    python3 -m venv "$here/venv"
    "$here/venv/bin/python" -m pip install --upgrade pip
    "$here/venv/bin/python" -m pip install -r "$here/requirements.txt"
  fi
else
  echo "· venv 已存在，跳过创建（如需重建：rm -rf '$here/venv' 后重跑）"
fi

echo "OK: $("$here/venv/bin/python" -c 'import ainotate,rough;print("ainotate",ainotate.__version__,"rough ok")')"
