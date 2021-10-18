from rest_framework import serializers

from Products.models import Category, MiniCategory, SubCategory


class menuserializer(serializers.ModelSerializer):
    class Meta:
      model = Category
      fields =['id','title','slug']
 
class submenuserializer(serializers.ModelSerializer):
    class Meta:
      model = SubCategory
      fields =['id','title','category','slug']
      
class minimenuserializer(serializers.ModelSerializer):
    class Meta:
      model = MiniCategory
      fields =['id','title','category','subcategory','slug']