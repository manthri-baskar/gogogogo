from django.urls import path
from .views import demand_prediction

app_name = 'demand_predict'

urlpatterns = [ 
    path('', demand_prediction, name='demand_forcast_url'),
] 