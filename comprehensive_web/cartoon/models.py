from django.db import models

# Create your models here.
class CarToon(models.Model):
    subject = models.CharField(max_length=100) # 標題、主題
    img_link = models.CharField(max_length=255) # 圖片連結
    link = models.CharField(max_length=255) # 連結
    item = models.CharField(max_length=50) # 類別
    year = models.CharField(max_length=50) # 年份
    popularity = models.IntegerField() # 人氣
    director = models.CharField(max_length=20) # 導演
    area = models.CharField(max_length=20) # 地區
    
    class Meta:
        db_table = "CarToon"