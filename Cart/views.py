from django.shortcuts import render,redirect,get_object_or_404
from Product.models import Product
from Protien.models import User
from .models import Cart,CartItem
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.core.exceptions import ObjectDoesNotExist 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from Coupon.models import Coupon
from django.contrib import messages
from Cart.models import Variation
#================Add Cart===============#

def _cart_id(request):
    cart = request.session.session_key   #its taking a cart id each product
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request,product_id):
    current_user =request.user
    product = Product.objects.get(id=product_id)   # get the product
    # if the user id authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item 
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.apppend(variation)
                except:
                    pass
        is_cart_item_exists =  CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product,user=current_user)
            ex_var_list =[]
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            
            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                if item.quantity < product.stock:
                    print(product.stock)
                    item.quantity += 1
                    item.save()
                else:
                    messages.error(request, "No stock available !!")
                    return redirect('cart')
            else:
                item = CartItem.objects.create(product=product,quantity=1,user=current_user)
                if len(product_variation)> 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(product=product,quantity=1,user=current_user)
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
        return redirect('cart')


        # IF THE USER IS NOT AUTHENTICATED means GUEST USER
    else:
        product_variation =[]
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation=Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        
        try:
            # get the cart using the cart_id present in the session
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list=[]
            id =[]
            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                if item.quantity < product.stock:
                    item.quantity += 1
                    item.save()
                    messages.success(request, "No stock!!")
                    return redirect('cart')

        else:
                cart_item = CartItem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation)>0:
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variation)
                cart_item.save()
        return redirect('cart')

#=============== Cart ===================#

def cart(request,total=0,quantity=0,cart_items=None):
    discount=0
    code="NO COUPON APPLIED"
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for i in cart_items:
            total += (i.product.price * i.quantity)
            quantity += i.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass   # it means just ignore
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.get(coupon_code = coupon)

        if not coupon_obj:
            messages.warning(request,"Your account")
            return redirect('cart')
        else:
            i.coupon = coupon_obj
            grand_total = int(grand_total - i.coupon.discount_price)
            print(i.coupon)
            i.save()
            code = i.coupon.coupon_code
            discount = i.coupon.discount_price
            print(code)

    context = {
        'discount' : discount,
        'code' : code,
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render (request,'cart.html',context)

#===============Remove Cart==============#

def delete_cart_item(request,id,product_id):
    try:
        product = get_object_or_404(Product,id=product_id)
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product,user=request.user,id=id)
            
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product=product,id=id,cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

#============Decrease Quantity=============#

def decrease_quantity(request,product_id,id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product,user=request.user,id=id)
    else:
        cart = Cart.objects.get(cart_id =_cart_id(request))
        cart_item = CartItem.objects.get(product=product,cart=cart,id=id) #it brings cart items
    
    cart_item.delete()
    return redirect('cart')


























# ================Cart==============#
# def cart(request,total=0,quantity=0,cart_items=None):
#     grand_total=0
#     tax =0
    
#     try:
#         if request.user.is_authenticated:
#             cart_items = CartItem.objects.filter(current_user_id = request.user.id, is_active=True) #this is for loged users ,taking objects by cart id
#         else:
#             cart=Cart.objects.get(cart_id =_cart_id(request))  #this is for non logged users ,taking cart object with cart_id
#             cart_items =CartItem.objects.filter()
        
#         for cart_item in cart_items:
#             total_price += (cart_item.product.price*cart_item.quantity) #looping a cart items and taking total of each cart item
#             quantity += cart_item.quantity
#         tax =(2*total)/100
#         grand_total = total+tax
#             # if cart_item.product.offer_price():
#                 # offer_price = Product.offer_price(cart_item.product)
#                 # total +=(offer_price["new_price"]*cart_item.quantity)
#                 # total = round(total,2)
                
#             # else:
#             #     total +=(cart_item.product.price*cart_item.quantity)
#             # quantity += cart_item.quantity
#             # saved = total_price-total
#             # saved = round(saved,2)
#     except:
#         pass
#     context = {
#         'total':total,
#         'quantity':quantity,
#         'cart_items':cart_items,
#         'tax':tax,
#         'grand_total':grand_total
#         }
#     return render(request,'cart.html',context)

# =============Add Cart===============#
# def add_cart(request,product_id):
#     current_user = request.user                                               #we want a prdct id snd using id and added to the cart
#     product = Product.objects.get(id=product_id)  #get the product
#     if current_user.is_authenticated:
#         try:
#             cart = Cart.objects.get(cart_id=_cart_id(request))  #get the cart using the cart_id present in the session of the each product it will get when you added on a cart it automatically create a session
#         except Cart.DoesNotExist:
#             cart = Cart.objects.create(                   #cart does not exist then create new cart
#             cart_id = _cart_id(request)
#         )
#     cart.save()
#     cart_item_exists = CartItem.objects.filter(product=product,cart=cart)
# #combine product and cart
    
#     try:
#         cart_item = CartItem.objects.get(product=product, cart=cart)        #this bring cart item
#         cart_item.quantity += 1  
#         cart_item.save()                                              #click on a cart button it will automatically increase
#         # cart_item.current_user = Fitness.objects.get(id=request.user.id)
#         # print(Fitness.objects.get(id=request.user.id))                      #cart_item.quantity=cart_item.quantity +1
        
#     except CartItem.DoesNotExist:
#         cart_item = CartItem.objects.create(                    #cart does not exist then create new cart
#             product = product,
#             quantity = 1,                    
#             cart = cart,
#         )
#         cart_item.save()
#     return redirect('cart') 






























    #=============== Carts =================#

# def carts(request,total=0,quantity=0,cart_items=None):
#     try:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#         cart_items = CartItem.objects.all()
#         print(cart,cart_items)
#         for cart_item in cart_items:
#             total += (cart_item.product.price * cart_item.quantity)
#             quantity += cart_item.quantity
#         # tax= (2 * total)/100
#         # grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass  #ignore the objects
    
#     context = {
#         'total' : total,
#         'quantity' :quantity,
#         'cart_items' :cart_items,
#         # 'tax'       : tax,
#         # 'grand_total' :grand_total
#     } 

#     return render(request,'cart.html',context)
