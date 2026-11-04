"""템플릿을 복사해 새 풀이 파일·오답 노트·실전 모의 기록을 만든다.

사용 예:
  python scripts/new.py programmers lv2 42586 기능개발 --type 스택큐
  python scripts/new.py programmers sql 59034 모든_레코드_조회하기 --type SELECT
  python scripts/new.py baekjoon silver2 1260 DFS와_BFS --type DFS BFS
  python scripts/new.py note programmers/lv2/42586_기능개발.py
  python scripts/new.py mock

이미 같은 번호의 파일이 있으면 덮어쓰지 않고 종료 코드 1 로 끝난다.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path
from urllib.parse import quote

from common import (
    ROOT,
    TEMPLATE_DIR,
    parse_types,
    read_header,
    render,
    setup_console,
    write_text_lf,
)

PROGRAMMERS_LEVELS = ("lv0", "lv1", "lv2", "lv3", "lv4", "lv5", "sql")

# 백준 티어: bronze5 ~ ruby1, 티어가 없는 문제는 unrated
BAEKJOON_TIER = re.compile(r"^(?:(?:bronze|silver|gold|platinum|diamond|ruby)[1-5]|unrated)$")

# 윈도우·맥에서 파일 이름에 쓸 수 없는 문자
INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')


class UserInputError(Exception):
    """사용자가 고칠 수 있는 입력 오류. main 에서 메시지만 출력하고 종료한다."""


def to_filename_part(text: str) -> str:
    """파일 이름에 쓸 수 없는 문자를 지우고 공백을 _ 로 바꾼다."""
    cleaned = INVALID_FILENAME_CHARS.sub("", text).strip()
    return re.sub(r"\s+", "_", cleaned)


def problem_link(platform: str, number: str) -> str:
    if platform == "programmers":
        return f"https://school.programmers.co.kr/learn/courses/30/lessons/{number}"
    return f"https://www.acmicpc.net/problem/{number}"


def coming_sunday(today: dt.date) -> dt.date:
    """다음 복기일(일요일). 오늘이 일요일이면 다음 주 일요일."""
    days_ahead = 6 - today.weekday()
    return today + dt.timedelta(days=days_ahead or 7)


def relative_posix(path: Path) -> str:
    """저장소 루트 기준 경로를 / 구분자로 돌려준다 (git·README 에서 그대로 쓰기 위해)."""
    return path.relative_to(ROOT).as_posix()


def create_solution(args: argparse.Namespace) -> None:
    platform = args.platform
    level = args.level.lower()
    number = args.number
    title = " ".join(args.title).strip()
    types = [t.strip() for t in (args.type or []) if t.strip()]

    if not number.isdigit():
        raise UserInputError(f"문제 번호는 숫자여야 합니다: {number}")
    filename_title = to_filename_part(title)
    if not filename_title:
        raise UserInputError("문제 이름이 비어 있습니다.")

    if platform == "programmers":
        if level not in PROGRAMMERS_LEVELS:
            raise UserInputError(
                f"프로그래머스 레벨은 {', '.join(PROGRAMMERS_LEVELS)} 중 하나여야 합니다: {level}"
            )
        folder = ROOT / "programmers" / level
        template_name = "sql.sql" if level == "sql" else "programmers.py"
    else:
        if not BAEKJOON_TIER.match(level):
            raise UserInputError(
                f"백준 티어는 silver2, gold5 같은 형식(또는 unrated)이어야 합니다: {level}"
            )
        folder = ROOT / "baekjoon"
        template_name = "baekjoon.py"

    extension = Path(template_name).suffix
    target = folder / f"{number}_{filename_title}{extension}"

    # 이름만 다르게 적어서 같은 문제가 두 번 생기는 것을 막는다
    existing = sorted(folder.glob(f"{number}_*")) if folder.exists() else []
    if existing:
        raise UserInputError(f"이미 같은 번호의 파일이 있습니다: {relative_posix(existing[0])}")

    template = (TEMPLATE_DIR / template_name).read_text(encoding="utf-8")
    content = render(
        template,
        {
            "platform": platform,
            "problem": f"{number} {title}",
            "link": problem_link(platform, number),
            "level": level,
            "types": ", ".join(types),
            "date": dt.date.today().isoformat(),
        },
    )
    folder.mkdir(parents=True, exist_ok=True)
    write_text_lf(target, content)

    path_text = relative_posix(target)
    type_suffix = f" ({', '.join(types)})" if types else " (유형)"
    print(f"생성: {path_text}")
    if not types:
        print("※ --type 을 주지 않았습니다. 풀이 후 헤더의 '유형'을 채우세요.")
    print("\n풀이 후 헤더의 소요 시간·한 번에 성공·핵심 아이디어·시간복잡도를 채우고:")
    print("  python scripts/update_readme.py")
    print(f'  git add "{path_text}" README.md')
    print(f'  git commit -m "[{platform} {level}] {number} {title}{type_suffix}"')
    print("  git push")


def resolve_inside_root(raw_path: str) -> Path:
    """입력 경로를 현재 폴더 → 저장소 루트 순으로 찾고, 저장소 밖이면 거부한다."""
    for base in (Path.cwd(), ROOT):
        candidate = (base / raw_path).resolve()
        if candidate.is_file():
            try:
                candidate.relative_to(ROOT)
            except ValueError:
                raise UserInputError(f"저장소 밖의 파일은 쓸 수 없습니다: {candidate}") from None
            return candidate
    raise UserInputError(f"풀이 파일을 찾을 수 없습니다: {raw_path}")


def create_note(args: argparse.Namespace) -> None:
    solution = resolve_inside_root(args.solution)
    fields = read_header(solution)
    if not fields.get("platform"):
        raise UserInputError(f"풀이 헤더를 읽지 못했습니다: {relative_posix(solution)}")

    types = parse_types(fields.get("types", ""))
    note_type = (args.type or (types[0] if types else "")).strip()
    if not note_type:
        raise UserInputError("풀이 헤더의 '유형'을 먼저 채우거나 --type 으로 노트 이름을 정하세요.")

    note_name = to_filename_part(note_type)
    if not note_name:
        raise UserInputError(f"노트 이름으로 쓸 수 없는 유형입니다: {note_type}")
    note_path = ROOT / "notes" / f"{note_name}.md"
    today = dt.date.today()
    entry = render(
        (TEMPLATE_DIR / "note.md").read_text(encoding="utf-8"),
        {
            "problem": fields.get("problem", solution.stem),
            "link": fields.get("link", ""),
            "types": ", ".join(types) or note_type,
            "solution_name": solution.name,
            # notes/ 폴더 기준 상대 링크. 한글·공백이 있어도 GitHub 에서 열리게 인코딩한다.
            "solution_path": "../" + quote(relative_posix(solution)),
            "date": today.isoformat(),
            "review_date": coming_sunday(today).isoformat(),
        },
    )

    # 유형별로 한 파일에 계속 쌓는다
    if note_path.exists():
        current = note_path.read_text(encoding="utf-8")
        content = current.rstrip("\n") + "\n\n" + entry
    else:
        content = f"# {note_type} 오답 노트\n\n" + entry
    note_path.parent.mkdir(parents=True, exist_ok=True)
    write_text_lf(note_path, content)

    path_text = relative_posix(note_path)
    print(f"추가: {path_text}")
    print("\n막힌 지점·아이디어를 한 줄씩 채우고:")
    print(f'  git add "{path_text}"')
    print(f'  git commit -m "[note] {note_type} - {fields.get("problem", solution.stem)}"')
    print("  git push")


def create_mock(args: argparse.Namespace) -> None:
    today = dt.date.today().isoformat()
    target = ROOT / "mock-tests" / f"{today}.md"
    if target.exists():
        raise UserInputError(f"오늘 모의 기록이 이미 있습니다: {relative_posix(target)}")

    content = render((TEMPLATE_DIR / "mock.md").read_text(encoding="utf-8"), {"date": today})
    target.parent.mkdir(parents=True, exist_ok=True)
    write_text_lf(target, content)

    path_text = relative_posix(target)
    print(f"생성: {path_text}")
    print("\n각 문제는 new.py 로 따로 만들어 문제별로 커밋하고, 모의 기록은 마지막에:")
    print(f'  git add "{path_text}"')
    print(f'  git commit -m "[mock] {today} 실전 모의"')
    print("  git push")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="코딩테스트 풀이 파일을 템플릿으로 만든다.")
    sub = parser.add_subparsers(dest="command", required=True)

    for platform, level_help in (
        ("programmers", "lv0~lv5 또는 sql"),
        ("baekjoon", "티어 (예: silver2, gold5)"),
    ):
        cmd = sub.add_parser(platform, help=f"{platform} 풀이 파일 생성")
        cmd.add_argument("level", help=level_help)
        cmd.add_argument("number", help="문제 번호")
        cmd.add_argument("title", nargs="+", help="문제 이름 (공백이 있으면 _ 로 바뀐다)")
        cmd.add_argument("--type", nargs="+", help="유형. 여러 개면 공백으로 구분 (예: --type DFS BFS)")
        cmd.set_defaults(handler=create_solution, platform=platform)

    note = sub.add_parser("note", help="풀이 파일 헤더를 읽어 유형별 오답 노트에 항목 추가")
    note.add_argument("solution", help="풀이 파일 경로 (예: programmers/lv2/42586_기능개발.py)")
    note.add_argument("--type", help="노트 파일 이름으로 쓸 유형 (기본: 헤더의 첫 번째 유형)")
    note.set_defaults(handler=create_note)

    mock = sub.add_parser("mock", help="오늘 날짜의 실전 모의 기록 파일 생성")
    mock.set_defaults(handler=create_mock)

    return parser


def main() -> int:
    setup_console()
    args = build_parser().parse_args()
    try:
        args.handler(args)
    except UserInputError as error:
        print(f"오류: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
