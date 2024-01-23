import datetime
from django.shortcuts import render,redirect
from Order.models import Order,OrderProduct,Address
from Cart.models import CartItem,Cart
from Product.models import Product
import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from Cart.views import _cart_id
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.http import HttpResponse
# Create your views here.

#==============Admin User Order List Page===============#

@login_required(login_url='adminsignin')
def admin_order(request):
    order = Order.objects.all().order_by('-created_at')
    context ={
        'order':order
    }
    return render(request,'Admin/admin_order.html',context)

#=============User Order Page list==============#


@login_required(login_url='login')
def user_order(request):
    order = Order.objects.filter(user=request.user).order_by('created_at')

    orderproduct = OrderProduct.objects.all()
    context = {
        'order':order,
        'orderproduct':orderproduct
    }
    return render(request,'user_order.html',context)


# ==============Order Product Details=============#

@login_required(login_url='login')
def order_details(request,order_id):
    order = Order.objects.get(id=order_id)
    address = Address.objects.filter()
    order_details = OrderProduct.objects.filter(order_number=order.order_number)
    subtotal = 0
    tax = 0
    order_total = 0

    for i in order_details:
        subtotal += i.product_price * i.quantity
        tax = ( 2*subtotal )/100
        order_total = subtotal + tax

    context = {
        'order':order,
        'address':address,
        'order_details':order_details,
        'subtotal':subtotal,
        'tax':tax,
        'order_total':order_total
    }
    return render(request,'order_details.html',context)

#================Cancel Order==================#

@login_required(login_url='login')
def cancel_order(request,order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.status = 'Cancelled'
        order.save()
    return redirect('user_order')

#=================Check Out====================#

@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_item=None):
    try:
        discount=0
        tax= 0
        grand_total =0
        if request.user.is_authenticated:
            cart_item = CartItem.objects.filter(user=request.user, is_active=True)
            address = Address.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.filter(cart=cart,is_active=True)
        for i in cart_item :
            total += (i.product.price * i.quantity) 
            quantity += i.quantity
        tax = (2 * total)/100
        grand_total = total + tax
        try:
            grand_total = grand_total - i.coupon.discount_price
            discount = i.coupon.discount_price
        except:
            pass
    except ObjectDoesNotExist:
        pass
    context = {
        'tax':tax,
        'discount':discount,
        'address':address,
        'total':total,
        'quantity': quantity,
        'cart_item':cart_item,
        'tax':tax,
        'grand_total':grand_total,
    }

    return render(request,'checkout.html',context)


#===========Add Address to a same check out Page=========#

def add_address(request):
    if not request.user.is_authenticated:
        messages.info(request,'Guest')
        return redirect(request.META.get('HTTP_REFERER'))
    if request.POST:
        First_name = request.POST.get('first_name')
        Last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        Email = request.POST.get('email')
        Address1 = request.POST.get('address_1')
        Address2 = request.POST.get('address_2')
        Ordernote = request.POST.get('notes')
        country = request.POST.get('country')
        state  = request.POST.get('state')
        dist = request.POST.get('dist')
        pin_code = request.POST.get('pincode')
        address = Address.objects.create(user=request.user,first_name=First_name,
        last_name =Last_name,phone=phone,address_1=Address1,address_2=Address2,
        email=Email,country=country,state=state,dist=dist,pincode=pin_code,
        order_note=Ordernote)

        address.save()
        print(address)
        # context = {
        #     'first_name': First_name,
        #     'last_name' : Last_name,
        #     'phone'     : phone,
        #     'email'     : Email,
        #     'address'   : Address1,
        #     'country'   : country,
        #     'state'     : state,
        #     'dist'      : dist,
        #     'pincode'   : pin_code

        # }
    return render(request,'checkout.html')


#=================View Address===============#

# @login_required(login_url='login')
# def view_address(request):
#     address = Address.objects.filter()

#     return render(request,'checkout.html',{'address':address})

#=======================Order Success Page=========================#

def ordrsuccess(request):

    return render(request,'ordersuccess.html')

#=================Place Order with required Payment Method=============#

def place_order(request, total=0, quantity=0):
    current_user = request.user
    
  
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        address_id = request.POST['address']
        shipping_address = Address.objects.get(id=address_id)
        # form = OrderForm(request.POST)
  
        data = Order()
        data.user = current_user
        data.address = shipping_address
        data.order_total = grand_total
        data.tax = tax
        data.payment_mode ="Cash On Delivery"
        # data.ip = request.META.get('REMOTE_ADDR')
        data.save()
            # Generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d") #20210305
        order_number = current_date + str(data.id)
        data.order_number = order_number
        
        data.save()
# ===================================================================================================================
        # order = Order.objects.get(user=request.user, is_orderd=False)
        # order.is_orderd = True
        # order.save()

        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            
 
            orderproduct=OrderProduct()
            # orderproduct.order = order
            # orderproduct.order_number = order.order_number 
                #orderproduct.payment = payment
            orderproduct.user = request.user
            orderproduct.product = item.product
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation= cart_item.variation.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variation.set(product_variation)
            orderproduct.save()


                # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # Clear cart
        CartItem.objects.filter(user=request.user).delete()
        
        
        
        return redirect('ordrsuccess')              

            

@login_required(login_url='login')
def razorpaycheck(request):
    cart = CartItem.objects.filter(user=request.user)
    total_price = 0
    tax = 0
    total = 0
    quantity =0
    for item in cart:
        total_price = total_price + item.product.price * item.quantity
        quantity += item.quantity
        tax = (2*total)/100
        grand_total = total + tax

    return JsonResponse({
        'grand_total' : grand_total
    })

def orders(request):
    return HttpResponse("My orders page")



#=================Order Place with Rzorpay & PayPal=======================#


def order_place(request, total=0, quantity=0):
    current_user = request.user
    
  
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        address_id = request.POST['address']
        shipping_address = Address.objects.get(id=address_id)
        # form = OrderForm(request.POST)
  
        data = Order()
        data.user = current_user
        data.address = shipping_address
        data.order_total = grand_total
        data.tax = tax
        data.payment_id = request.POST['payment_id']
        data.payment_mode =request.POST['payment_mode']
        # data.ip = request.META.get('REMOTE_ADDR')
        data.save()
            # Generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d") #20210305
        order_number = current_date + str(data.id)
        data.order_number = order_number
        
        data.save()
# ===================================================================================================================
        order = Order.objects.get(user=request.user, is_orderd=False)
        order.is_orderd = True
        order.save()

        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            
 
            orderproduct=OrderProduct()
            orderproduct.order = order
            orderproduct.order_number = order.order_number 
                #orderproduct.payment = payment
            orderproduct.user = request.user.id
            orderproduct.product = item.product
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation= cart_item.variation.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variation.set(product_variation)
            orderproduct.save()


                # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # Clear cart
        CartItem.objects.filter(user=request.user).delete()
        # else:
        payMode = request.POST['payment_mode']
        if (payMode == 'Paid by Razorpay' or payMode == 'Paid by Paypal' ):
            return JsonResponse({'status' : "Your order placed"})
        else:
            pass
        
        
        return redirect('ordrsuccess') 
        #     return redirect()




