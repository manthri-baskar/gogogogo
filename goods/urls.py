from django.urls import path
from .views import *

app_name = 'goods' 

urlpatterns = [ 
    path('', goods_form_view, name='goods_form_url'),
    path('amount/', amount_form_view, name='amount_form_url'),
    path('delete_items/', delete_goods, name="delete_goods_url"),
    path('raw_to_good/', add_rawTo_good, name="add_rawTo_good_url"),
] 