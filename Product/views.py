
from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
# from Fitness import Category, Product
from Category.models import Subcategory,Category
from .models import Product
from Cart.models import CartItem
from Cart.views import _cart_id
# Create your views here.
# Product Management
from Cart.models import Variation
from .forms import VariationForm
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
#==============Product Display===================#
@never_cache
@login_required(login_url='adminsignin')
def admin_productlist(request):
    if request.user.is_authenticated:
        data = Product.objects.filter()
        context = {
            'product_display':data
            }
        return render(request,'Admin/product.html',context)
        # return redirect('add_product')


#===============Add Product==================#

@never_cache
def add_product(request):
    if request.user.is_authenticated:
        category = Category.objects.all()
        subcategory = Subcategory.objects.all()
        product = Product.objects.all()
        context = {
            'category':category,
            'subcategory':subcategory,
            'product':product
        }
        if request.method =='POST':
            if request.POST.get('prdct_name') and request.POST.get('prdct_price') and request.POST.get('prdct_stock') and request.POST.get('prdct_desc') and request.POST.get('subcat_list') and request.POST.get('cat_list') and request.FILES['prdct-img1'] and request.FILES['prdct-img2'] and request.FILES['prdct-img3'] and request.FILES['prdct-img4']:
                product_name = request.POST.get('prdct_name')
                product_desc = request.POST.get('prdct_desc')
                product_price= request.POST.get('prdct_price')
                product_stock= request.POST.get('prdct_stock')
                if Product.objects.filter(prdct_name=product_name).exists():
                    messages.error(request,'Product name already exists')
                    return redirect ('admin_productlist')
                product = Product()
                product.prdct_name  = product_name
                product.slug        = slugify(product_name)
                product.prdct_desc  = product_desc
                product.price       = product_price
                product.stock       = int(product_stock)
                product.subcategory = request.POST.get('subcategory')
                product.category    = request.POST.get('category')
                if 'prdct-img1' in request.FILES:
                        product.img1 =request.FILES['prdct-img1']
                if 'prdct-img2' in request.FILES:
                        product.img2 =request.FILES['prdct-img2']
                if 'prdct-img3' in request.FILES:
                        product.img3 =request.FILES['prdct-img3']
                if 'prdct_img4' in request.FILES:
                        product.img4 =request.FILES['prdct-img4']

                if product.stock <1:
                        product.is_available =False
                else:
                        product.is_available =True
                product.save()
                messages.success(request,'New product added')
                return redirect('admin_productlist')
            else:
                messages.error(request,'Required all fields..!!')
                return redirect('add_product')
        return render (request,'Admin/add_product.html',context)
    else:
            return render(request,'Admin/adminsignin.html')

#==========Product Edit=============#

def edit_product(request):
    category = Category.objects.all()
    subcategory = Subcategory.objects.all()
    # productlist    = Product.objects.all()
    if request.method =='POST':
        product_name = request.POST.get('prdct_name')
        slug= slugify(product_name)
        description = request.POST.get('prdct_desc') 
        price = request.POST.get('prdct_price') 
        stock = request.POST.get('prdct_stock')
        subcategory = request.POST.get('subcategorylist')
        category    = request.POST.get('categorylist')
        product_img1 = request.FILES.get('prdct-img1')
        product_img2 = request.FILES.get('prdct-img2')
        product_img3 = request.FILES.get('prdct-img3')
        product_img4 = request.FILES.get('prdct-img4')
        product = Product.objects.create(prdct_name=product_name,slug=slug,prdct_desc=description,price=price,stock=stock,category=category,subcategory=subcategory,img1=product_img1,img2=product_img2,img3=product_img3,img4=product_img4)
        product.save()
        return redirect('admin_productlist')
        
    else:
        context = {
            'categorylist':category,
            'subcategorylist':subcategory,
            # 'product'  :productlist
        }
    return render(request,'Admin/edit_product.html',context)

#==========Product Delete===========#

def prdctlist_delete(request,id):
    list = Product.objects.get(id=id)
    list.delete()
    return redirect('admin_productlist')
#=============Product List Edit===========#

def prdctlist_edit(request,id):
    product = Product.objects.get(id=id)
    print(product.prdct_name,product.prdct_desc,product.slug,product.price,product.stock,product.created_date)
    return render(request,'Admin/edit_product.html',{'product':product})

#==================Store Page==================#

def store(request,category_slug=None):
        categories = None
        products   = None
        if category_slug != None:
                categories = get_object_or_404(Category,slug=category_slug)
                products   = Product.objects.filter(category=categories,is_available=True)
        else:
            products = Product.objects.filter(is_available=True)
        context = {
                'products' :products,               
        }
        return render(request,'store.html',context)


#===============Single Product Details==========#

def product_details(request,id):
    try:
      
        single_product = Product.objects.get(id=id)         
           
    except Exception as e:
            raise e

    context = {
        'single_product' : single_product,
        
    } 
    return render(request,'product_details.html',context)

# Admin Side
#===============Variation================#

@login_required(login_url='adminsignin')
def variation(request):
    Pvariation = Variation.objects.all()

    context = {
        'Pvariation': Pvariation

    }
      
    return render(request,'Admin/variations.html',context)


#===============Add Variation==============#

@login_required(login_url='adminsignin')
def add_variation(request):
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            varform = VariationForm(request.POST)

            print(varform.errors)
            if varform.is_valid():
                varform.save()
            return redirect('variation')
        varform = VariationForm()
        context = {
            'varform':varform
        }
        return render(request,'Admin/add_variations.html',context)
    
    else:
        return redirect('variation')


#==============Variation Block=============# 

@login_required(login_url='adminsignin')
def var_block(request,id):
    variant = Variation.objects.get(id=id)
    
    if request.method == 'POST':
        if variant.is_active == True:
            print(variant.is_active)
            variant.is_active =False
            variant.save()
        
        else:
            print(variant.is_active)
            variant.is_active =True
            variant.save()
        print("//////\\\\\\\\\\")
    return redirect('variation')
 
#================Delete Variant===============#

@login_required(login_url='adminsignin')
def delete_variant(request,id):
    variation = Variation.objects.get(id=id)
    if request.method == 'POST':
        variation.delete()
        return redirect('variation')

#===============Search Product=================#

# def search(request):
#     if 'key' in request.GET:
#         key = request.GET['key']
#         if key:
#             products = Product.objects.order_by('-created_date').filter(Q(prdct_desc__icontains=key)|Q(prdct_name__icontains=key)) 
#             product_count = products.count()
#     context = {
#         'products':products,
#         'product_count':product_count
#     }
#     return render (request,'search.html',context)


#================Price High=====================#

def price_high(request):
    products = Product.objects.all().filter(is_available=True).order_by('-price')
    category = Category.objects.all()
    variation = Variation.objects.all()
    products_paginater = Paginator(products,8)

    page_number = request.GET.get('page')
    try:
        page_obj = products_paginater.get_page(page_number)
    except PageNotAnInteger:
        page_obj = products_paginater.page(1)
    except EmptyPage:
        page_obj = products_paginater.page(products_paginater.num_pages)
    context ={
        'page_obj': page_obj,
        'variation':variation,
        'category' : category
    }
    return render(request, 'store.html', context)


#===================Price Law==================#

def price_low(request):
    products = Product.objects.all().filter(is_available=True).order_by('price')
    category = Category.objects.all()
    variation = Variation.objects.all()
    products_paginater = Paginator(products,8)

    page_number = request.GET.get('page')
    try:
        page_obj = products_paginater.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = products_paginater.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = products_paginater.page(products_paginater.num_pages)
    context = {
        'page_obj': page_obj,
        'variation':variation,
        'category' : category,
    }
    
    return render(request, 'store.html', context)


#=============Newest Product=================#

def newest(request):
    products = Product.objects.all().filter(is_available=True).order_by('-created_date')
    category = Category.objects.all()
    variation = Variation.objects.all()
    products_paginater = Paginator(products,8)


    page_number = request.GET.get('page')
    try:
        page_obj = products_paginater.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = products_paginater.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = products_paginater.page(products_paginater.num_pages)
    context = {
        'page_obj': page_obj,
        'variation':variation,
        'category' : category,
    }
    
    return render(request, 'store.html', context)


#======================Store View=================#

def store_view(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')
    category = Category.objects.all()
    variation = Variation.objects.all()
    products_paginater = Paginator(products,8)
    page_number = request.GET.get('page')
    try:
        page_obj = products_paginater.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = products_paginater.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = products_paginater.page(products_paginater.num_pages)
    context = {
        'page_obj': page_obj,
        'variation':variation,
        'category' : category,
    }
    
    return render(request, 'store.html', context)
