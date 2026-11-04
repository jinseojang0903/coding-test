# coding-test

취업 준비를 위해 코딩테스트 풀이를 매일 기록하는 저장소입니다.

- **언어**: Python (알고리즘), SQL
- **플랫폼**: 프로그래머스 (주), 백준 (보조)
- **원칙**: 실제로 푼 문제만 올립니다. 풀이마다 소요 시간, 한 번에 성공했는지, 핵심 아이디어를 남겨 약한 유형을 찾는 데 씁니다.

## 학습 루틴

인턴과 병행하고 있어서 평일에는 적게, 주말에는 실전과 복기에 시간을 씁니다.

| 요일 | 할 일 | 분량 | 기록 위치 |
|---|---|---|---|
| 월 · 수 · 금 | 알고리즘 (프로그래머스 위주, 백준 보조) | 1문제 이상 | `programmers/lv*/`, `baekjoon/` |
| 화 · 목 | SQL | 1문제 이상 | `programmers/sql/` |
| 토 | 실전 모의 (시간 제한을 두고 3문제) | 3문제 | `mock-tests/` + 문제별 풀이 파일 |
| 일 | 복기 (오답 노트 복습, 틀린 문제 다시 풀기) | 이번 주 오답 | `notes/` |

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
├─ templates/             # 풀이·노트·모의 템플릿
└─ scripts/               # new.py, update_readme.py
```

파일 이름은 `{문제번호}_{문제이름}.py` (SQL 은 `.sql`) 이고, 문제 이름의 공백은 `_` 로 바뀝니다.

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

### 매일 하는 흐름

```bash
# 1) 문제 파일 만들기
python scripts/new.py programmers lv2 42586 기능개발 --type 스택큐

# 2) 풀고 헤더 채우기 (소요 시간, 한 번에 성공, 핵심 아이디어, 시간복잡도)

# 3) 통계 갱신
python scripts/update_readme.py

# 4) 커밋·푸시 (new.py 가 출력해 준 명령을 그대로 써도 됩니다)
git add programmers/lv2/42586_기능개발.py README.md
git commit -m "[programmers lv2] 42586 기능개발 (스택큐)"
git push
```

### 한글 파일 이름 팁

`git status` 에서 한글 파일 이름이 `\354\240...` 처럼 보이면 아래를 한 번 실행합니다.

```bash
git config --global core.quotepath false
```
