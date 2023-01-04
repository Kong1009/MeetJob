from django.db import models

# Create your models here.
from django.utils import timezone

# 當django 要使用圖片上傳的功能時，要先行安裝 pip install pillow 套件

class Photo(models.Model):
    
    # upload_to 圖片上傳後，存放的路徑位置
    image = models.ImageField(upload_to='images/', blank=False, null=False)
    upload_date = models.DateField(default=timezone.now)