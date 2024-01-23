from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from Cart.models import CartItem
from django.contrib.auth.decorators import login_required
from Coupon.models import Coupon
from django.contrib import messages
from .forms import CouponForm
# Create your views here.

#=================Coupon Manage=================#
@login_required(login_url='adminsignin')
def coupon_manage(request):
    coupon = Coupon.objects.all()
    messages.success(request,'Deleted Successfully')
    return render(request,'Admin/coupon_manage.html',{'coupon':coupon})

#================Add Coupon=====================#
@login_required(login_url='adminsignin')
def add_coupon(request):

    if request.user.is_authenticated:
        if request.method == 'POST':
            cpnform = CouponForm(request.POST,request.FILES)

            print(cpnform.errors)
            if cpnform.is_valid():
                cpnform.save()
            return redirect('coupon_manage')
        cpnform = CouponForm()
        context = {
            'cpnform':cpnform
        }
        return render(request,'Admin/add_coupon.html',context)
    else:
        return redirect('adminsignin')

#=================Delete Coupon=================#

def delete_coupon(request,id):
    coupon = Coupon.objects.get(id =id)
    coupon.delete()
    
    return redirect('coupon_manage')

#==================Coupon Active================#


@login_required(login_url='adminsignin')
def coupon_actives(request,id):
    coupon = Coupon.objects.get(id=id)
    
    if request.method == 'POST':
        if coupon.is_expired == True:
            coupon.is_expired =False
            coupon.save()
        
        else:
            
            coupon.is_expired =True
            coupon.save()
        print("//////\\\\\\\\\\")
    return redirect('coupon_manage')
