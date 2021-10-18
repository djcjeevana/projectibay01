from django.contrib import admin

from .models import *


# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    list_display=['user','country','division','district','subdistrict']
    class Media:
        js=("assets/js/locations.js",)

admin.site.register(Address,LocationAdmin)


class DistrictAdmin(admin.ModelAdmin):
    
    class Media:
        js=("assets/js/newdistrict.js",)

admin.site.register(District,DistrictAdmin)

class SubDistrictAdmin(admin.ModelAdmin):
    
    class Media:
        js=("assets/js/newsubdistrict.js",)

admin.site.register(SubDistrict,SubDistrictAdmin)


admin.site.register([Country,Division])