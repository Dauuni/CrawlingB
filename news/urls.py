from django.urls import path
from . import views

# 'news' is not a registered namespace 방지용 선언, 생략시 reverse() 함수에러 발생
app_name='news'

urlpatterns = [
    # 주소, 호출할 뷰, 뷰에 전달할 값은 생략, path 이름
    # http://127.0.0.1:8000/news/
    path('', views.index, name='index'),
    path('crawling', views.crawling, name='crawling'),
    path('delete', views.delete, name='delete'),
    path('delete_all', views.delete_all, name='delete_all'),
    path('trend_analysis', views.trend_analysis, name='trend_analysis'),
]