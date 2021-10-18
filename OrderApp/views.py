from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render
from django.template.loader import render_to_string
from OrderApp.models import ShopCart, ShopingCartForm
from Products.models import Category
from Stores.models import Setting
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from Products.models import Product



# TODO- Handle Out of stocks here 
# Create your views here.
def add_to_shoping_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checking = ShopCart.objects.filter(
        product_id=id, user_id=current_user.id)
    if checking:
        control = 1
    else:
        control = 0

    if request.method == "GET":
        form = ShopingCartForm(request.GET)
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.filter(
                    product_id=id, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, 'Your Product  has been added')
        return HttpResponseRedirect(url)
    else:
        if control == 1:
            data = ShopCart.objects.filter(
                product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, 'Your  product has been added')
        return HttpResponseRedirect(url)


#def cart_detials(request):
#    current_user = request.user
#    category = Category.objects.all()
#    setting = Setting.objects.get(id=1)
#    cart_product = ShopCart.objects.filter(user_id=current_user.id)
#    total_amount = 0
#    for p in cart_product:
#        total_amount += p.product.new_price*p.quantity
#
#    context = {
#        'category': category,
#        'setting': setting,
#        'cart_product': cart_product,
#        'total_amount': total_amount,
#
#    }
#    return render(request, 'cart_details.html', context)


def cart_delete(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    cart_product = ShopCart.objects.filter(id=id, user_id=current_user.id)
    cart_product.delete()
    messages.warning(request, 'Your product has been deleted.')
    return HttpResponseRedirect(url)


#def add_to_cart(request):
#    
#    #del request.session['cartdata']
#	
#    cart_p={}
#    cart_p[str(request.GET['id'])]={
#		'image':request.GET['image'],
#		'title':request.GET['title'],
#		'qty':request.GET['qty'],
#		'price':request.GET['price'],
#	}
#    if 'cartdata' in request.session: # session එකක් තියෙනව නම් 
#        if str(request.GET['id']) in request.session['cartdata']: # select කරපු product එක මේ session එකේ තියෙනවද බලනවා 
#            cart_data=request.session['cartdata'] # ඊට පස්සේ මේ session එක  card_data එකට සමාන කරලා 
#            cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty']) # මේ product එකේ quantity එක increase කරනවා
#            cart_data.update(cart_data) 
#            request.session['cartdata']=cart_data
#        else:
#            cart_data=request.session['cartdata'] # product එක  cart එකේ තිබුනේ නැත්නම්
#            cart_data.update(cart_p) # සැම විටම session එක පවතින තත්වයට update කල යුතුමය 
#            request.session['cartdata']=cart_data
#    else:
#        request.session['cartdata']=cart_p # if not session create session 
#    return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

def check_num(num_type, value):
    try:
        return num_type(value)
    except ValueError:
        return None

def cart_detials(request):
    total_amt=0
    setting = Setting.objects.get(id=1)    
    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():                     
            total_amt+=int(item['qty'])*float(item['price']) # $ ලකුණක් මිලත් එක්ක පාස් වෙලා තිබ්බ එක වුල උනේ. 
                                   
        return render(request, 'cart_details.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'setting':setting})
    else:
        return render(request, 'cart_details.html',{'cart_data':'','totalitems':0,'total_amt':total_amt,'setting':setting})
            
            
#def delete_cart_item(request):
#    p_id=str(request.GET['id']) # ID එක ගන්නවා
#    print("in side thte dlete methohd---------------------------------- ")
#    setting = Setting.objects.get(id=1) 
#    if 'cartdata' in request.session:# session එක ගන්නවා 
#        if p_id in request.session['cartdata']:# ඉහතින් ගත්ත id එකට අදාල product එක session එකේ  තියෙවනවා නම්
#            cart_data=request.session['cartdata']# session එක  card_data එකට දාල
#            del request.session['cartdata'][p_id]# ඒ product එක කරලා දානව ඊට පස්සේ
#            request.session['cartdata']=cart_data# product එක  remove කරලා  remove කලබවට තොරතුරු නැවැත  session එක updataeකරයි
#            
#    total_amt=0
#    for p_id,item in request.session['cartdata'].items():
#        total_amt+=int(item['qty'])*float(item['price'])
#        
#    t=render_to_string('updated-cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
#    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})
        
    