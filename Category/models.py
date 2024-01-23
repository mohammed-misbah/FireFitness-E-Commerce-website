from django.db import models
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    category_name   = models.CharField(max_length=100,unique=True,null=False)
    slug            = models.SlugField(max_length=100,unique=True)
    category_image  = models.ImageField(upload_to ='images/',blank=True)
   
    def get_url(self):
        return reverse('products_by_category',args=[self.slug])
    def __str__(self):
        return self.category_name

        
class Subcategory(models.Model):
    subcat_name     = models.CharField(max_length=100,unique=True)
    subcat_image    = models.ImageField(upload_to='images/',blank=True)
    subcat_list     = models.CharField(max_length=100,unique=True)
    category        = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.subcat_name





    
    
    
    