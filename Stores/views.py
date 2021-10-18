
from django.contrib import messages
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.template.loader import render_to_string
from Marketing.models import ImagesAdds
from Products.models import (Category, Images, MiniCategory, Product,
                             SubCategory)

from .models import *
from .serializers import menuserializer, minimenuserializer, submenuserializer


class Homeview(View):
    
    
    def home(request):
        try:
          
          categories = Category.get_all_categories()
          subcategories = SubCategory.get_all_subcategories()
          minicategories = MiniCategory.get_all_mini_categories()
          
          
          mainmenu = menuserializer(categories,many=True)
          data = mainmenu.data         
          request.session['mainM'] = data
      
          submenudata = submenuserializer(subcategories,many=True)
          subdata = submenudata.data          
          request.session['submenu'] = subdata
          
          minimenudata = minimenuserializer(minicategories,many=True)
          minidata = minimenudata.data          
          request.session['minimenu'] = minidata
                  
          setting = Setting.get_settings_by_id(1)
          top_banners = ImagesAdds.objects.filter(image_category='Top-Banner') # ප්‍රධාන බැනර් එකට පින්තුර දාන්නේ මෙතනින්. මේකට පින්තුර එකතු කරන්නේ  Image adds කියන ටේබල් එකෙන් 
          #slider_products = Product.objects.all().order_by('id')[:3] # පහලම  තිබෙන තුන ලබා ගැනීම. 
          latest_products = Product.products.all().order_by('-id')[:3] # ඉහළම  තිබෙන තුන ලබා ගැනීම. 
          best_seller = Product.products.filter(variant='Best-Seller').order_by('-id')[:5]
          featured_products = Product.products.filter(variant='Featured-Product')
          
          products = None
          categoryID = request.GET.get('category') # href="/?category={{category.id}}" එකෙන් මෙතන CategoeryID එකට ලින්ක් කර අදාළ category id එක ලබා ගනී 
         
          if categoryID == None:
               
               products = Product.get_products_by_categoryID(None)
               
          else:
               products  = Product.get_products_by_categoryID(categoryID)
               
               
                         
          context = {'setting': setting,
                     #'slider_products':slider_products,
                     'latest_products':latest_products,
                     'featured_products':featured_products,
                     'best_seller':best_seller,
                     'top_banners':top_banners,
                     'categories':categories,
                     'subcategories':subcategories,
                     'minicategories':minicategories,
                     'products':products}
          
          return render(request, 'index.html',context)
        except Exception as identifier:         
          return render(request, 'index.html', {}) 
          
     
# About Page
def about(request):
    setting = Setting.get_settings_by_id(1)
    context = {'setting':setting,}
    return render(request, 'about.html', context)   

# Contact Page
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid(): 
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Profile details updated.')
#
            return redirect('contact_dat')
#
    form = ContactForm
    setting = Setting.get_settings_by_id(1)
    context = {
        'form': form,
        'setting':setting,         
         }
    return render(request, 'contact.html', context)


# search bar
class SearchView(TemplateView):
    template_name = "products_templates/category_products.html"
    def get_context_data(self,**kwargs):
        
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        product_cat = Product.objects.filter(title__icontains=kw)
        
        setting = Setting.get_settings_by_id(1)
        context = {
            'product_cat':product_cat,
            'setting':setting,
        }
        #context["product_cat"] = product_cat
        #context["setting"]   = setting
        return context
    
    
# Sngle Product View Class


def product_single(request,slug):
       product = get_object_or_404(Product, slug=slug, in_stock=True)
       setting = Setting.get_settings_by_id(1)
       latest_products = Product.products.filter(category=product.category)
       context = {
           'single_product': product,
           'setting':setting,
           'latest_products':latest_products
           }
       return render(request,'products_templates/single-product.html',context)

# Displya All Products relatete to your selected category
     
def category_product(request, id, slug):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    minicategories = MiniCategory.objects.all()
          
    
    setting = Setting.objects.get(id=1)
    sliding_images = Product.objects.all().order_by('id')[:2]
    prouct_cat = Product.objects.filter(category_id=id)
    context = {
        'categories': categories,
        'subcategories': subcategories,
        'subcategories': subcategories,        
        'setting': setting,
        'product_cat': prouct_cat,
        'sliding_images': sliding_images,
        'minicategories':minicategories,
    }
    return render(request, 'products_templates/category_products.html', context)


def add_to_cart(request):
    
    #del request.session['cartdata']
	
    cart_p={}
    cart_p[str(request.GET['id'])]={
		'image':request.GET['image'],
		'title':request.GET['title'],
		'qty':request.GET['qty'],
		'price':request.GET['price'],
	}
    if 'cartdata' in request.session: # session එකක් තියෙනව නම් 
        if str(request.GET['id']) in request.session['cartdata']: # select කරපු product එක මේ session එකේ තියෙනවද බලනවා 
            cart_data=request.session['cartdata'] # ඊට පස්සේ මේ session එක  card_data එකට සමාන කරලා 
            cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty']) # මේ product එකේ quantity එක increase කරනවා
            cart_data.update(cart_data) 
            request.session['cartdata']=cart_data
        else:
            cart_data=request.session['cartdata'] # product එක  cart එකේ තිබුනේ නැත්නම්
            cart_data.update(cart_p) # සැම විටම session එක පවතින තත්වයට update කල යුතුමය 
            request.session['cartdata']=cart_data
    else:
        request.session['cartdata']=cart_p # if not session create session 
    return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})


def delete_cart_item(request):
    p_id=str(request.GET['id']) # ID එක ගන්නවා
    print("in side thte dlete methohd ")
    setting = Setting.objects.get(id=1) 
    if 'cartdata' in request.session:# session එක ගන්නවා 
        if p_id in request.session['cartdata']:# ඉහතින් ගත්ත id එකට අදාල product එක session එකේ  තියෙවනවා නම්
            cart_data=request.session['cartdata']# session එක  card_data එකට දාල
            del request.session['cartdata'][p_id]# ඒ product එක කරලා දානව ඊට පස්සේ
            request.session['cartdata']=cart_data# product එක  remove කරලා  remove කලබවට තොරතුරු නැවැත  session එක updataeකරයි
            
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
        
    t=render_to_string('updated-cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})    
     