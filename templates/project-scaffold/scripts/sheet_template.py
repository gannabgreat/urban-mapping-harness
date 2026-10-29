"""시트 1장 = 스크립트 1개. 이 파일을 sheet_<번호>.py 로 복사해서 고친다.

지키는 것
- 지도는 실제 축척(기본 S 1:2,500, A3 100% 인쇄)으로 그린다. check_scale() 이 틀리면 멈춘다.
- 문장 속 숫자는 data/ 에서 계산한 값을 f-string 으로 넣는다. 손으로 쓴 숫자 금지.
- 출처·기준일 각주, 축척 막대, 방위, 범례를 모든 지도에 넣는다.
- PNG(170dpi)·PDF·SVG 세 개를 out/ 에 쓴다. SVG 는 글자를 텍스트로 남긴다.

실행: python scripts/sheet_template.py  (예시 데이터로 out/sheet_template.* 생성)
"""
import json
import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Polygon as MplPolygon
from shapely.geometry import shape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"

A3_MM = (420, 297)          # A3 가로
MM = 1 / 25.4               # mm → inch
FONT = os.environ.get("SHEET_FONT", "Apple SD Gothic Neo")  # 인스턴스 CLAUDE.md 의 한글 폰트로
try:  # 폰트가 없으면 한글이 네모로 찍힌다 — 조용히 대체하지 말고 멈춘다
    font_manager.findfont(FONT, fallback_to_default=False)
except ValueError:
    sys.exit(f"한글 폰트 '{FONT}' 를 못 찾았다. SHEET_FONT 환경변수로 설치된 폰트 이름을 줘라.")
plt.rcParams["font.family"] = FONT
plt.rcParams["svg.fonttype"] = "none"   # SVG 글자를 텍스트로 유지
plt.rcParams["pdf.fonttype"] = 42


def load_layer(path):
    """GeoJSON(EPSG:5186 등 m 단위 투영좌표)을 읽는다. 0건이면 실패로 올린다(없음 ≠ 못 읽음)."""
    with open(path, encoding="utf-8") as f:
        fc = json.load(f)
    feats = fc.get("features") or []
    if not feats:
        raise RuntimeError(f"{path}: 피처 0건 — 수집 실패로 보고 멈춘다")
    return [(shape(ft["geometry"]), ft.get("properties", {})) for ft in feats]


def map_axes(fig, x_mm, y_mm, w_mm, h_mm, center, scale):
    """종이 위 (x,y,w,h mm) 자리에 축척 1:scale 지도 축을 만든다. center=(X,Y) m."""
    W, H = A3_MM
    ax = fig.add_axes([x_mm / W, y_mm / H, w_mm / W, h_mm / H])
    half_w = w_mm / 1000 * scale / 2
    half_h = h_mm / 1000 * scale / 2
    ax.set_xlim(center[0] - half_w, center[0] + half_w)
    ax.set_ylim(center[1] - half_h, center[1] + half_h)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([]); ax.set_yticks([])
    return ax


def check_scale(fig, ax, scale, tol=0.01):
    """축의 실제 종이 폭(mm)과 지면 폭(m)으로 축척을 다시 계산해 표기와 맞는지 본다."""
    fig.canvas.draw()
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    paper_mm = bbox.width * 25.4
    ground_m = ax.get_xlim()[1] - ax.get_xlim()[0]
    real = ground_m * 1000 / paper_mm
    if abs(real - scale) / scale > tol:
        raise RuntimeError(f"축척 불일치: 표기 1:{scale}, 실제 1:{real:.0f}")
    return real


def scale_bar(ax, length_m, label=None):
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    x, y = x0 + (x1 - x0) * 0.04, y0 + (y1 - y0) * 0.05
    ax.plot([x, x + length_m], [y, y], color="k", lw=2, solid_capstyle="butt")
    for t in (x, x + length_m):
        ax.plot([t, t], [y, y + (y1 - y0) * 0.01], color="k", lw=1)
    ax.text(x + length_m / 2, y + (y1 - y0) * 0.015, label or f"{length_m:g} m", ha="center", va="bottom", fontsize=6)


def north_arrow(ax):
    ax.annotate("", xy=(0.95, 0.92), xytext=(0.95, 0.84), xycoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", color="k", lw=1))
    ax.text(0.95, 0.93, "N", transform=ax.transAxes, ha="center", va="bottom", fontsize=8)


def save_all(fig, name):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / f"{name}.png", dpi=170)
    fig.savefig(OUT / f"{name}.pdf")
    fig.savefig(OUT / f"{name}.svg")
    return [OUT / f"{name}.{e}" for e in ("png", "pdf", "svg")]


def example_layer():
    """예시용 건물 3동(EPSG:5186 근처 가짜 좌표). 실제 시트에서는 load_layer('data/<레이어>.geojson')."""
    feats = []
    for i, (x, y, w, h, use) in enumerate([(0, 0, 20, 12, "근생"), (30, 5, 15, 15, "주거"), (10, 30, 25, 10, "근생")]):
        X, Y = 197000 + x, 553000 + y
        feats.append({"type": "Feature", "properties": {"id": i + 1, "용도": use},
                      "geometry": {"type": "Polygon", "coordinates": [[[X, Y], [X + w, Y], [X + w, Y + h], [X, Y + h], [X, Y]]]}})
    return [(shape(f["geometry"]), f["properties"]) for f in feats]


def main():
    scale = 2500
    bldg = example_layer()

    # 숫자는 여기서 계산한다
    n = len(bldg)
    n_shop = sum(1 for _, p in bldg if p["용도"] == "근생")
    share = n_shop / n * 100
    area = sum(g.area for g, _ in bldg)

    fig = plt.figure(figsize=(A3_MM[0] * MM, A3_MM[1] * MM))
    fig.text(15 / A3_MM[0], 1 - 15 / A3_MM[1], "0.0 시트 제목", fontsize=16, weight="bold", va="top")

    cx = sum(g.centroid.x for g, _ in bldg) / n
    cy = sum(g.centroid.y for g, _ in bldg) / n
    ax = map_axes(fig, 15, 30, 260, 230, (cx, cy), scale)
    colors = {"근생": "#e4572e", "주거": "#f3d34a"}
    for g, p in bldg:
        ax.add_patch(MplPolygon(list(g.exterior.coords), closed=True, fc=colors[p["용도"]], ec="k", lw=0.3))
    scale_bar(ax, 50)
    north_arrow(ax)
    real = check_scale(fig, ax, scale)

    for i, (k, c) in enumerate(colors.items()):
        fig.patches.append(plt.Rectangle(((290) / A3_MM[0], (240 - i * 8) / A3_MM[1]), 6 / A3_MM[0], 4 / A3_MM[1],
                                         transform=fig.transFigure, fc=c, ec="k", lw=0.3))
        fig.text(298 / A3_MM[0], (241 - i * 8) / A3_MM[1], k, fontsize=8)

    body = (f"건물 {n}동 중 근생 {n_shop}동({share:.0f}%).\n"
            f"건축면적 합계 {area:,.0f}㎡.")
    fig.text(290 / A3_MM[0], 200 / A3_MM[1], body, fontsize=9, va="top", linespacing=1.6)
    fig.text(15 / A3_MM[0], 12 / A3_MM[1],
             f"S 1:{scale:,} (A3 100% 인쇄) · 출처: 예시 데이터 · 기준일: - · SOURCES.md 참조",
             fontsize=6, color="#555")

    paths = save_all(fig, "sheet_template")
    print(f"축척 확인 1:{real:.0f}", *map(str, paths), sep="\n")


if __name__ == "__main__":
    sys.exit(main())
