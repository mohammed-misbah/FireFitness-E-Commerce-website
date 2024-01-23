from django.urls import path
from . import views
urlpatterns = [
    
    path('',views.admin,name='admin'),
    path('adminsignin',views.adminsignin,name='adminsignin'),
    path('adminsignout',views.adminsignout,name='adminsignout'),
    path('user_detailes/',views.user_detailes,name='user_detailes'),
    path('user_delete/<int:id>/',views.user_delete,name='user_delete'),
    path('user_block/<int:id>/',views.user_block,name='user_block'),
    
    path('adminuser',views.user_detailes,name='adminuser'),
    path('admin_graph/',views.admin_graph,name='admin_graph'),
    path('sales_report_date',views.sales_report_date, name='sales_report_date'),
    path('export_to_pdf',views.export_to_pdf, name='export_to_pdf'),
    path('export_to_excel',views.export_to_excel, name='export_to_excel')
    
    
    # path('index1/',views.index,name='index1')
   ]
