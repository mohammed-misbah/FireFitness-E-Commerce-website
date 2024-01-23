import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
class MyFitnessManager (BaseUserManager):
    #========creating user======#
    def create_user(self,username,email,password=None,**extra_fields):    
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        user =self.model(
            email = self.normalize_email(email),
            **extra_fields,
            username=username,
            date_joined=datetime.datetime.now()
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    #===========creating superuser========#

    def create_superuser(self,username,email,password):
        user =self.create_user(email=self.normalize_email(email),username=username,password=password)
        user.is_admin =True
        user.is_active =True
        user.is_staff=True
        user.is_superuser =True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username=models.CharField(max_length=100,null=True)
    email=models.CharField(max_length=100,null=True,unique=True)
    phone_number=models.CharField(max_length=15,null=True)
    

    date_joined  = models.DateTimeField(null=True)
    last_login  = models.DateTimeField(auto_now_add=True,null=True)
    is_staff   = models.BooleanField(default=True)
    is_active   = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS= ['username']
    
    objects =MyFitnessManager()

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    def has_module_perms(self, add_label):
        return True
    
     