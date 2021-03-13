from django import forms
from django.forms import CheckboxSelectMultiple
from .models import *

class GoodsForm(forms.ModelForm):
    class Meta:
        model  = Goods
        fields = '__all__'

        widgets = {
            'raw_material': CheckboxSelectMultiple(),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('good_name').upper()
        return name

class AmountForm(forms.ModelForm):
    class Meta:
        model  = Amount
        fields = '__all__'