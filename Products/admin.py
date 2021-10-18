from django.contrib import admin

from .models import *


 #Register your models here.
 # Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',)} # title ekata dana nama automatically slug eka lese add vei.



# SubCategory  Admin
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = [ 'category','title']
    prepopulated_fields = {'slug': ('title',)}
    


# Mini Category  Admin
@admin.register(MiniCategory) 
class MiniCategoryAdmin(admin.ModelAdmin):
    list_display = ['category','subcategory','title']
    prepopulated_fields = {'slug': ('title',)}

    class Media:
        js=("assets/js/newminicategory.js",)



 # Product Images Admin 

class ProductImageInline(admin.TabularInline): # admin product form එකේම images add කරන්න connect කරන එක කරන්නේ මෙහෙමයි. 
    model = Images
    extra = 5   # Add කල හැකි Image fileds counts ගණන මෙතනින් වනස් කල හැක.

# Image Inline Filde in product Form

class ProductVariantsInline(admin.TabularInline):
    #model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True 

# Product Admin 
@admin.register(Product) 
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ['category','title', 'new_price', 'amount','in_stock','image_tag']
    list_filter = ['in_stock', 'in_stock']
    list_editable = ['new_price', 'in_stock'] # You can edit this price in admin
    list_per_page = 10
    search_fields = ['title', 'new_price', 'detail']
    prepopulated_fields = {'slug': ('title',)} # Automatically slug එක generate වීම මෙතනින් සිදුවේ 
    inlines = [ProductImageInline]    # උඩ තියෙන method එක භාවිතා admin product forme එකට image form fildes කරන්නේ මෙතැනදී 
    class Media:
        js=("assets/js/newcategory.js",)
