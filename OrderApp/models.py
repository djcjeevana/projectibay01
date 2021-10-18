from django.conf import settings
from django.db import models
from django.forms import ModelForm
from django.utils.safestring import mark_safe

from Location.models import SubDistrict
from Location.views import Country, District, Division
from Products.models import Product

# Create your models here.


class ShopCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()

    def price(self):
        return self.product.new_price 


    @property
    def amount(self):
        return self.quantity*self.product.new_price

    def __str__(self):
        return self.product.title
    
    
class ShopingCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']