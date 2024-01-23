from django.db import models

# Create your models here.
class Coupon(models.Model):
    coupon_code    = models.CharField(max_length=10)
    is_expired     = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)

    def __str__(self):
        return self.coupon_code