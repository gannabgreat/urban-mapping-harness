# scripts

- `fetch_*.py` 수집 · `georef*.py` 정합 · `read_*.py` 판독 · `sheet_<번호>.py` 작도
- `run.sh` 하나로 전체 재실행(하나라도 실패하면 멈춘다)
- `sheet_template.py` — 시트 견본. 복사해서 `sheet_<번호>.py` 로 쓴다. A3 실제 축척 지도 축, `check_scale()` 축척 검사, 축척 막대·방위·출처 각주, 문장 속 숫자 계산, PNG·PDF·SVG 동시 출력, 0건 레이어는 실패로 멈춤.
- 필요 패키지: `pip install matplotlib shapely` (정합·판독은 pyproj·opencv 등 추가)
- 키는 환경변수로만 (`DATAGOKR_KEY`, `KAKAO_REST_KEY` 등). 코드에 박지 마라.
