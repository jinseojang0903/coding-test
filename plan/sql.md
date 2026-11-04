# SQL 계획 (화 · 목)

하루에 **워밍업 1문제 + 본 문제 1문제**를 풉니다. 두 문제는 같은 문법을 쓰고, 본 문제가 더 어렵습니다.
프로그래머스 [SQL 고득점 Kit](https://school.programmers.co.kr/learn/challenges?tab=sql_practice_kit)에서 골랐습니다.

- SQL 은 문제가 짧아서 두 문제를 다 푸는 것을 기본으로 합니다.
- 풀이 파일은 레벨과 상관없이 `programmers/sql/` 에 들어갑니다.
- 문제 번호·이름·레벨은 2026-11-04 에 프로그래머스 페이지에서 확인했습니다.

| 일차 | 유형 | 구분 | 번호 | 문제 | 레벨 |
|:-:|---|---|---|---|:-:|
| 1 | SELECT | 워밍업 | 59034 | [모든 레코드 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/59034) | lv1 |
| 1 | SELECT | 본 문제 | 59404 | [여러 기준으로 정렬하기](https://school.programmers.co.kr/learn/courses/30/lessons/59404) | lv1 |
| 2 | SELECT | 워밍업 | 59036 | [아픈 동물 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/59036) | lv1 |
| 2 | SELECT | 본 문제 | 131120 | [3월에 태어난 여성 회원 목록 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/131120) | lv2 |
| 3 | SELECT | 워밍업 | 59405 | [상위 n개 레코드](https://school.programmers.co.kr/learn/courses/30/lessons/59405) | lv1 |
| 3 | SELECT | 본 문제 | 131536 | [재구매가 일어난 상품과 회원 리스트 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/131536) | lv2 |
| 4 | 집계함수 | 워밍업 | 59415 | [최댓값 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/59415) | lv1 |
| 4 | 집계함수 | 본 문제 | 59406 | [동물 수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/59406) | lv2 |
| 5 | 집계함수 | 워밍업 | 59408 | [중복 제거하기](https://school.programmers.co.kr/learn/courses/30/lessons/59408) | lv2 |
| 5 | 집계함수 | 본 문제 | 131115 | [가격이 제일 비싼 식품의 정보 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/131115) | lv2 |
| 6 | IS NULL | 워밍업 | 59039 | [이름이 없는 동물의 아이디](https://school.programmers.co.kr/learn/courses/30/lessons/59039) | lv1 |
| 6 | IS NULL | 본 문제 | 59410 | [NULL 처리하기](https://school.programmers.co.kr/learn/courses/30/lessons/59410) | lv2 |
| 7 | GROUP BY | 워밍업 | 59040 | [고양이와 개는 몇 마리 있을까](https://school.programmers.co.kr/learn/courses/30/lessons/59040) | lv2 |
| 7 | GROUP BY | 본 문제 | 59041 | [동명 동물 수 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/59041) | lv2 |
| 8 | GROUP BY | 워밍업 | 132202 | [진료과별 총 예약 횟수 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/132202) | lv2 |
| 8 | GROUP BY | 본 문제 | 59412 | [입양 시각 구하기(1)](https://school.programmers.co.kr/learn/courses/30/lessons/59412) | lv2 |
| 9 | GROUP BY | 워밍업 | 133026 | [성분으로 구분한 아이스크림 총 주문량](https://school.programmers.co.kr/learn/courses/30/lessons/133026) | lv2 |
| 9 | GROUP BY | 본 문제 | 144855 | [카테고리 별 도서 판매량 집계하기](https://school.programmers.co.kr/learn/courses/30/lessons/144855) | lv3 |
| 10 | GROUP BY | 워밍업 | 151137 | [자동차 종류 별 특정 옵션이 포함된 자동차 수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/151137) | lv2 |
| 10 | GROUP BY | 본 문제 | 131123 | [즐겨찾기가 가장 많은 식당 정보 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/131123) | lv3 |
| 11 | GROUP BY | 워밍업 | 164668 | [조건에 맞는 사용자와 총 거래금액 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/164668) | lv3 |
| 11 | GROUP BY | 본 문제 | 59413 | [입양 시각 구하기(2)](https://school.programmers.co.kr/learn/courses/30/lessons/59413) | lv4 |
| 12 | 문자열·날짜 | 워밍업 | 59046 | [루시와 엘라 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/59046) | lv2 |
| 12 | 문자열·날짜 | 본 문제 | 59409 | [중성화 여부 파악하기](https://school.programmers.co.kr/learn/courses/30/lessons/59409) | lv2 |
| 13 | 문자열·날짜 | 워밍업 | 59414 | [DATETIME에서 DATE로 형 변환](https://school.programmers.co.kr/learn/courses/30/lessons/59414) | lv2 |
| 13 | 문자열·날짜 | 본 문제 | 59411 | [오랜 기간 보호한 동물(2)](https://school.programmers.co.kr/learn/courses/30/lessons/59411) | lv3 |
| 14 | 문자열·날짜 | 워밍업 | 151138 | [자동차 대여 기록에서 장기/단기 대여 구분하기](https://school.programmers.co.kr/learn/courses/30/lessons/151138) | lv1 |
| 14 | 문자열·날짜 | 본 문제 | 131113 | [조건별로 분류하여 주문상태 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/131113) | lv3 |
| 15 | 문자열·날짜 | 워밍업 | 157342 | [자동차 평균 대여 기간 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/157342) | lv2 |
| 15 | 문자열·날짜 | 본 문제 | 164671 | [조회수가 가장 많은 중고거래 게시판의 첨부파일 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/164671) | lv3 |
| 16 | JOIN | 워밍업 | 144854 | [조건에 맞는 도서와 저자 리스트 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/144854) | lv2 |
| 16 | JOIN | 본 문제 | 59042 | [없어진 기록 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/59042) | lv3 |
| 17 | JOIN | 워밍업 | 59043 | [있었는데요 없었습니다](https://school.programmers.co.kr/learn/courses/30/lessons/59043) | lv3 |
| 17 | JOIN | 본 문제 | 59044 | [오랜 기간 보호한 동물(1)](https://school.programmers.co.kr/learn/courses/30/lessons/59044) | lv3 |
| 18 | JOIN | 워밍업 | 59045 | [보호소에서 중성화한 동물](https://school.programmers.co.kr/learn/courses/30/lessons/59045) | lv4 |
| 18 | JOIN | 본 문제 | 133027 | [주문량이 많은 아이스크림들 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/133027) | lv4 |

다 끝내면 SQL 고득점 Kit 의 남은 문제를 같은 방식으로 이 표에 이어 붙입니다.
