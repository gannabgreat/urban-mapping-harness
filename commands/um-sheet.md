---
description: 분석 시트 1장 파이프라인 — 수집 → 정합 → 판독 → 작도 → 자가검토. 인자: 시트 번호 (예 /um-sheet 2.7h)
---
urban-mapping-harness 스킬의 「시트 파이프라인」으로 시트 $ARGUMENTS 를 만든다.

1. `sheets/SHEETS.md` 에서 이 시트가 교안의 어떤 항목인지·필요한 레이어를 확인한다. 없으면 교안에서 찾아 한 줄 추가.
2. collector 에 필요한 데이터를 맡긴다(이미 있으면 건너뜀). `SOURCES.md` 갱신 확인.
3. 좌표가 안 맞는 레이어가 있으면 georef 에 맡긴다. 잔차를 받는다.
4. 사진·항공 판독이 필요하면 reader 에 맡기고, 표본을 본체가 직접 확인한다.
5. cartographer 가 `scripts/sheet_<번호>.py` 로 그린다. 문장 속 숫자는 계산값.
6. 본체가 PNG 를 열어 보고, 숫자 3개를 무작위로 골라 데이터와 대조한다.
7. `_state/sheet-status.json` 을 `초안` 으로, git 커밋.
