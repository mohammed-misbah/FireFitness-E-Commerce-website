from django.db import models
from Category.models import Category,Subcategory
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Product(models.Model):
    prdct_name      = models.CharField(max_length=500,unique=True)
    prdct_desc      = models.TextField(max_length=500,blank=True)
    slug            = models.SlugField(max_length=500,unique=True)
    offer_percentage = models.IntegerField(default=0,validators=[MaxValueValidator(70)])
    original_price   = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    price           = models.FloatField()
    stock           = models.BigIntegerField(default=0)
    created_date    = models.DateTimeField(auto_now_add=True,null=True)
    category        = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    subcategory     = models.ForeignKey(Subcategory,on_delete=models.CASCADE,null=True)
    is_available    = models.BooleanField(default=True)
    img1     = models.ImageField(upload_to='images/',blank=True)
    img2     = models.ImageField(upload_to='images/',blank=True)
    img3     = models.ImageField(upload_to='images/',blank=True)
    img4     = models.ImageField(upload_to='images/',blank=True)

    def get_url(self):
        return reverse('product_datails',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.prdct_name 



