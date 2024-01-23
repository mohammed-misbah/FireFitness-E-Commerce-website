from django.urls import path
from . import views
urlpatterns = [
    
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('otp_validate/',views.otp_validate,name='otp_validate'),
    path('otp_login_validate',views.otp_login_validate,name='otp_login_validate'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('address_manage/',views.address_manage,name='address_manage'),
    
]