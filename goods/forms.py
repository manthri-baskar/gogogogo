from django import forms
from django.forms import CheckboxSelectMultiple
from .models import *

class GoodsForm(forms.ModelForm):
    class Meta:
        model  = Goods
        exclude = ('user','raw_material',)

    def clean_name(self):
        name = self.cleaned_data.get('good_name').upper()
        return name

    def __init__(self,user=None,*args,**kwargs):
        super(GoodsForm,self).__init__(*args,**kwargs)
        if user:
            user=user

class AmountForm(forms.ModelForm):
    class Meta:
        model=Amount
        exclude =('goods','raw_mate',)