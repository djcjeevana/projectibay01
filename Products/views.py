from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework.views import APIView

from .models import *


class SubCategoryList(APIView):
    permission_classes=[IsAuthenticated,]
    def post(self,request,format=None):
        category=request.data['category']
        subcategory={}
        if category:
            subcategories=Category.objects.get(id=category).subcategories.all()
            subcategory={p.title:p.id for p in subcategories}
        return JsonResponse(data=subcategory, safe=False)
    
    
class MiniCategoryList(APIView):
    permission_classes=[IsAuthenticated,]
    def post(self,request,format=None):
        subcategory=request.data['subcategory']
        minicategory={}
        if subcategory:
            minicategories=SubCategory.objects.get(id=subcategory).minicategories.all()
            minicategory={p.title:p.id for p in minicategories}
        return JsonResponse(data=minicategory, safe=False)
    
    
