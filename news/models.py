from django.db import models

# Create your models here.
# id 컬럼이 BIGINT NOT NULL AUTO_INCREMENT 형식으로 자동 생성됨.
class News(models.Model):  # models.Model class 상속, 테이블명
    newsno = models.AutoField(primary_key=True)  # AUTO_INCREMENT 기능을 갖는 PK 직접 지정
    article = models.CharField(max_length = 255)  # 컬럼, VARCHAR
    link = models.CharField(max_length=255)  # 컬럼, VARCHAR
    rdate = models.DateTimeField(auto_now_add=True)  # 날짜 자동 등록됨, date