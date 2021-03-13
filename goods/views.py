from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .forms import *
 
# Create your views here.

@login_required(login_url='login')
def goods_form_view(request):
    form = GoodsForm()
    if request.method == 'POST':
        form=GoodsForm(request.POST) 
        if form.is_valid():
            a = form.cleaned_data["good_name"]
            b = form.cleaned_data["setup_cost"]
            c = form.cleaned_data["production_cost"]
            d = form.cleaned_data["holding_cost"]
            e = form.cleaned_data["production_rate"]
            f = form.cleaned_data["production_quantity"]
            g = form.cleaned_data["raw_material"]
            h = form.cleaned_data["total_demand"]

            for i in request.user.good.all():
                if i.good_name==a:
                    messages.error(request, a +' good Already Created')
                    return redirect('goods:goods_form_url')

            t = Goods(good_name=a, setup_cost=b, production_cost=c, holding_cost=d, production_rate=e, production_quantity=f, total_demand=h)
            t.save()
            for i in g:
                z = Product.objects.get(name=i)
                print('////=============', z.id)
                #t.raw_material.add(z.id, through_defaults={'date_joined': required_amount})

            request.user.good.add(t)
            
            return redirect('goods:goods_form_url')
                    
    return render(request,'goods/add_goods.html',context={'form': form})

@login_required(login_url='login')
def amount_form_view(request):
    form = AmountForm()
    if request.method == 'POST':
        form=GoodsForm(request.POST) 
        if form.is_valid():
            a = form.cleaned_data["goods"]
            b = form.cleaned_data["raw_material"]
            c = form.cleaned_data["required_amount"]
            
            t = Goods(goods=a, raw_material=b, required_amount=c)
            t.save()
            
            return redirect('goods/add_amount.html')
                    
    return render(request,'goods/add_amount.html',context={'form': form})

