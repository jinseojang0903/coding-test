"""new.py 와 update_readme.py 가 함께 쓰는 경로·헤더 파싱 도구.

표준 라이브러리만 사용한다. Python 3.8 이상, 윈도우·맥 공통.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# 스크립트를 어느 폴더에서 실행해도 저장소 루트를 기준으로 동작하게 한다
ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "templates"

# 통계에 포함할 풀이 폴더와 확장자
SOLUTION_DIRS = ("programmers", "baekjoon")
SOLUTION_EXTS = (".py", ".sql")

# 헤더에 적힌 한국어 키(공백 제거 후) → 내부 필드 이름
HEADER_KEYS = {
    "플랫폼": "platform",
    "문제": "problem",
    "링크": "link",
    "난이도": "level",
    "유형": "types",
    "풀이날짜": "date",
    "소요시간(분)": "minutes",
    "한번에성공(O/X)": "first_try",
    "핵심아이디어": "idea",
    "시간복잡도": "complexity",
}

# "# 키: 값" 또는 "-- 키: 값" 형태의 한 줄. 링크의 "https:" 때문에 키는 첫 콜론까지만 본다.
HEADER_LINE = re.compile(r"^\s*(?:#|--)\s*([^:]+?)\s*:\s*(.*?)\s*$")

# 헤더는 파일 맨 위에 있으므로 이 줄 수까지만 읽는다
MAX_HEADER_LINES = 30


def setup_console() -> None:
    """윈도우 터미널 종류와 상관없이 한글 출력이 깨지거나 죽지 않게 한다.

    Git Bash(MSYS) 는 UTF-8 로 화면에 그리지만 Python 은 cp949 로 내보내서 글자가 깨진다.
    그 경우만 UTF-8 로 바꾸고, PowerShell·cmd 는 원래 설정을 그대로 쓴다.
    """
    use_utf8 = (
        sys.platform == "win32"
        and "MSYSTEM" in os.environ
        and "PYTHONIOENCODING" not in os.environ
    )
    for stream in (sys.stdout, sys.stderr):
        try:
            if use_utf8:
                stream.reconfigure(encoding="utf-8", errors="replace")
            else:
                stream.reconfigure(errors="replace")
        except AttributeError:
            # reconfigure 가 없는 스트림(IDE 대체 콘솔 등)은 그대로 둔다
            pass


def read_header(path: Path) -> dict[str, str]:
    """풀이 파일 맨 위 주석 헤더를 읽어 {필드 이름: 값} 으로 돌려준다.

    주석이 아닌 첫 줄을 만나면 멈춘다. 헤더가 없으면 빈 dict 를 돌려준다.
    파일을 읽을 수 없으면 OSError / UnicodeDecodeError 를 그대로 올린다.
    """
    fields: dict[str, str] = {}
    # utf-8-sig: 윈도우 메모장이 붙이는 BOM 도 처리한다
    with path.open(encoding="utf-8-sig") as file:
        for line_no, line in enumerate(file):
            if line_no >= MAX_HEADER_LINES:
                break
            stripped = line.strip()
            if not stripped:
                continue
            if not stripped.startswith(("#", "--")):
                break
            match = HEADER_LINE.match(line)
            if not match:
                continue
            key = re.sub(r"\s+", "", match.group(1))
            name = HEADER_KEYS.get(key)
            if name and name not in fields:
                fields[name] = match.group(2)
    return fields


def parse_types(raw: str) -> list[str]:
    """'DFS, BFS' 처럼 쉼표로 구분한 유형 문자열을 목록으로 바꾼다."""
    return [part.strip() for part in raw.split(",") if part.strip()]


def render(template: str, values: dict[str, str]) -> str:
    """템플릿의 {{키}} 자리를 값으로 바꾼다.

    str.format 대신 단순 치환을 쓰는 이유: 풀이 코드에 중괄호가 있어도 깨지지 않게.
    """
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def write_text_lf(path: Path, text: str) -> None:
    """윈도우에서도 줄바꿈을 LF 로 저장해 커밋마다 줄바꿈 diff 가 생기지 않게 한다."""
    with path.open("w", encoding="utf-8", newline="\n") as file:
        file.write(text)
