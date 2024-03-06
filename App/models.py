from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from .choices import *
import uuid
import datetime
import random
from Discord_Taher.settings import *
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class CommonTimePicker(models.Model):
    created_at = models.DateTimeField("Created Date", auto_now_add=True)
    updated_at = models.DateTimeField("Updated Date", auto_now=True)

    class Meta:
        abstract = True


class MyUserManager(BaseUserManager):

    def create_user(self, email, password):
        if not email:
            raise ValueError('Users must have an Email Address')

        user = self.model(
            email=self.normalize_email(email),
            is_active=False,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        if user.is_superuser:
            user.first_name = "Admin"
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser,CommonTimePicker):
    user_type = models.CharField("User Type", max_length=10, default='Admin', choices=USERTYPE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField("Email Address", null=True, blank=True, unique=True)
    mobile = models.CharField('Mobile Number', max_length=256,default="")
    first_name = models.CharField("First Name", max_length=256, blank=True, null=True)
    last_name = models.CharField("Last Name", max_length=256, blank=True, null=True)
    avatar = models.ImageField("profile photo", null=True, blank=True,upload_to='user_images')
    age = models.DateField("Age", blank=True, null= True)
    otp = models.CharField('OTP', max_length=4, blank=True, null=True)
    device_token = models.CharField("Device ID", max_length=500, blank=True, null=True)
    is_superuser = models.BooleanField("Super User", default=False)
    is_staff = models.BooleanField("Staff", default=False)
    is_active = models.BooleanField("Active", default=False)
    
    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def _str_(self):
        return f"{self.uuid}_{self.email}" 
    
    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_short_name(self):
        return self.email

    def otp_creation(self):
        otp = random.randint(1000, 9999)
        self.otp = otp
        self.save()
        return otp



# exchnage = symbol i.e 	USDDT.P
# pair = Exchange i.e Binances  
class CryptoPair(models.Model):
    exchange = models.CharField(max_length=50, unique=True)
    pair = models.CharField(max_length=50)
    # symbol = models.ImageField("Symbol", null=True, blank=True, upload_to='symbols')
    def _str_(self):
        return f"{self.exchange} - {self.pair}"

    
class Commodities(models.Model):
    exchange = models.CharField(max_length=50, unique=True)
    pair = models.CharField(max_length=50)
    # symbol = models.ImageField("Symbol", null=True, blank=True, upload_to='symbols')
    def _str_(self):
        return f"{self.exchange} - {self.pair}"

class Forex(models.Model):
    exchange = models.CharField(max_length=50, unique=True)
    pair = models.CharField(max_length=50)
    # symbol = models.ImageField("Symbol", null=True, blank=True, upload_to='symbols')
    def _str_(self):
        return f"{self.exchange} - {self.pair}"

class IndStockMarket(models.Model):
    exchange = models.CharField(max_length=50, unique=True)
    pair = models.CharField(max_length=50)
    # symbol = models.ImageField("Symbol", null=True, blank=True, upload_to='symbols')
    def _str_(self):
        return f"{self.exchange} - {self.pair}"
   
class UsStockMarket(models.Model):
    exchange = models.CharField(max_length=50, unique=True)
    pair = models.CharField(max_length=50)
    # symbol = models.ImageField("Symbol", null=True, blank=True, upload_to='symbols')
    def _str_(self):
        return f"{self.exchange} - {self.pair}"
class WorldMarket(models.Model):
    exchange = models.CharField(max_length=50, unique=True)
    pair = models.CharField(max_length=50)
    # symbol = models.ImageField("Symbol", null=True, blank=True, upload_to='symbols')
    def _str_(self):
        return f"{self.exchange} - {self.pair}"
    
class CryptoTotalMarket(models.Model):
    exchange = models.CharField(max_length=50, unique=True)
    pair = models.CharField(max_length=50)
    # symbol = models.ImageField("Symbol", null=True, blank=True, upload_to='symbols')
    def _str_(self):
        return f"{self.exchange} - {self.pair}"
    

class DivergenceScreener(CommonTimePicker):
    interval_choices=[
        ('15m','15m'),
        ('1h','1h'),
        ('4h','4h'),
        ('1d','1d'),
        ('1w','1w'),
    ]
    divergence_choice=[
        ('BERD','Bearish Regular Divergence'),
        ('BEHD','Bearish Hidden Divergence'),
        ('BURD','Bullish Regular Divergence'),
        ('BUHD','Bullish Hidden Divergence'),
    ]
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True, related_name='+')
    object_id = models.PositiveIntegerField(null=True, blank=True)
    exchange = GenericForeignKey('content_type', 'object_id')
    price = models.FloatField(blank=True,null=True)
    rsi = models.CharField(max_length=50,blank=True,null=True,choices=divergence_choice)
    macd_histogram = models.CharField(max_length=50,blank=True,null=True,choices=divergence_choice)
    obv = models.CharField(max_length=50,blank=True,null=True,choices=divergence_choice)
    cvd = models.CharField(max_length=50,blank=True,null=True,choices=divergence_choice)
    stochastics = models.CharField(max_length=50,blank=True,null=True,choices=divergence_choice)
    interval = models.CharField(max_length=3,blank=True,null=True ,choices=interval_choices)
    time = models.CharField(max_length=300,blank=True,null=True)

    
    class Meta:
        ordering = ['-id']
        
class BrakerScreener(CommonTimePicker):
    interval_choices=[
        ('15m','15m'),
        ('1h','1h'),
        ('4h','4h'),
        ('1d','1d'),
        ('1w','1w'),
    ]
    breaker_choice=[
        ('ACTIVE','ACTIVE'),
        ('BREAKOUT','BREAKOUT'),
        ('BRAKEIN','BRAKEIN'),
    ]
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, blank=True, null=True, related_name='+')
    object_id = models.PositiveIntegerField(null=True, blank=True)
    exchange = GenericForeignKey('content_type', 'object_id')
    price = models.FloatField(blank=True,null=True)
    notification= models.CharField(max_length=20,blank=True,null=True,choices=breaker_choice)
    interval = models.CharField(max_length=3,blank=True,null=True ,choices=interval_choices)
    is_support = models.CharField(max_length=300,blank=True,null=True)
    level = models.CharField(max_length=300,blank=True,null=True)
    time = models.CharField(max_length=300,blank=True,null=True)

    
    class Meta:
        ordering = ['-id']
    
    
    
