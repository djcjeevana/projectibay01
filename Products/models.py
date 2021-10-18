from django.conf import settings
from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe

# Category Class Begings 


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)
    

class Category(models.Model):

    
    title = models.CharField(max_length=225)
    image = models.ImageField(blank=True, upload_to='category/')
    details = models.TextField()
    status =  models.BooleanField(default=True)
    slug = models.SlugField(null=True, unique=True)
    

    

    def __str__(self):
        return self.title
    
    def ImageUrl(self):
        if self.image:
            return self.image.url
        else:
            return ""
    

    def get_absolute_url(self):
        return reverse('product_element',kwargs={'slug':self.slug})
    
    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
    
# SubCategory Class Ends


class SubCategory(models.Model):
  
    
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='subcategories')
    title = models.CharField(max_length=225)
    status = models.BooleanField(default=True)
    slug = models.SlugField(null=True, unique=True)
    
    
    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title
    
   
    
    def get_absolute_url(self):
        return reverse('product_element',kwargs={'slug':self.slug})
    

    @staticmethod
    def get_all_subcategories():
        return SubCategory.objects.all()
    
    
# miniCategory Class


class MiniCategory(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name='minicategories')
     # category එකේ id එක  product table එකට කරන්න 
    title = models.CharField(max_length=225)
    status = models.BooleanField(default=True)
    slug = models.SlugField(null=True, unique=True)
    
    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title
    
    
    
    def get_absolute_url(self):
        return reverse('product_element',kwargs={'slug':self.slug})
    

    @staticmethod
    def get_all_mini_categories():
        return MiniCategory.objects.all()
    


# size Class

class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name
    
# Products Class


class Product(models.Model):   

    VARIANTS = (
        
        ('Featured-Product', 'Featured-Product'),
        ('Best-Seller', 'Best-Seller'),

    )
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # category එකේ id එක  product table එකට කරන්න 
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    mini_category = models.ForeignKey(MiniCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(blank=True, upload_to='product/',default='product/default.jpg')
    image_hover = models.ImageField(blank=True, upload_to='product/',default='product/default.jpg')
    new_price = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    amount = models.IntegerField(default=0)
    variant = models.CharField(max_length=20, choices=VARIANTS, default='None')
    detail = models.TextField(blank=True)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()
    
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'
    

    def __str__(self):
        return self.title

    

    def ImageUrl(self):
        if self.image:
            return self.image.url
        else:
            return ""
        
    def ImageUrlHover(self):
        if self.image_hover:
            return self.image_hover.url
        else:
            return ""

    def get_absolute_url(self):
        return reverse("Stores:product_single",kwargs={"slug":self.slug})
    
    
    

    @staticmethod
    def get_products_by_categoryID(category_id):
        if category_id:
            
            return Product.objects.filter(category = category_id)
        else:
            
            return Product.objects.all()
    
# Image Class

class Images(models.Model):
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(blank=True, upload_to='product/')
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
    

    def __str__(self):
        return self.title
    

# Comment Class 
class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),

    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, blank=True)
    comment = models.CharField(max_length=500, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=40, choices=STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    
# Comment Form 


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']


# Color Class


class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""
    
#Varient Class



class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    image_id = models.IntegerField(blank=True, null=True, default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage = ""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""