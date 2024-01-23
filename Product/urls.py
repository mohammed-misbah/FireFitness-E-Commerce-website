from django.urls import path

from.import views

urlpatterns = [
    path('',views.admin_productlist,name='admin_productlist'),
    path('add_product',views.add_product,name='add_product'),
    path('prdctlist_delete/<int:id>/',views.prdctlist_delete,name='prdctlist_delete'),
    path('store/',views.store,name='store'),
    path('<slug:category_slug>/',views.store,name='products_by_category'),
    path('product_details/<int:id>/',views.product_details,name='product_details'),
    path('edit_product',views.edit_product,name='edit_product'),
    path('prdctlist_edit/<int:id>/',views.prdctlist_edit,name='prdctlist_edit'),
    path('variation',views.variation,name='variation'),
    path('add_variation',views.add_variation,name='add_variation'),
    path('var_block/<int:id>/',views.var_block,name='var_block'),
    path('delete_variant/<int:id>/',views.delete_variant,name='delete_variant'),
    # path('search/',views.search,name='search')


    path('price_high/',views.price_high,name='price_high'),
    path('price_low/',views.price_low,name='price_low'),
    path('newest/',views.newest,name='newest'),
    path('store_view/',views.store_view,name='store_view')
]

#<slug:category_slug><slug:product_slug>/