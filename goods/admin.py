from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Goods)
admin.site.register(Amount)
admin.site.register(goods_demand)
admin.site.register(company_details)

 