from django.urls import path

from.import views

urlpatterns = [
    path('coupon_actives/<int:id>/',views.coupon_actives,name='coupon_actives'),
    path('coupon_manage/',views.coupon_manage,name='coupon_manage'),
    path('add_coupon/',views.add_coupon,name='add_coupon'),
    path('delete_coupon/<int:id>/',views.delete_coupon,name='delete_coupon')
]