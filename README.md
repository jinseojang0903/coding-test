# coding-test

취업 준비를 위해 코딩테스트 풀이를 매일 기록하는 저장소입니다.

- **언어**: Python (알고리즘), SQL
- **플랫폼**: 프로그래머스 (주), 백준 (보조)
- **원칙**: 실제로 푼 문제만 올립니다. 풀이마다 소요 시간, 한 번에 성공했는지, 핵심 아이디어를 남겨 약한 유형을 찾는 데 씁니다.

## 학습 루틴

인턴과 병행하고 있어서 평일에는 적게, 주말에는 실전과 복기에 시간을 씁니다.
평일은 **워밍업 1문제 + 같은 유형의 본 문제 1문제**를 풉니다. 풀 문제는 [`plan/`](plan/)에 순서대로 정해 두었습니다.

| 요일 | 할 일 | 분량 | 계획 |
|---|---|---|---|
| 월 · 수 · 금 | 알고리즘 (고득점 Kit 유형 순서) | 워밍업 + 본 문제 | [`plan/algorithm.md`](plan/algorithm.md) |
| 화 · 목 | SQL (SQL 고득점 Kit) | 워밍업 + 본 문제 | [`plan/sql.md`](plan/sql.md) |
| 토 | 실전 모의 (기업 기출 3문제, 120분) | 3문제 | [`plan/mock.md`](plan/mock.md) |
| 일 | 복기 (복습일이 된 오답 노트 다시 풀기) | 이번 주 오답 | `notes/` |

- 바쁜 날은 워밍업만 풉니다. 본 문제는 다음 날 이어서 풉니다.
- 본 문제는 40분 안에 못 풀면 풀이를 보고 오답 노트를 남깁니다.

## 진행 현황

아래 영역은 `python scripts/update_readme.py` 가 풀이 파일 헤더를 읽어 자동으로 만듭니다. 직접 고치지 마세요.

<!-- STATS:START -->
아직 기록된 풀이가 없습니다. `python scripts/new.py programmers lv1 ...` 로 첫 문제를 만들어 보세요.
<!-- STATS:END -->

## 커밋 규칙

| 종류 | 형식 | 예시 |
|---|---|---|
| 풀이 | `[플랫폼 레벨] 문제번호 문제이름 (유형)` | `[programmers lv2] 42586 기능개발 (스택큐)` |
| SQL | 위와 같음 (레벨 자리에 `sql`) | `[programmers sql] 59034 모든 레코드 조회하기 (SELECT)` |
| 백준 | 위와 같음 (레벨 자리에 티어) | `[baekjoon silver2] 1260 DFS와 BFS (DFS, BFS)` |
| 오답 노트 | `[note] 유형 - 문제` | `[note] 스택큐 - 42586 기능개발` |
| 복기 | `[review] 내용` | `[review] 42586 기능개발 다시 풀기` |
| 실전 모의 | `[mock] 날짜 실전 모의` | `[mock] 2026-11-07 실전 모의` |

- **문제 하나당 커밋 하나.** README 통계 변경은 그 문제 커밋에 같이 넣습니다.
- **`main` 브랜치에 바로 커밋하고 푸시합니다.** GitHub 잔디는 기본 브랜치에 들어간 커밋만 셉니다.
- 날짜를 바꾼 커밋, 빈 커밋, 의미 없는 수정은 만들지 않습니다.

### 커밋 이메일 확인

커밋 이메일이 GitHub 계정에 등록된 이메일과 다르면 잔디에 표시되지 않습니다.

```bash
git config user.email            # 이 저장소에서 실제로 쓰는 이메일
git config --global user.email   # 전역 설정
```

- 출력된 이메일이 GitHub **Settings → Emails** 목록에 있는지 확인합니다.
- 다르면 이 저장소에서만 바꿉니다: `git config user.email "본인@example.com"`
- 이미 올린 커밋의 이메일은 `git log -1 --format="%an <%ae>"` 로 확인할 수 있습니다.

## 사용법

Python 3.8 이상만 있으면 됩니다. 외부 라이브러리는 쓰지 않습니다.
아래 명령은 저장소 루트에서 실행합니다. 맥에서는 `python` 대신 `python3` 을 씁니다.

### 폴더 구조

```
coding-test/
├─ README.md
├─ programmers/
│  ├─ lv1/ lv2/ lv3/      # 필요하면 lv0, lv4 도 자동 생성
│  └─ sql/
├─ baekjoon/
├─ mock-tests/            # 토요일 실전 모의 기록 (날짜.md)
├─ notes/                 # 오답 노트 (유형별 md)
├─ plan/                  # 풀 문제 순서 (알고리즘 · SQL · 실전 모의)
├─ templates/             # 풀이·노트·모의 템플릿
└─ scripts/               # today.py, new.py, update_readme.py
```

파일 이름은 `{문제번호}_{문제이름}.py` (SQL 은 `.sql`) 이고, 문제 이름의 공백은 `_` 로 바뀝니다.
`[1차]` 같은 대괄호와 `/` 는 파일 이름에서 빠집니다.

### 0. 오늘 풀 문제 확인

```bash
python scripts/today.py
```

요일에 맞는 계획에서 아직 안 푼 첫 문제들을 보여 주고, 바로 쓸 수 있는 `new.py` 명령을 출력합니다.
`programmers/` 에 같은 번호의 파일이 있으면 푼 것으로 봅니다. 따로 체크할 필요가 없습니다.

```
2026-11-04 (수) · 오늘은 알고리즘

[알고리즘] 1일차 · 해시  (완료 0/35일차)
  워밍업: 1845 폰켓몬 (lv1)
    https://school.programmers.co.kr/learn/courses/30/lessons/1845
    python scripts/new.py programmers lv1 1845 "폰켓몬" --type "해시"
  본 문제: 42577 전화번호 목록 (lv2)
    ...
```

- 요일과 다른 계획을 보려면 `--mode algorithm|sql|mock|review` 를 붙입니다. 예: 토요일에 SQL 을 더 풀고 싶을 때 `--mode sql`.
- 일요일에는 복습일이 된 오답 노트와, 한 번에 못 풀었는데 오답 노트가 없는 이번 주 문제를 보여 줍니다.
- 순서를 바꾸거나 문제를 더하려면 `plan/*.md` 의 표를 직접 고칩니다.

### 1. 새 문제 만들기

```bash
python scripts/new.py programmers lv2 42586 기능개발 --type 스택큐
python scripts/new.py programmers sql 59034 모든 레코드 조회하기 --type SELECT
python scripts/new.py baekjoon silver2 1260 DFS와 BFS --type DFS BFS
```

템플릿이 복사되고 플랫폼, 문제, 링크, 난이도, 유형, 오늘 날짜가 헤더에 채워집니다.
풀이가 끝나면 나머지 항목을 채웁니다.

```python
# 소요 시간(분): 35
# 한 번에 성공(O/X): X
# 핵심 아이디어: 남은 일수를 계산해 앞 기능보다 늦게 끝나는 지점에서 배포를 끊는다
# 시간복잡도: O(n)
```

### 2. 통계 갱신

```bash
python scripts/update_readme.py
```

- 빈 헤더 항목이 있으면 `확인 필요:` 로 알려 줍니다. 통계는 그대로 만들어집니다.
- `--dry-run` 을 붙이면 README 를 쓰지 않고 결과만 출력합니다.

### 3. 오답 노트

한 번에 못 푼 문제는 풀이 파일을 지정해 오답 노트에 항목을 추가합니다.

```bash
python scripts/new.py note programmers/lv2/42586_기능개발.py
```

헤더의 첫 번째 유형 이름으로 `notes/스택큐.md` 같은 파일에 항목이 쌓입니다. 복습 날짜는 다가오는 일요일로 들어갑니다.
막힌 지점과 다음에 떠올릴 아이디어는 한 줄씩만 씁니다. 일요일에 복습한 뒤 `- [ ]` 를 `- [x]` 로 바꿉니다.

### 4. 실전 모의 (토요일)

```bash
python scripts/new.py mock
```

`mock-tests/오늘날짜.md` 가 생깁니다. 모의에서 푼 문제는 1번처럼 따로 만들어 문제별로 커밋하고, 모의 기록은 마지막에 `[mock]` 으로 커밋합니다.
실전처럼 유형을 모르고 풀도록 모의 문제에는 `--type` 이 없습니다. 풀고 나서 헤더에 유형을 적습니다.

### 매일 하는 흐름

```bash
# 1) 오늘 풀 문제 확인
python scripts/today.py

# 2) 출력된 명령으로 워밍업 문제 파일 만들기 → 풀고 헤더 채우기
python scripts/new.py programmers lv1 1845 "폰켓몬" --type "해시"

# 3) 통계 갱신 후 커밋·푸시 (new.py 가 출력해 준 명령을 그대로 써도 됩니다)
python scripts/update_readme.py
git add programmers/lv1/1845_폰켓몬.py README.md
git commit -m "[programmers lv1] 1845 폰켓몬 (해시)"
git push

# 4) 본 문제도 2~3번을 똑같이 반복 (문제 하나당 커밋 하나)
```

### 한글 파일 이름 팁

`git status` 에서 한글 파일 이름이 `\354\240...` 처럼 보이면 아래를 한 번 실행합니다.

```bash
git config --global core.quotepath false
```
