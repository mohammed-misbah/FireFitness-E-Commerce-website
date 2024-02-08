from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth import authenticate
from django.contrib.auth import login as loogin
from django.contrib.auth.decorators import login_required
from .models import User
from Product.models import Product
from Protien import otp
from ast import literal_eval
from Cart.models import Cart,CartItem
from Cart.views import _cart_id 
from Order.models import *

# Create your views here.

#=============Home Page=============#

def home(request):
    products = Product.objects.filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request,"home.html",context)

#=============Register Page============#

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phoneNumber = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is Taken')
                return redirect('register')

            elif len(phoneNumber) < 10 or len(phoneNumber) > 14:
                messages.error(request, 'Phone number is not valid!!!')
                return redirect('register')

            elif User.objects.filter(email=email).exists() or User.objects.filter(phone_number=phoneNumber).exists():
                messages.error(request, 'The user is already taken')
                return redirect('register')

            else:
                # Create a new user if all conditions are satisfied
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, 'Registration successful!')
                return redirect('login')

        else:
            messages.info(request, 'Passwords do not match')
            return redirect('register')

    else:
        return render(request, 'register.html')
    
# def register(request):
#     if request.method =='POST':
#         # is_private = request.POST.get('is_private', False)

#         username=request.POST['username']
#         email=request.POST['email']
#         phoneNumber=request.POST['phone_number']
        
#         password1=request.POST['password1']
#         password2=request.POST['password2']
#         if password1==password2:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request,'name is Taken')
#                 return redirect('register')
            
#             elif len(phoneNumber)<10 or len(phoneNumber) > 14:
#                 messages.error(request,'Phone-number is not Valid!!!')
#                 return redirect('register')
#             elif User.objects.filter(email=email).exists() or User.objects.filter(phone_number=phoneNumber).exists():
#                 messages.error(request,'The User is Already Taken')
#                 return redirect('register')
                
            # else:
            #   print(phoneNumber)
            #   msg =  otp.send_request(phoneNumber)
            #   if msg == True:
            #     messages.success(request,'Otp Sended Successfully')
            #     print("in true")
            #     dict = {         
            #         'username' : username,
            #         'email' : email,
            #         'phone_number' : phoneNumber,
            #         'password' : password1
            #       }
            # res =  render(request,'otp.html')
            # res.set_cookie('userdetails',dict)
            # return res
    #         else:
    #             print("in else")
    #             messages.error(request,'Something went wrong!!!')
    #             return redirect('register')  

    #     else:
            
    #         messages.info(request,'password is not matching')
    #         return redirect('register')
        
    # else:
    #     return render(request,'register.html')

#==============Login Page==============#

def login(request):
    print(request.method)
    if request.method =='POST':
        print("innn")
        username=request.POST['username']
        password=request.POST['password']
        print(username,password)
        user = authenticate(email=username,password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cartt_id = _cart_id(request))
                cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request,user)
            return redirect('/')
            
        else:
            messages.error(request,'invalid login credentials')
            return redirect('login')
            
    else:
        return render(request,'login.html')

#==============Logout Page============#
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,"You are logged out")
    return redirect('login')

#============OTP validate================#


def otp_login_validate(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST' and request.POST['otp']:
        otp1 = int(request.POST['otp'])
        userdetails = literal_eval(request.COOKIES.get('userdetails'))
        print(userdetails['phone'],"in cookie")
        response = otp.verify_Otp(otp1, userdetails['phone'])
        print(response)
        if response == None:
            messages.error(request,'OTP is invalid')
            return redirect('otp_login_validate')
        else:
            user = User.objects.create_user(username=userdetails['username'],email=userdetails['email'],phone_number=userdetails['phone'],password=userdetails['password'])
            loogin(request,user)
            res = redirect('home')   
            res.delete_cookie('userdetails')
            return res 

    return render(request,'otp.html')


def otp_validate(request):
    if request.method == 'POST' and request.POST['otp']:
        otp1 =request.POST.get('otp')
        username=request.POST['username']
        email=request.POST['email']
        phoneNumber=request.POST['phone_number']
        password=request.POST('password1')
      
        if otp_validate == 'approved':
           
            messages.info(request,"Account Created")
            return redirect('home')
        else: 
          messages.info(request,"Wrong OTP")
          context = {
            'username'  : username,
            'email' : email,
            'phone_number' : phoneNumber,
            'password1'  : password,
          }
          return render(request,'otp.html',context)
    return render(request,'otp.html')


#================Dash board===================#

@login_required(login_url='login')
def dashboard(request):
    # send_message()

    order = Order.objects.order_by('-created_at').filter(user_id = request.user.id)
    order_count = order.count()

    print(order_count)
    context = {
        'order_count':order_count,
    }

    return render(request,'Userprofile/dashboard.html',context)


#===============My Order Details================#


@login_required(login_url='login')
def my_orders(request):
    order = Order.objects.filter(user=request.user).order_by('-created_at')
    ordersproduct = OrderProduct.objects.all()
    context = {
        'order': order,
        'ordersproduct' : ordersproduct
    }
    return render(request, 'Userprofile/my_orders.html', context) 


#=============Address Manage===============#

def address_manage(request):
    address = Address.objects.filter(user = request.user)
    
    return render(request, 'Userprofile/address.html',{ 'address':address})


