---
description: 새 현황분석 인스턴스를 만든다. 인자: 프로젝트 slug (예 /um-init seochon-hyojaro)
---
새 Urban Mapping 인스턴스를 만들어라.

1. 대상 경로: 인자가 경로면 그대로, slug 면 `./um-<slug>/`. 이미 있으면 멈추고 알린다.
2. 이 플러그인의 `templates/project-scaffold/` 를 통째로 복사한다.
3. `CLAUDE.md` 의 `{{PROJECT_NAME}}`·`{{DATE}}` 를 치환한다.
4. 사용자에게 묻고 `CLAUDE.md` 「인스턴스 결정 항목」에 적는다: 대상지 경계·담당 가로, 과목·과제 안내 파일, 교수 제공 자료 목록, 시트 규격(A3·축척), 제출일·발표일, 시트 번호 체계, 생성형 이미지 허용 여부.
5. `git init` 후 첫 커밋.
6. 보고: 경로, 다음 단계(`data/raw/` 에 교수 PDF 넣기 → `/um-sheet 2.1`).
