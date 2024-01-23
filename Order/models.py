from django.db import models
from Product.models import Product
from Protien.models import User
from Cart.models import Variation
import datetime
current_date =  datetime.date.today()

# Create your models here.

class Address(models.Model):
    user       = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,null=False)
    last_name  = models.CharField(max_length=100,null=False)
    phone      = models.CharField(max_length=12,unique=True)
    email      = models.CharField(max_length=100,null=False)
    address_1  = models.CharField(max_length=100,null=False)
    address_2  = models.CharField(max_length=100,null=False)
    country    = models.CharField(max_length=100,null=False)
    state      = models.CharField(max_length=100,null=False)
    dist       = models.CharField(max_length=100,null=False)
    pincode    = models.IntegerField(null=False)
    order_note = models.TextField(null=True)

class Order(models.Model):
    STATUS = (('Placed','Placed'),('Shipped','Shipped'),('Out For Delivery','Out For Delivery'),('Delivered','Delivered'),('Cancelled','Cancelled'))
    order_number = models.CharField(max_length=20)
    payment_mode = models.CharField(max_length=200,null=False,default="Pending")
    payment_id   = models.CharField(max_length=200,null=False,default=0)
    status       = models.CharField(max_length=100,choices=STATUS,default="Placed")
    user         = models.ForeignKey(User,on_delete=models.CASCADE)
    address      = models.ForeignKey(Address,on_delete=models.CASCADE)
    order_total  = models.FloatField()
    tax          = models.FloatField()
    is_orderd    = models.BooleanField(default=False)
    Order_day    = models.IntegerField(default = current_date.day)
    Order_month  = models.IntegerField(default = current_date.month)
    Order_year   = models.IntegerField(default = current_date.year)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    
    def _str_(self):
            return self.order_number

class OrderProduct(models.Model):
    order        = models.ForeignKey(Order, on_delete=models.CASCADE,null=True)
    order_number = models.CharField(default=1,max_length=20)
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    product      = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation    = models.ManyToManyField(Variation, blank=True)
    quantity     = models.IntegerField()
    product_price = models.FloatField()
    is_ordered   = models.BooleanField(default=False)
    ordered      = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    


    def __str__(self):
        return self.product.prdct_name

    


