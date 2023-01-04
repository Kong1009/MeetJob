from django.db import models

# Create your models here.
class Movies(models.Model):
    title = models.CharField(max_length=100)
    img_link = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    evaluation = models.CharField(max_length=10)
    date = models.DateField(max_length=10)
    
    class Meta:
        db_table = "movies"
    