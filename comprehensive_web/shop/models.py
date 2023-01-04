from django.db import models

# Create your models here.
class Product(models.Model):
    subject = models.CharField(max_length=100)
    platform = models.CharField(max_length=50)
    link = models.CharField(max_length=255)
    img_link = models.CharField(max_length=255)
    price = models.CharField(max_length=100)
    item = models.CharField(max_length=50)
    info = models.TextField()
    create_date = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = "products"