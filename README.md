# News 데이터 분석 시스템

직접 사이트에 접속하여 기사를 읽어야 트렌드를 분석할 수 있는 불편함을 해소하기 위한 사이트이다. 데이터 분석 시 주관적인 견해가 포함되는 문제점을 해결할 수 있고, 워드클라우드 기법을 사용하여 통계 자료의 시각적 효과를 높였다.

통계 자료의 경우 Crawling, 자연어 처리, 빈도 분석을 통해 제공된다.<br><br>

## Goals

1. Daum News 랭킹에서 순서대로 제목을 수집
2. 수집된 자료의 태그를 분석하여 정보 추출
3. 추출한 정보를 Maria DB에 저장
4. 저장된 정보를 이용하여 빈도 분석 진행
5. 워드클라우드 기법을 이용하여 시각화
6. 사용자가 웹 상에서 컨트롤 가능하도록 구현
<br><br>

## Techique
<br>

| Means | Explanation |
|:--------:|--------|
|개발 방법론|애자일 방법론을 적용하여 개인에게 책임 부여하고 주도적인 개발 환경 구성|
|기본 언어|Python|
|DBMS|MariaDB|
|Front end|HTML, CSS, jQuery, Ajax, Javascript, Bootstrap|
|Back end|Python, Django|
|데이터 수집|BeautifulSoup|
|형태소 분석기|Konlpy, Okit package|
|빈도 분석|Counter class|
|시각화|WorldCloud package|
|Web Framework|Django 3|
|편집기|Anaconda, Jupyter, Notebook, Pycharm 2020.1|

<br>
