# 06. 파이썬 도구

| 라이브러리 | 역할 |
|---|---|
| PyMuPDF (fitz) | 교수 PDF 벡터·채움색 추출, 교안 PDF 페이지 이미지 |
| shapely | 건물·필지·버퍼(역세권 250/500 m)·교차 |
| pyproj | EPSG:5186/5174/4326 변환 |
| matplotlib | 시트 작도(PNG·PDF·SVG 동시 출력, SVG 는 `svg.fonttype='none'` 으로 글자 유지) |
| rasterio | DSM·위성 격자 |
| OpenCV | 위성·사진 정합(윤곽 상관), HSV 초록 판정 |
| networkx | 골목 도보 거리·접근성 |
| cairosvg | CC0 벡터 축척 요소 래스터화 |
| requests | API 수집 |

- 재실행 스크립트 하나(`run.sh`)로 수집 → 정합 → 시트 전체를 다시 그릴 수 있게 둔다.
- 한글 폰트는 시트 전체에 같은 것 하나(인스턴스 CLAUDE.md 에 지정).
