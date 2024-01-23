from django.shortcuts import render,redirect
from Product.models import Product
from Offer.models import *
from .forms import *
from django.contrib import messages
from Category.models import *
# Create your views here.


#=================Product Offer====================#

def product_offer(request):
    prdct = Product.objects.all()
    prdctoffer = Productoffer.objects.all()

    if request.method == 'POST':
        discount = int(request.POST.get('discount'))
        product = request.POST.get('product')
        is_active = request.POST.get('is_active')
        print(discount)
        print(product)
        print(is_active)
        if Productoffer.objects.filter(product=product).exists():
            print('is exists')
            messages.success(request,'Offer is exists')
        else:
            print('No')
            Productoffer.objects.create(product=product,discount=discount,is_active=is_active)
            product = Product.objects.get(prdct_name=product)
            print(product.prdct_name)
            if product.offer_percentage < discount:
                price = float(product.original_price)
                product.price = price-price*float(discount)/100
                product.offer_percentage = discount
                print(discount)
                product.save()
                messages.success(request,'Offer is Applied')

            else:
                pass
        return redirect('product_offer')
    context = {
            'prdct':prdct,
            'prdctoffer':prdctoffer,
        }
    return render(request,'Admin/product_offer.html',context)

#==================Delete ProductOffer==============#

def delete_product_offer(request,id):
    prdctoffer = Productoffer.objects.get(id = id)
    product = Product.objects.get(prdct_name = prdctoffer.product)

    if Categoryoffer.objects.filter(category = product.category).exists():
        catoffer = Categoryoffer.objects.get(category = product.category)
        discount = catoffer.discount
        price = float(product.original_price)
        product.price = price-price*float(discount)/100
        product.offer_percentage = discount
        product.save()
        messages.success(request,'Offer is Deleted')
    else:
        product.price = product.original_price
        product.offer_percentage = 0
        product.save()
        messages.success(request,'Offer is deleted')
    prdctoffer.delete()

    return redirect('category_offer')


#================Category Offer====================#

def category_offer(request):
    catgry = Category.objects.all()
    catgryoffer = Categoryoffer.objects.all()

    if request.method == 'POST':
        discount = int(request.POST.get('discount'))
        category=request.POST.get('category')
        is_active=request.POST.get('is_active')
        
        if Categoryoffer.objects.filter(category=category).exists():
            print('is exists')
            messages.success(request , 'Offer is exists')
        else:
            Categoryoffer.objects.create(category=category,discount=discount,is_active=is_active)
            category = Category.objects.get(category_name=category)
            product = Product.objects.filter(category=category)
            for items in product:
                print(type(items.offer_percentage))
                print(type(discount))
                if items.offer_percentage < discount:
                    print(category)
                    print(discount)
                    print(is_active)
                    print(items.prdct_name)
                    price = float(items.original_price)
                    items.price=price-price*float(discount)/100
                    items.offer_percentage = discount
                    items.save()
            messages.success(request,'Offer added Successfully')
            return redirect('category_offer')
    context = {
        'catgryoffer':catgryoffer,
        'catgry':catgry,
    }

    return render(request,'Admin/category_offer.html',context)


#===================Delete Category Offer================#

def delete_category_offer(request,id):
    catgryoffer = Categoryoffer.objects.get(id = id)
    catgry = Category.objects.get(category_name=catgryoffer.category)
    prdct = Product.objects.filter(category=catgry)
    discount = catgryoffer.discount
    for items in prdct:
        if Productoffer.objects.filter(product=items.prdct_name).exists():
            prdctoffer = Productoffer.objects.get(product=items.prdct_name)
            discount = prdctoffer.discount
            print(items.prdct_name)
            product = Product.objects.get(prdct_name =items.prdct_name)
            price = float(product.original_price)
            product.price = price-price*float(discount)/100
            product.offer_percentage = discount
            print()
            print(product.offer_percentage)
            product.save()
        else:
            print(items.prdct_name)
            items.price= items.original_price
            items.offer_percentage = 0
            items.save()
    catgryoffer.delete()
    return redirect('category_offer')
