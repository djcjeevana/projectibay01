from django.contrib.auth import authenticate, login, logout
# Create your models here.
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


from Location.models import *

# Create your models here.
class CustomAccountManager(BaseUserManager):
    
       
    def create_user(self, email, username, password=None):

        if not email:
            raise ValueError(_('You must provide an email address'))
        
        if not username:
            raise ValueError(_('You must provide an username'))
               
        
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
         
    def create_superuser(self, email, username, password):
    
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,            
        )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user 

    
def get_profile_image_filepath(self,filename):
    return f'profile_images/{self.pk}/{"profile_image.png)"}'

def get_default_profile_image():
    return "ibayimage/logo_1080_1080.png"





class UserBase(AbstractBaseUser, PermissionsMixin):

    location=models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True, related_name='location')
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=225, unique=True)
    first_name = models.CharField(max_length=225, blank=True)
    last_name = models.CharField(max_length=225, blank=True)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    # Delivery details
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=225, blank=True)
    address_line_2 = models.CharField(max_length=225, blank=True)
    town_city = models.CharField(max_length=150, blank=True)
    # User Status
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=225,upload_to=get_profile_image_filepath,null=True,blank=True,default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.username
    
    def get_profiel_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]
    

    def has_perm(self, perm,obj=None):
        return self.is_admin
    
    
    
    def has_module_perms(self,app_label):
        return True
    