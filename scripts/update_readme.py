"""풀이 파일 헤더를 읽어 README.md 의 진행 현황 영역을 다시 만든다.

<!-- STATS:START --> 와 <!-- STATS:END --> 사이만 덮어쓰고 나머지는 건드리지 않는다.

사용 예:
  python scripts/update_readme.py            # README 갱신
  python scripts/update_readme.py --dry-run  # 쓰지 않고 결과만 출력

표식이 없거나 여러 개면 README 를 건드리지 않고 종료 코드 1 로 끝난다.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import statistics
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
from urllib.parse import quote

from common import (
    ROOT,
    SOLUTION_DIRS,
    SOLUTION_EXTS,
    parse_types,
    read_header,
    setup_console,
    write_text_lf,
)

README = ROOT / "README.md"
START_MARK = "<!-- STATS:START -->"
END_MARK = "<!-- STATS:END -->"
RECENT_LIMIT = 10

PLATFORM_ORDER = {"programmers": 0, "baekjoon": 1}
PROGRAMMERS_LEVEL_ORDER = {"lv0": 0, "lv1": 1, "lv2": 2, "lv3": 3, "lv4": 4, "lv5": 5, "sql": 6}
BAEKJOON_TIERS = ("bronze", "silver", "gold", "platinum", "diamond", "ruby")
TIER_PATTERN = re.compile(r"^([a-z]+)(\d)$")


@dataclass
class Solution:
    path: Path
    platform: str
    level: str
    problem: str
    link: str
    types: List[str]
    solved_on: Optional[dt.date]
    minutes: Optional[int]
    is_first_try: Optional[bool]
    # 아직 안 채운 헤더 항목. 통계는 내되 갱신 시 알려 준다.
    missing: List[str] = field(default_factory=list)


def parse_solution(path: Path) -> Optional[Solution]:
    """헤더를 Solution 으로 바꾼다. 플랫폼 항목이 없으면 풀이 파일로 보지 않는다."""
    fields = read_header(path)
    if not fields.get("platform"):
        return None

    missing: List[str] = []

    try:
        solved_on: Optional[dt.date] = dt.date.fromisoformat(fields.get("date", ""))
    except ValueError:
        solved_on = None
        missing.append("풀이 날짜(YYYY-MM-DD)")

    minutes_text = fields.get("minutes", "")
    minutes = int(minutes_text) if minutes_text.isdigit() else None
    if minutes is None:
        missing.append("소요 시간(분)")

    first_try_text = fields.get("first_try", "").upper()
    is_first_try = {"O": True, "X": False}.get(first_try_text)
    if is_first_try is None:
        missing.append("한 번에 성공(O/X)")

    types = parse_types(fields.get("types", ""))
    if not types:
        missing.append("유형")
    if not fields.get("idea"):
        missing.append("핵심 아이디어")
    if fields.get("complexity", "").replace(" ", "") in ("", "O()"):
        missing.append("시간복잡도")

    return Solution(
        path=path,
        platform=fields["platform"].lower(),
        level=fields.get("level", "").lower() or "-",
        problem=fields.get("problem", path.stem),
        link=fields.get("link", ""),
        types=types,
        solved_on=solved_on,
        minutes=minutes,
        is_first_try=is_first_try,
        missing=missing,
    )


def collect_solutions() -> List[Solution]:
    solutions: List[Solution] = []
    for dirname in SOLUTION_DIRS:
        folder = ROOT / dirname
        if not folder.exists():
            continue
        for path in sorted(folder.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in SOLUTION_EXTS:
                continue
            solution = parse_solution(path)
            if solution is None:
                print(f"건너뜀 (헤더 없음): {path.relative_to(ROOT).as_posix()}", file=sys.stderr)
                continue
            solutions.append(solution)
    return solutions


def level_sort_key(level: str) -> tuple:
    """프로그래머스 lv0→sql, 백준 bronze5→ruby1 순, 나머지는 이름순."""
    if level in PROGRAMMERS_LEVEL_ORDER:
        return (0, PROGRAMMERS_LEVEL_ORDER[level], 0, level)
    match = TIER_PATTERN.match(level)
    if match and match.group(1) in BAEKJOON_TIERS:
        # 같은 티어 안에서는 숫자가 클수록 쉽다 (bronze5 < bronze1)
        return (1, BAEKJOON_TIERS.index(match.group(1)), -int(match.group(2)), level)
    return (2, 0, 0, level)


def cell(text: str) -> str:
    """표 칸 안에서 | 가 칸 구분자로 해석되지 않게 한다."""
    return text.replace("|", "\\|")


def build_stats(solutions: List[Solution], today: dt.date) -> str:
    if not solutions:
        return (
            "아직 기록된 풀이가 없습니다. "
            "`python scripts/new.py programmers lv1 ...` 로 첫 문제를 만들어 보세요."
        )

    lines: List[str] = []

    # 1) 요약
    week_start = today - dt.timedelta(days=today.weekday())  # 월요일 시작
    week_end = week_start + dt.timedelta(days=6)
    this_week = sum(1 for s in solutions if s.solved_on and week_start <= s.solved_on <= week_end)
    first_try_known = [s.is_first_try for s in solutions if s.is_first_try is not None]
    first_try_rate = (
        f"{round(100 * sum(first_try_known) / len(first_try_known))}%" if first_try_known else "-"
    )
    minutes = [s.minutes for s in solutions if s.minutes is not None]
    average_minutes = f"{round(statistics.mean(minutes))}분" if minutes else "-"
    week_label = f"{week_start:%m/%d}~{week_end:%m/%d}"

    lines += [
        f"_마지막 갱신: {today.isoformat()}_",
        "",
        f"| 총 풀이 | 이번 주 ({week_label}) | 한 번에 성공률 | 평균 소요 시간 |",
        "|:---:|:---:|:---:|:---:|",
        f"| **{len(solutions)}** | {this_week} | {first_try_rate} | {average_minutes} |",
        "",
    ]

    # 2) 플랫폼·난이도별
    by_level = Counter((s.platform, s.level) for s in solutions)
    lines += ["#### 플랫폼·난이도별", "", "| 플랫폼 | 난이도 | 풀이 수 |", "|---|---|:---:|"]
    for (platform, level), count in sorted(
        by_level.items(),
        key=lambda item: (PLATFORM_ORDER.get(item[0][0], 99), item[0][0], level_sort_key(item[0][1])),
    ):
        lines.append(f"| {cell(platform)} | {cell(level)} | {count} |")
    by_platform = Counter(s.platform for s in solutions)
    platform_summary = " · ".join(
        f"{name} {count}"
        for name, count in sorted(by_platform.items(), key=lambda item: PLATFORM_ORDER.get(item[0], 99))
    )
    lines += ["", f"플랫폼 합계: {platform_summary}", ""]

    # 3) 유형별 (한 문제에 유형이 여러 개면 각각 센다)
    by_type = Counter(t for s in solutions for t in s.types)
    lines += ["#### 유형별", ""]
    if by_type:
        lines += ["| 유형 | 풀이 수 |", "|---|:---:|"]
        for type_name, count in sorted(by_type.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {cell(type_name)} | {count} |")
    else:
        lines.append("유형이 기록된 풀이가 없습니다.")
    lines.append("")

    # 4) 최근 풀이
    recent = sorted(
        solutions,
        key=lambda s: (s.solved_on or dt.date.min, s.path.as_posix()),
        reverse=True,
    )[:RECENT_LIMIT]
    lines += [
        f"#### 최근 풀이 {len(recent)}개",
        "",
        "| 날짜 | 문제 | 플랫폼 | 난이도 | 유형 | 소요(분) | 한 번에 | 풀이 |",
        "|---|---|---|---|---|:---:|:---:|:---:|",
    ]
    for s in recent:
        title = f"[{cell(s.problem)}]({s.link})" if s.link else cell(s.problem)
        solution_link = f"[보기]({quote(s.path.relative_to(ROOT).as_posix())})"
        first_try = {True: "O", False: "X", None: "-"}[s.is_first_try]
        lines.append(
            f"| {s.solved_on.isoformat() if s.solved_on else '-'} | {title} | {cell(s.platform)} "
            f"| {cell(s.level)} | {cell(', '.join(s.types)) or '-'} "
            f"| {s.minutes if s.minutes is not None else '-'} | {first_try} | {solution_link} |"
        )

    return "\n".join(lines)


def replace_stats(readme_text: str, stats: str) -> str:
    """표식 사이만 바꾼 README 전문을 돌려준다. 표식이 잘못되면 ValueError."""
    if readme_text.count(START_MARK) != 1 or readme_text.count(END_MARK) != 1:
        raise ValueError(f"README 에 {START_MARK} 와 {END_MARK} 가 각각 정확히 하나씩 있어야 합니다.")
    start = readme_text.index(START_MARK) + len(START_MARK)
    end = readme_text.index(END_MARK)
    if end < start:
        raise ValueError(f"{END_MARK} 가 {START_MARK} 보다 앞에 있습니다.")
    return readme_text[:start] + "\n" + stats + "\n" + readme_text[end:]


def main() -> int:
    setup_console()
    parser = argparse.ArgumentParser(description="README 진행 현황 표를 갱신한다.")
    parser.add_argument("--dry-run", action="store_true", help="README 를 쓰지 않고 결과만 출력")
    args = parser.parse_args()

    solutions = collect_solutions()
    stats = build_stats(solutions, dt.date.today())

    for s in solutions:
        if s.missing:
            print(
                f"확인 필요: {s.path.relative_to(ROOT).as_posix()} → 비어 있음: {', '.join(s.missing)}",
                file=sys.stderr,
            )

    if args.dry_run:
        print(stats)
        return 0

    try:
        current = README.read_text(encoding="utf-8")
        updated = replace_stats(current, stats)
    except (OSError, ValueError) as error:
        print(f"오류: {error}", file=sys.stderr)
        return 1

    if updated == current:
        print(f"변경 없음 (풀이 {len(solutions)}개)")
    else:
        write_text_lf(README, updated)
        print(f"README 갱신 완료 (풀이 {len(solutions)}개)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
