from django.urls import path
from .views import *

app_name = 'demand_predict'

urlpatterns = [ 
    path('chart/', chart_select_view, name='error_chart_view'),
    path('', demand_prediction, name='demand_forcast_url'),
]  