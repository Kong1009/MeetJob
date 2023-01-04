from django.db import models

# Create your models here.

class Member(models.Model):
    email = models.EmailField(max_length=100, blank=True) # 帳號
    username = models.CharField(max_length=50, blank=True) # 使用者名稱
    password = models.CharField(max_length=200, blank=True) # 使用者密碼
    birthday = models.DateField() # 出生年月日 
    sex = models.CharField(max_length=2) # 性別
    create_date = models.DateTimeField(auto_now_add=True) # 建立日期
    
    
    class Meta:
        db_table = "members"
    
