#!/bin/zsh
# 전체 재실행: 수집 → 정합 → 판독 → 시트. 하나라도 실패하면 멈춘다.
set -euo pipefail
cd "$(dirname "$0")/.."
PY=${PY:-python3}

for f in scripts/fetch_*.py(N) scripts/georef*.py(N) scripts/read_*.py(N); do
  echo "▶ $f"; $PY "$f"
done
for f in scripts/sheet_*.py(N); do
  [[ $f == scripts/sheet_template.py ]] && continue
  echo "▶ $f"; $PY "$f"
done
echo "끝 — out/ 확인"
