from django.db import models

# Create your models here.
class Contact(models.Model):
	title = models.CharField(max_length=50)
	username = models.CharField(max_length=50)
	info = models.TextField()
	create_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'contacts'