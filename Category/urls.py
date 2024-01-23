from django.urls import path
from . import views
urlpatterns = [
    #===============Category==============#
    path('',views.admin_category,name='admin_category'),
    path('add_category',views.add_category,name='add_category'),
    path('category/',views.category,name='category'),
    path('edit_category',views.edit_category,name='edit_category'),
    path('editcat_list<int:id>/',views.editcat_list,name='editcat_list'),
    path('catdelete/<int:id>/',views.catgrylist_delete,name='catgrylist_delete'),

    #================SubCategory===========#
    path('subcategory/',views.subcategory,name='subcategory'),
    path('add_subcategory',views.add_subcategory,name='add_subcategory'),
    path('saver',views.save_subcate,name="saver"), 
    path('editsubcat_list<int:id>/',views.editsubcat_list,name='editsubcat_list'),
    path('subcatdelete/<int:id>/',views.subcatgrylist_delete,name='subcatgrylist_delete'),
    path('edit_subcategory/',views.edit_subcategory,name='edit_subcategory')
]
