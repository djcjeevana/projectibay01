from django.conf.urls import url
from django.urls import path

from Location.views import DistrictList, DivisionList, SubDistrictList

urlpatterns = [
    
    path('divisions/',DivisionList.as_view()),
    path('districts/',DistrictList.as_view()),
    path('subdistricts/',SubDistrictList.as_view()),
    
] 

