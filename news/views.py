import json
import time

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Crawling 관련
# ----------------------------------------------------------------------------------------------
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote  # 한글 처리 함수
from urllib.error import HTTPError

from django.urls import reverse
from requests import get        # GET 방식 호출

# ncaptcha를 우회
from news.models import News

# Wordcloud 관련
# ----------------------------------------------------------------------------------------------
import os
import pandas as pd
import pymysql
import re
import platform

from konlpy.tag import Twitter
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import rc

rc('font', family='Malgun Gothic')
plt.rcParams["font.size"] = 12         # 글자 크기
plt.rcParams['axes.unicode_minus'] = False # minus 부호는 unicode 적용시 한글이 깨짐으로 설정


def getbs(url):
    try:
        web = get(url).content
        bs = BeautifulSoup(str(web, 'utf-8'), 'html.parser') # parser: 태그 해석기, html 가능
        # 아래도 동일
        # bs = BeautifulSoup(html, 'html.parser', from_encoding='utf-8') # parser: 태그 해석기, html 가능
    except HTTPError as e:
        print(e)
        return None
    else:
        return bs
# ----------------------------------------------------------------------------------------------


# Create your views here.
# def index(request):
#     return HttpResponse("news first page")

# 시작 페이지 Template 적용
# def index(request):
#     return render(request, 'index.html') # /Crawling/news/templates/index.html

# news table list
def index(request):
    result_set = News.objects.all()  # 모든 레코드를 가져오는 명령어, SELECT ~
    result_set = {'result_set': result_set} # key, value
    return render(request, 'index.html', result_set) # /news/templates/index.html


def crawling(request):
    bs = getbs('https://news.daum.net/ranking/popular')
    # #mArticle > div.rank_news > ul.list_news2
    tags = bs.select('#mArticle > div.rank_news > ul.list_news2 > li')

    for i, tag in enumerate(tags):
        title = tag.select('a.link_txt')[0].string
        article = '{0:2d}. {1}'.format(i + 1, title)
        link = tag.select('a')[0]['href']
        # print('-> article: {0}'.format(article))
        # print('-> link: {0}'.format(link))

        # MariaDB 연동
        # content = request.POST['content']
        # print('등록할 내용 content: ' + content)
        news = News(article = article, link = link) # Todo class 객체 생성, content 컬럼에 값 할당
        news.save() # DBMS에 저장 실행, INSERT SQL 실행

    # print('-> crawling')
    #
    time.sleep(3)  # 3초 실행 중지
    # 처리 건수 출력
    data = {
        "cnt": i+1,
    }

    return HttpResponse(json.dumps(data), content_type="application/json")

# news table list
def index(request):
    result_set = News.objects.all()  # 모든 레코드를 가져오는 명령어, SELECT ~
    result_set = {'result_set': result_set} # key, value
    return render(request, 'index.html', result_set) # /news/templates/index.html

def delete(request):
    newsno = request.POST['newsno']
    print('삭제할 번호 newsno: ' + newsno)
    news = News.objects.get(newsno=newsno) # id 컬럼에 값을 할당하여 삭제할 레코드를 가져옴
    news.delete() # DBMS에서 삭제 실행, DELETE FROM ~
    return HttpResponseRedirect(reverse('news:index')) # 목록으로 이동

def delete_all(request):
    time.sleep(3)  # 3초 실행 중지
    News.objects.all().delete()

    data = {
        "msg": "모든 데이터를 삭제했습니다.",
    }

    return HttpResponse(json.dumps(data), content_type="application/json")

def trend_analysis(request):
    print("데이터분석 시작.")
    conn = pymysql.connect(host='localhost', user='pyuser', password='1234',
                           db='crawling', charset='utf8')

    cursor = conn.cursor()
    sql = '''
      SELECT newsno, article, link, rdate
      FROM news_news
      ORDER BY newsno ASC
    '''
    df = pd.read_sql(sql, conn)
    print("데이터베이스에서 데이터 로딩.")

    cursor.close()
    conn.close()

    # 기사 제목 추출
    articles = df['article']

    # 모든 기사 제목에서 번호 삭제
    print("모든 기사 제목에서 한글을 뺀  문자 제거:", end='')
    for i in range(len(articles)):
        article = articles[i]
        dot_index = article.find(".")
        article = article[dot_index + 1:]
        articles[i] = article

        # 모든 기사 제목에서 한글을 뺀  문자 제거
        print('#', end='')
        for i in range(len(articles)):
            article = articles[i]
            article = re.sub('[.]+', ' ', article)
            article = re.sub('[0-9]+', '', article)
            article = re.sub('[A-Za-z]+', '', article)
            article = re.sub('[-=+,#/\?:^$@*\"※~&%ㆍ·!』\\‘’|\(\)\[\]\<\>`\'…》]', '', article)
            articles[i] = article

    print("\n모든 데이터 문자열로 통합")
    article_all = ''
    for i in range(len(articles)):
        article_all = article_all + ' ' + articles[i]

    okt = Okt()
    article_all_nouns = okt.nouns(article_all)

    # 한문자는 의미 없는 경우가 많아 제거, 달, 해, 술이란 단어는 무시함.
    print('한문자는 의미 없는 경우가 많아 제거, 달, 해, 술이란 단어는 무시함.')
    article_all_nouns2 = []
    for item in article_all_nouns:
        if (len(item) >= 2):
            article_all_nouns2.append(item)

    # 불용어는 명사가 아닌 단어를 선정 권장
    print('불용어 제거')
    stop_words = "한날 한시 육박 가자 생긴 같이 아직 들어가 금지 변화 등급 지급 도움 강타 어디가"
    stop_words = stop_words.split(' ')  # 불용어 공백으로 분할
    print('stop_words -> ', stop_words)

    result = []
    for w in article_all_nouns2:
        if w not in stop_words:
            result.append(w)

    print('빈도가 높은 30위까지 출력')
    tags_counts = Counter(result)
    print(type(tags_counts))
    most_common = tags_counts.most_common(30)  # 빈도가 높은 30위까지 출력

    df = pd.DataFrame(most_common)
    df.columns = ['tags', 'counts']

    # 워드클라우드 이미지 만들기
    # background_color="white": 배경색
    # max_words=100: 최대 출력할 단어의 수
    # relative_scaling= 0.3: 빈도에 따라 상대적인 크기
    # width = 1200: 너비
    # height = 800: 높이
    print('워드클라우드 이미지 제작중...')
    if platform.system() == 'Windows':  # 윈도우의 경우
        font_path = "C:/Windows/Fonts/malgun.ttf"
    elif platform.system() == "Darwin":  # Mac 의 경우
        font_path = "/Users/$USER/Library/Fonts/AppleGothic.ttf"

    wordcloud = WordCloud(font_path=font_path,
                          background_color="white",
                          max_words=100,
                          relative_scaling=0.1,
                          width=1200,
                          height=800
                          ).generate_from_frequencies(tags_counts)
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud)
    plt.axis('off')

    fname = 'C:/ai8/ws_python/CrawlingB/news/static/images/news-wordcloud.png'
    if os.path.exists(fname):
        print("기존에 생성된 news-wordcloud.png 파일을 삭제했습니다.")
        os.remove(fname)

    print('Wordcloud 이미지 파일로 저장')
    plt.savefig(fname) # Wordcloud 이미지 파일로 저장

    print("데이터분석을 완료했습니다.")

    data = {
        "msg": "데이터분석을 완료했습니다.",
    }

    return HttpResponse(json.dumps(data), content_type="application/json")