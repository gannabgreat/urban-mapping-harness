# Urban Mapping Harness

**도시설계 현황분석(Urban Mapping) 하네스** — Claude Code 플러그인. 교수 제공 도면·공공데이터·지도 판독으로 A3 분석 시트를 코드로 그리고, 만든 쪽과 다른 AI 검수자가 4번 뜯어보는 구조입니다.

> Urban-mapping harness for Claude Code: public-data collection, georeferencing, code-drawn A3 analysis sheets, a 4-round adversarial review, and a field-check list. 7 agents, 4 commands. Fully local.

실제로 한 학기 「도시와 디자인」 Project 2(가로 현황분석, A3 시트 26장)를 이 방식으로 만들었고, 그 과정을 일반화했습니다.

## 설치
```
/plugin marketplace add gannabgreat/urban-mapping-harness
/plugin install urban-mapping-harness@urban-mapping-harness
```

## 핵심 원칙
- **숫자는 손으로 안 쓴다** — 시트 문장 속 숫자는 데이터에서 계산되어 들어간다. 데이터가 바뀌면 글도 바뀐다.
- **모르면 「없음」이 아니라 「판독 불가·현장 확인」** — 빈 값은 실패로 취급하고 현장 확인 목록(`FIELD_TODO.md`)으로 보낸다.
- **만든 쪽 ≠ 검토하는 쪽** — 검토는 4차까지, 차수마다 다른 검수자. 지적은 그대로 받지 않고 데이터로 다시 계산해서 맞는 것만 고친다.
- **자동 판정은 표본 확인 뒤에** — 색 판정·사진 판독 규칙은 표본을 사람/본체가 직접 보고 맞는지 확인한 뒤에 전체에 돌린다.
- **출처가 시트에 남는다** — 모든 레이어에 출처·기준일을 적는다(`SOURCES.md`).
- **사람 몫과 자동 몫을 나눈다** — 답사·촬영·판단·롤백은 사람, 수집·정합·판독·작도·계산·검토는 AI.

## 구성
| 경로 | 내용 |
|---|---|
| `docs/SPEC.md` | 정본 명세 |
| `agents/` | collector · georef · cartographer · reader · verify · blind-critic · field (7종) |
| `skills/urban-mapping-harness/` | 오케스트레이션(원칙·단계·검토 게이트) |
| `skills/urban-mapping-reference/` | 한국 공공데이터 출처, 좌표 정합, 시트 목록, 사진 판독, 검토 체크리스트, 파이썬 도구 |
| `commands/` | `/um-init` `/um-sheet` `/um-review` `/um-field` |
| `templates/project-scaffold/` | 인스턴스 스켈레톤 |

## 사용 흐름
1. `/um-init <slug>` — 인스턴스 생성 + 대상지·담당 가로·제출 규격·교수 제공 자료 인터뷰
2. 교수 PDF·답사사진을 `data/raw/`·`photos/` 에 넣는다
3. `/um-sheet <번호>` — 시트 1장: 수집 → 정합 → 판독 → 작도 → 자가검토
4. `/um-review <차수>` — 적대적 검토 1~4차
5. `/um-field` — 현장에서만 확인되는 항목 목록 뽑기(줄자 실측·개방 여부 등)

## 참고
구조(플러그인·에이전트·커맨드·스캐폴드 분리)는 [FrownyFrown/urban-design-harness](https://github.com/FrownyFrown/urban-design-harness)(MIT)를 참고했습니다. 그쪽은 마스터플랜·판넬 설계 중심, 이쪽은 현황분석·데이터 중심입니다.

## 라이선스
MIT
