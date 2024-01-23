from django.urls import path
from .import views

urlpatterns = [
    path('cart/',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('delete_cart_item/<int:id>/',views.delete_cart_item,name='delete_cart_item'),
    path('decrease_quantity/<int:id>/<int:product_id>/',views.decrease_quantity,name='decrease_quantity')
]
