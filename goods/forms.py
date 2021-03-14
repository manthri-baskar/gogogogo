from django import forms
from django.forms import CheckboxSelectMultiple
from .models import *

class GoodsForm(forms.ModelForm):
    class Meta:
        model  = Goods
        exclude = ('user',)

        widgets = {
            'raw_material': CheckboxSelectMultiple(),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('good_name').upper()
        return name