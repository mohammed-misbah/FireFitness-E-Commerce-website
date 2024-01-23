from django.db import models
from Product.models import Product
from Protien.models import User
from Coupon.models import Coupon
# Create your models here.

class VariationManager(models.Manager):
    def flavour(self):
        return super(VariationManager, self).filter(variation_category='flavour', is_active=True)

    def size(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (('flavour','flavour'),('size','size'))

class Variation(models.Model):
    product             = models.ForeignKey   (Product,on_delete=models.CASCADE)
    variation_category  = models.CharField    (max_length=100,choices=variation_category_choice)
    variation_value     = models.CharField    (max_length=100)
    is_active           = models.BooleanField (default=True)
    created_date        = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class Cart(models.Model):
    cart_id    = models.CharField(max_length=300)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user      = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product   = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    cart      = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    variation = models.ManyToManyField(Variation,blank=True)
    coupon    = models.ForeignKey(Coupon, on_delete=models.SET_NULL , null =True,blank=True)
    
    quantity  = models.IntegerField()
    is_active = models.BooleanField(default=True)
   

    def sub_total(self):
        return self.product.price*self.quantity
    
    def __unicode__(self):
        return self.product
    



