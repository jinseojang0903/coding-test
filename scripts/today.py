"""오늘 풀 문제를 계획(plan/*.md)에서 꺼내 new.py 명령으로 보여 준다.

요일별로 보여 주는 내용:
  월·수·금  plan/algorithm.md 에서 아직 안 푼 첫 일차 (워밍업 + 본 문제)
  화·목     plan/sql.md 에서 아직 안 푼 첫 일차
  토        plan/mock.md 에서 아직 안 푼 첫 회차 (3문제)
  일        복습 날짜가 된 오답 노트, 오답 노트를 안 쓴 이번 주 X 문제

사용 예:
  python scripts/today.py                    # 오늘 요일 기준
  python scripts/today.py --mode sql         # 요일과 상관없이 SQL 계획 보기
  python scripts/today.py --date 2026-11-07  # 다른 날짜 기준으로 미리 보기

푼 문제는 programmers/ 아래에 같은 번호로 시작하는 파일이 있는지로 판단한다.
이 스크립트는 파일을 만들거나 고치지 않는다. 계획 파일 형식이 잘못되면 종료 코드 1.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

from common import ROOT, SOLUTION_EXTS, setup_console
from update_readme import Solution, collect_solutions

PLAN_DIR = ROOT / "plan"
WEEKDAY_NAMES = "월화수목금토일"
MODE_BY_WEEKDAY = {0: "algorithm", 1: "sql", 2: "algorithm", 3: "sql", 4: "algorithm", 5: "mock", 6: "review"}
MODE_LABELS = {"algorithm": "알고리즘", "sql": "SQL", "mock": "실전 모의", "review": "복기"}
DAILY_GOAL = 2

TABLE_SEPARATOR = re.compile(r"^:?-+:?$")
LINK_CELL = re.compile(r"^\[(.*)\]\((.*)\)$")
NOTE_TITLE = re.compile(r"^###\s+\[(.*)\]\((.*)\)\s*$")
REVIEW_ITEM = re.compile(r"^-\s+\[( |x|X)\]\s+복습 날짜:\s*(\d{4}-\d{2}-\d{2})")


class PlanError(Exception):
    """계획 파일을 읽을 수 없거나 형식이 잘못됨. main 에서 메시지만 출력한다."""


@dataclass
class PlanItem:
    group: int  # 일차(알고리즘·SQL) 또는 회차(모의)
    number: str
    title: str
    link: str
    level: str  # 실제 난이도 (lv1 등)
    role: str  # 워밍업 / 본 문제. 모의는 빈 값
    type: str  # 유형. 모의는 빈 값 (실전처럼 유형을 모르고 푼다)


def load_plan(mode: str) -> List[PlanItem]:
    """plan/{mode}.md 의 마크다운 표를 읽는다. 표 위아래의 설명 글은 무시한다."""
    path = PLAN_DIR / f"{mode}.md"
    if not path.exists():
        raise PlanError(f"계획 파일이 없습니다: plan/{mode}.md")

    items: List[PlanItem] = []
    header: Optional[List[str]] = None
    for line_no, raw_line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), start=1):
        line = raw_line.strip()
        if not line.startswith("|"):
            header = None  # 표가 끝나면 다음 표는 새 헤더부터 읽는다
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(TABLE_SEPARATOR.match(cell) for cell in cells):
            continue

        row = dict(zip(header, cells))
        group_text = row.get("일차") or row.get("회차") or ""
        number = row.get("번호", "")
        if not group_text.isdigit() or not number.isdigit():
            raise PlanError(f"plan/{mode}.md {line_no}번째 줄: 일차(회차)와 번호는 숫자여야 합니다.")
        title_cell = row.get("문제", "")
        link_match = LINK_CELL.match(title_cell)
        items.append(
            PlanItem(
                group=int(group_text),
                number=number,
                title=(link_match.group(1) if link_match else title_cell).strip(),
                link=link_match.group(2) if link_match else "",
                level=row.get("레벨", "").lower(),
                role=row.get("구분", ""),
                type=row.get("유형", ""),
            )
        )

    if not items:
        raise PlanError(f"plan/{mode}.md 에서 문제 표를 찾지 못했습니다.")
    return items


def solved_numbers() -> Set[str]:
    """programmers/ 아래 풀이 파일 이름 앞의 문제 번호 목록."""
    numbers: Set[str] = set()
    folder = ROOT / "programmers"
    if not folder.exists():
        return numbers
    for path in folder.rglob("*"):
        if path.is_file() and path.suffix.lower() in SOLUTION_EXTS:
            prefix = path.stem.split("_", 1)[0]
            if prefix.isdigit():
                numbers.add(prefix)
    return numbers


def new_command(item: PlanItem, mode: str) -> str:
    # SQL 은 레벨과 상관없이 programmers/sql/ 에 저장한다
    level = "sql" if mode == "sql" else item.level
    # 큰따옴표로 감싸면 PowerShell·bash·zsh 어디서든 공백·괄호가 있는 제목을 그대로 넘길 수 있다
    title = item.title.replace('"', "")
    command = f'python scripts/new.py programmers {level} {item.number} "{title}"'
    if item.type:
        command += f' --type "{item.type}"'
    return command


def show_plan(mode: str, today: dt.date, solved_today: List[Solution]) -> None:
    items = load_plan(mode)
    solved = solved_numbers()

    groups: Dict[int, List[PlanItem]] = {}
    for item in items:
        groups.setdefault(item.group, []).append(item)
    done_count = sum(1 for g in groups.values() if all(i.number in solved for i in g))
    unit = "회차" if mode == "mock" else "일차"
    label = MODE_LABELS[mode]

    current = next(
        (groups[key] for key in sorted(groups) if any(i.number not in solved for i in groups[key])),
        None,
    )
    if current is None:
        print(f"{label} 계획을 모두 끝냈습니다 ({done_count}/{len(groups)}{unit}).")
        print(f"plan/{mode}.md 에 문제를 더 추가하세요.")
        return

    if mode in ("algorithm", "sql") and len(solved_today) >= DAILY_GOAL:
        print(f"오늘 목표({DAILY_GOAL}문제)를 채웠습니다. 아래는 다음 순서이고, 더 풀고 싶을 때만 이어서 푸세요.\n")

    if mode == "mock":
        mock_file = ROOT / "mock-tests" / f"{today.isoformat()}.md"
        if not mock_file.exists():
            print("먼저 모의 기록 파일을 만듭니다:")
            print("    python scripts/new.py mock\n")

    type_text = f" · {current[0].type}" if current[0].type else ""
    print(f"[{label}] {current[0].group}{unit}{type_text}  (완료 {done_count}/{len(groups)}{unit})")
    for item in current:
        role = item.role or "문제"
        if item.number in solved:
            print(f"  [완료] {role}: {item.number} {item.title} ({item.level})")
            continue
        print(f"  {role}: {item.number} {item.title} ({item.level})")
        if item.link:
            print(f"    {item.link}")
        print(f"    {new_command(item, mode)}")

    remaining = [i for i in current if i.number not in solved]
    print()
    if mode == "algorithm":
        if len(remaining) == len(current) and len(current) > 1:
            print("바쁜 날은 워밍업만 풀어도 됩니다. 본 문제는 다음 날 이어서 나옵니다.")
        print("본 문제는 40분 안에 못 풀면 풀이를 보고 오답 노트를 남기세요: python scripts/new.py note <풀이 파일>")
    elif mode == "mock":
        print("타이머를 120분에 맞추고 시작하세요. 유형은 풀고 나서 헤더에 적습니다.")
    print("풀고 나면: 헤더 채우기 → python scripts/update_readme.py → 문제별로 커밋·푸시")


def show_review(today: dt.date, solutions: List[Solution]) -> None:
    notes_dir = ROOT / "notes"
    note_files = sorted(notes_dir.glob("*.md")) if notes_dir.exists() else []

    due = []  # (복습일, 문제, 링크, 노트 파일)
    all_note_text = ""
    for note in note_files:
        text = note.read_text(encoding="utf-8")
        all_note_text += text
        current_title = None
        for line in text.splitlines():
            title_match = NOTE_TITLE.match(line.strip())
            if title_match:
                current_title = (title_match.group(1), title_match.group(2))
                continue
            review_match = REVIEW_ITEM.match(line.strip())
            if not review_match or review_match.group(1) != " " or current_title is None:
                continue
            try:
                review_on = dt.date.fromisoformat(review_match.group(2))
            except ValueError:
                print(f"건너뜀 (복습 날짜 형식 오류): {note.relative_to(ROOT).as_posix()}", file=sys.stderr)
                continue
            if review_on <= today:
                due.append((review_on, current_title[0], current_title[1], note.relative_to(ROOT).as_posix()))

    print(f"[복기] 복습할 오답 노트 {len(due)}개")
    for review_on, title, link, note_path in sorted(due):
        print(f"  {title}  (복습일 {review_on}, {note_path})")
        if link:
            print(f"    {link}")
    if due:
        print("  → 풀이를 보지 않고 다시 풀어 본 뒤, 노트의 '- [ ]' 를 '- [x]' 로 바꿉니다.")

    # 한 번에 못 풀었는데 오답 노트에 아직 없는 이번 주 문제
    week_start = today - dt.timedelta(days=today.weekday())
    unnoted = [
        s
        for s in solutions
        if s.is_first_try is False
        and s.solved_on is not None
        and week_start <= s.solved_on <= today
        and s.path.name not in all_note_text
    ]
    print(f"\n[복기] 오답 노트가 없는 이번 주 X 문제 {len(unnoted)}개")
    for s in unnoted:
        print(f"  {s.problem}")
        print(f"    python scripts/new.py note {s.path.relative_to(ROOT).as_posix()}")

    print("\n복기를 마치면:")
    print("    git add notes")
    print(f'    git commit -m "[review] {today.isoformat()} 주간 복기"')
    print("    git push")


def main() -> int:
    setup_console()
    parser = argparse.ArgumentParser(description="오늘 풀 문제를 계획에서 꺼내 보여 준다.")
    parser.add_argument("--mode", choices=sorted(MODE_LABELS), help="요일 대신 이 계획을 본다")
    parser.add_argument("--date", type=dt.date.fromisoformat, help="기준 날짜 (YYYY-MM-DD, 미리 보기용)")
    args = parser.parse_args()

    today = args.date or dt.date.today()
    mode = args.mode or MODE_BY_WEEKDAY[today.weekday()]
    solutions = collect_solutions()
    solved_today = [s for s in solutions if s.solved_on == today]

    print(f"{today.isoformat()} ({WEEKDAY_NAMES[today.weekday()]}) · 오늘은 {MODE_LABELS[mode]}")
    if solved_today:
        print(f"오늘 푼 문제 {len(solved_today)}개: " + ", ".join(s.problem for s in solved_today))
    print()

    try:
        if mode == "review":
            show_review(today, solutions)
        else:
            show_plan(mode, today, solved_today)
    except PlanError as error:
        print(f"오류: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
