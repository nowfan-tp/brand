from django.db import models
from user_area.models import users

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    status=models.BooleanField(default=False,help_text="0=default,1=Hidden")
    # date_joined     =models.DateTimeField(auto_now_add=True)
    # last_login      =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class brands(models.Model):
    name = models.CharField(max_length=255)
    status=models.BooleanField(default=False,help_text="0=default,1=Hidden")
    # date_joined     =models.DateTimeField(auto_now_add=True)
    # last_login      =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class products(models.Model):
    name = models.CharField(max_length=255)
   
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_1 = models.ImageField(upload_to='shoes/')
    image_2 = models.ImageField(upload_to='shoes/')
    image_3 = models.ImageField(upload_to='shoes/')
    size            =models.DecimalField(max_digits=10, decimal_places=2)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=False ,null=True)
    brans = models.ForeignKey(brands, on_delete=models.CASCADE, default=False ,null=True)
    date_joined     =models.DateTimeField(auto_now_add=True)
    last_login      =models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50,blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=6)
    is_active = models.BooleanField(default=True)


class Usedcoupoon(models.Model):
    user=models.ForeignKey(users,on_delete=models.CASCADE,null=True)
    Coupon=models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True)






