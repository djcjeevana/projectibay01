from django.conf.urls import url
from django.urls import path

from .views import *

app_name = 'Stores'  # ඕනිම ඇප එකක සිට මෙහි urls වලට ඇමතීම ඉතා පැහදිලිව මෙමගින් කර ගත හැකි වේ. 

urlpatterns = [
    path('',Homeview.home,name="home"),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact_dat'),
    path('product/<slug:slug>',product_single,name="product_single"), 
    path('product/<int:id>/<slug:slug>/', category_product, name='category_product'), 
    path('search/', SearchView.as_view(), name='search'),
    path('add-to-cart',add_to_cart,name='add_to_cart'),
    path('delete-from-cart',delete_cart_item,name='delete-from-cart'),
      
    
] 







