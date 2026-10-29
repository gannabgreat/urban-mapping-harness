#!/usr/bin/env python3
"""urban-mapping-harness PreToolUse 게이트 (Write|Edit|MultiEdit).

막는 것 두 가지 — 문장 규칙을 실제로 강제하는 최소 장치다.
1. data/raw/ 원본 수정 (SPEC §2·§3 「원본은 수정 금지」)
2. _state/sheet-status.json 에서 시트를 「제출」로 올리는데 _state/review-log.json 에
   검토 1·2·3·4차 기록이 다 없을 때 (SPEC §5 「4차 검토 통과가 제출 조건」)

현황분석 인스턴스(cwd 위로 sheets/SHEETS.md 가 있는 곳)가 아니면 아무것도 안 한다.
review-log 를 못 읽으면 통과가 아니라 차단한다(fail-closed).
Bash 로 쓰는 경로는 못 막는다 — 이 훅은 실수 방지용이지 보안 장치가 아니다.
종료코드 2 + stderr = Claude Code 가 도구 호출을 막고 이유를 모델에 돌려준다.
"""
import json
import sys
from pathlib import Path

SUBMIT = {"제출", "submitted", "final"}
ROUNDS_REQUIRED = {1, 2, 3, 4}


def block(msg):
    print(f"[urban-mapping-harness 게이트] {msg}", file=sys.stderr)
    sys.exit(2)


def find_instance(start):
    for d in [start, *start.parents]:
        if (d / "sheets" / "SHEETS.md").is_file():
            return d
    return None


def proposed_text(tool, inp, path):
    if tool == "Write":
        return inp.get("content", "")
    cur = path.read_text(encoding="utf-8") if path.exists() else ""
    edits = inp.get("edits") if tool == "MultiEdit" else [inp]
    for e in edits or []:
        old, new = e.get("old_string", ""), e.get("new_string", "")
        if e.get("replace_all"):
            cur = cur.replace(old, new)
        else:
            cur = cur.replace(old, new, 1)
    return cur


def statuses(doc):
    sheets = (doc or {}).get("sheets") or {}
    out = {}
    for k, v in sheets.items():
        if isinstance(v, dict):
            v = v.get("status") or v.get("상태")
        out[k] = str(v or "")
    return out


def done_rounds(instance):
    p = instance / "_state" / "review-log.json"
    try:
        log = json.loads(p.read_text(encoding="utf-8"))
        rounds = log["rounds"]
    except Exception as e:  # 못 읽음 = 판정 불가 = 차단
        block(f"review-log.json 을 못 읽어 제출 여부를 판정할 수 없다({e}). 검토 기록부터 복구하라.")
    got = set()
    for r in rounds:
        n = r.get("차수", r.get("round"))
        try:
            got.add(int(n))
        except (TypeError, ValueError):
            continue
    return got


def main():
    try:
        ev = json.load(sys.stdin)
    except Exception:
        return 0  # 훅 입력이 깨지면 게이트 대상 판단도 못 한다 — 도구 자체는 막지 않는다
    tool = ev.get("tool_name", "")
    inp = ev.get("tool_input") or {}
    if tool not in {"Write", "Edit", "MultiEdit"} or not inp.get("file_path"):
        return 0
    cwd = Path(ev.get("cwd") or ".").resolve()
    path = Path(inp["file_path"])
    path = (path if path.is_absolute() else cwd / path).resolve()
    instance = find_instance(path.parent) or find_instance(cwd)
    if not instance:
        return 0
    try:
        rel = path.relative_to(instance)
    except ValueError:
        return 0

    if rel.parts[:2] == ("data", "raw"):
        block(f"{rel} 는 원본(data/raw/)이다. 원본은 고치지 말고 가공본을 data/ 에 써라.")

    if rel.as_posix() == "_state/sheet-status.json":
        before = {}
        if path.exists():
            try:
                before = statuses(json.loads(path.read_text(encoding="utf-8")))
            except Exception:
                before = {}
        try:
            after = statuses(json.loads(proposed_text(tool, inp, path)))
        except Exception as e:
            block(f"sheet-status.json 수정 결과가 JSON 이 아니다({e}).")
        newly = [k for k, v in after.items() if v in SUBMIT and before.get(k) not in SUBMIT]
        if newly:
            missing = sorted(ROUNDS_REQUIRED - done_rounds(instance))
            if missing:
                block(f"시트 {', '.join(newly)} 를 제출로 올릴 수 없다 — review-log 에 검토 {missing}차 기록이 없다. "
                      f"/um-review 로 1~4차를 먼저 끝내라.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
