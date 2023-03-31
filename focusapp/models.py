from django.db import models
from user_area.models import users
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from admin_app.models import *
# Create your models here.

# class MyAccountManager(BaseUserManager):
#     def create_user( self, email , username, password ):
#         if not email:
#             raise ValueError("User must have an email address")
#         if not username:
#             raise ValueError("User must have an username ")
#         user = self.model(
#             email = self.normalize_email(email),
#             username = username,
#         )
#         user.set.password(password)
#         user.save(using=self._db)
#         return user

#     def create_supperuser(self, email , username , password):
#         user = self.create_user(
#             email = self.normalize_email(email),
#             username = username,
#             password = password
#         )

#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using = self._db)
#         return user


        





# class myusers(AbstractBaseUser):
#     first_name = models.CharField(max_length = 100)
#     last_name = models.CharField(max_length = 100)
#     email = models.EmailField(max_length = 100,unique=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     username = models.CharField(max_length = 100)
#     is_superuser = models.BooleanField(default=False)
#     password = models.CharField(max_length = 100)
#     date_joined     =models.DateTimeField(auto_now_add=True)
#     last_login      =models.DateTimeField(auto_now_add=True)
#     otps       = models.CharField(max_length=10,blank=True,default=0)
#     is_admin = models.BooleanField(default=False)




#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['uesrname']


#     def __str__(self):
#         return self.first_name

#     def has_perm(self,perm,obj=None):
#         return self.is_admin

#     def has_module_perms(self,app_label):
#         return True

    


class Cart(models.Model):
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    user = models.ForeignKey(users, on_delete=models.CASCADE,null = True,blank=True)
    price = models.PositiveIntegerField(default=False ,null=True)
    totalprice = models.PositiveIntegerField(default=False ,null=True)

    def sub_total(self):
        return self.product.price*self.quantity
        # return self.product.price*self.product.quantity
    # purchased = modls.BooleanField(_("",default=False))

class Address(models.Model):
    user=models.ForeignKey(users,on_delete=models.CASCADE,null=True,blank=True)
    pincode=models.IntegerField()
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    locality=models.CharField(max_length=100)
    flat=models.CharField(max_length=100)
    phone =models.CharField(max_length=100,null=False)
    is_difault = models.BooleanField(default=False)

class order(models.Model):
    user=models.ForeignKey(users,on_delete=models.CASCADE,null=True,blank=True)
    Addres = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price=models.FloatField(null=False)
    payment_mode=models.CharField(max_length=100,null=False)
    payment_id=models.CharField(max_length=100,null=False)
    STATUS = (
        ('Out_for_delivery','Out_for_delivery'),
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
        ('Refund','Refund'),
    )
    status = models.CharField(max_length=30, choices = STATUS,default='Pending')
    message =models.TextField(null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self) -> str:
    #     return '{}-{}'.format(self.id,self.tracking_no)

class orderitem(models.Model):
    user=models.ForeignKey(users,on_delete=models.CASCADE,null=True,blank=True)
    orderit = models.ForeignKey(order, on_delete=models.CASCADE)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    # def __str__(self):
    #     return '{}-{}'.format(self.orderit.id,self.orderit.tracking_no)

class wishlist(models.Model):
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    user = models.ForeignKey(users, on_delete=models.CASCADE,null = True,blank=True)
    price = models.PositiveIntegerField(default=False ,null=True)
    totalprice = models.PositiveIntegerField(default=False ,null=True)

    def sub_total(self):
        return self.product.price*self.quantity

class UserProfilepic(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE,null = True,blank=True)
    # add this field to store the profile picture
    profile_picture = models.ImageField(upload_to='dp', blank=True, null=True)
    








