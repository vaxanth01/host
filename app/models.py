from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager

class MyAccountManager(BaseUserManager):
    """creating the user"""
    def create_user(self, first_name,last_name, username,email, password=None):
        if not email:
            raise ValueError('user most have a email')
        if not username:
            raise ValueError('user most have a username')
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,


        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,first_name,last_name, username,email,password):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            password= password,
            username = username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True    
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=20)

    """SOME OTHER REQUIED FIELD"""
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name','last_name', 'username']

    objects = MyAccountManager()
    
    def full_name(self):
         return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_lable):
        return True
    
from django.conf import settings
from django.db import models

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses', default=1)
    first_name = models.CharField(max_length=100,default='')
    last_name = models.CharField(max_length=100,default='')
    phone_number = models.CharField(max_length=15 , default=0)
    address_line= models.CharField(max_length=1000,default='')
    alter_number = models.IntegerField(default=0)
    email = models.EmailField(default='')
    street_name= models.CharField(max_length=1000,default='')
    kilometer=models.IntegerField(default=0)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    zip_code = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}, {self.state}"

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,default='')
    last_name = models.CharField(max_length=100,default='')
    profile_pic = models.ImageField(blank=True, upload_to='user/profile')
    phone_number = models.IntegerField( default=0)
    alter_number = models.IntegerField( default=0)
    email = models.EmailField(default='')
    address_line = models.CharField(max_length=100,default='')
    street_name= models.CharField(max_length=1000,default='')
    kilometer=models.IntegerField(default=0)
    city = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    zip_code = models.IntegerField(default=0)
    bussiness_credit = models.BooleanField(default=False)
    credit_day = models.IntegerField(default=0)
    credit_day1 = models.IntegerField(default=0)




    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

