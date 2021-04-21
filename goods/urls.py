from django.urls import path
from .views import *

app_name = 'goods' 

urlpatterns = [ 
    path('', goods_form_view, name='goods_form_url'),
    path('details/<str:pk>/<str:pk1>/', details_form_view, name='details_form_url'),
    path('delete_items/', delete_goods, name="delete_goods_url"),
    path('company_info/', company_info, name="company_info_url"),
    path('raw_to_good/<str:pk>/<str:pk1>/', add_rawTo_good, name="add_rawTo_good_url"),
    path('update_item/<str:pk>/<str:pk1>/',update_items,name="update_item_url"),  
    path('delete3/<str:pk>/<str:pk1>/<str:pk2>',remove_raw_from_good,name="remove_rawfromgood_url"),  
    path('delete_good/<str:pk>/<str:pk1>',delete_good,name="delete_good_url"),  
]