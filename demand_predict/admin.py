from django.contrib import admin
from .models import past_data, past_csv_data, places

# Register your models here.

admin.site.register(past_data)
admin.site.register(past_csv_data)
admin.site.register(places)
  