from django.urls import path
from .views import *

app_name = 'csvs'

urlpatterns = [
    path('purchase/', upload_file_view, name='upload_view_url'),
    path('product/', upload_product_file_view, name='upload_view_product_url'),
    path('good_demand/', upload_demand_view, name='upload_good_demand_url')
]