
from django.contrib import admin
from django.urls import path

from OrderApp.views import *

app_name = 'OrderApp'

urlpatterns = [
  path('addingcart/<int:id>/', add_to_shoping_cart, name='add_to_shoping_cart'),
  path('cart_details/', cart_detials, name='cart_detials'),
  path('cart_delete/<int:id>/', cart_delete, name='cart_delete'), 
  
  
  

]
