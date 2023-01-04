from django.db import models

# Create your models here.
class OrdersModel(models.Model):
    subtotal = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    
    # 顧客資料
    customername = models.CharField(max_length=100)
    customerphone = models.CharField(max_length=50)
    customeremail = models.EmailField()
    customeraddress = models.CharField(max_length=100)
    paytype = models.CharField(max_length=20)
    create_date = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.customername
    
class DetailModel(models.Model):
    dorder = models.ForeignKey('OrdersModel', on_delete = models.CASCADE)
    pname = models.CharField(max_length=100)
    unitprice = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    dtotal = models.IntegerField(default=0)
    
    def __str__(self):
        return self.Name
    
    