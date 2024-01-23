from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Category, Subcategory
from django.utils.text import slugify
from django.contrib.auth import views as auth_views  
from django.http import JsonResponse
# from .forms import CategoryForm
# Create your views here.
#    Category Management

@never_cache
@login_required(login_url='signin')
def admin_category(request):

    return render(request,'Admin/category.html')

#============Category=============#

def category(request):
    category_display = Category.objects.all()
    
    return render(request,'Admin/category.html',{"category_display":category_display}) 


#==============Add Category===========#

def add_category(request):
    if request.method =='POST':
        category=request.POST.get('ctgry_name')
        image=request.FILES.get('ctgry_img')
        slug=slugify(category)
        cat=Category.objects.create(category_name=category,category_image=image,slug=slug)
        cat.save()
       
        return redirect('category')
        
    return render(request,'Admin/add_category.html')
    
#=============Edit Categroy=============#

def edit_category(request):
    if request.method == 'POST':
        category=request.POST.get('editcat_name')
        image=request.FILES.get('editcat_img')
        slug=slugify('categroy')
        cat=Category.objects.create(category_name=category,category_image=image,slug=slug)
        cat.save()
        return redirect('category')
    return render(request,'Admin/edit_category.html')


#=============Subcategory==============#

def subcategory(request):
    subcategory_display = Subcategory.objects.all()

    return render(request,'Admin/subcategory.html',{"subcategory_display":subcategory_display})

def  add_subcategory(request):
    category= Category.objects.all()
    if request.method =='POST':
        sub_name=request.POST.get('subcat_name')
        sub_image=request.FILES.get('subcat_img')
        sub_list=request.POST.get('subcat_list')
        category = Subcategory.objects.create(subcat_name=sub_name,subcat_image=sub_image,subcat_list=sub_list)
        category.save()
        
        return redirect('subcategory')
    else:
        context = {
            'category':category
             
        }
        return render(request,'Admin/add_subcategory.html',context)

#===============Add Subcategory===========#

def save_subcate (request):

    select_category=request.GET.get('choosed_option')
    image=request.GET.get('img')
    print()
    print(select_category,image)

    return JsonResponse({'msg':"successfully added"})

#================Category List delete================#

#id set as a integer it already asigned in a database
def catgrylist_delete(request,id):
    list = Category.objects.get(id=id)
    list.delete()
    return redirect('category')

# =============Category List Edit=============#

def editcat_list(request,id):
    list = Category.objects.get(id=id)
    print(list.category_name,list.slug,list.category_image)
    
    return render(request,'Admin/edit_category.html',{'list':list})

#================Sub Category List delete==========#

def subcatgrylist_delete(request,id):
    sublist = Subcategory.objects.get(id=id)
    sublist.delete()
    return redirect('subcategory')

#================Subcategory list Delete=============#

def editsubcat_list(request,id):
    sublist =Subcategory.objects.get(id=id)
    print(sublist.subcat_name,sublist.subcat_image,sublist.subcat_list,sublist.category)

    return render(request,'Admin/edit_subcategory.html',{'sublist':sublist})


#==================Edit SubCategy==================#


def edit_subcategory(request):
    if request.method == 'POST':
        subcategory=request.POST.get('editsubcat_name')
        image=request.FILES.get('editsubcat_img')
        category_id=request.POST.get('editcategory')
        subcategory_list=request.POST.get('subcatlist')
        subcat=Subcategory.objects.create(subcat_name=subcategory,subcat_image=image,category=category_id,subcat_list=subcategory_list)
        subcat.save()
        return redirect('subcategory')
    return render(request,'Admin/edit_subcategory.html')
