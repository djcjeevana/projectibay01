from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    
    path('subcategory/',SubCategoryList.as_view()),
    path('minicategory/',MiniCategoryList.as_view()),
    
    
] 