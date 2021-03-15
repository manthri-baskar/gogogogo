from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
#from products.models import Product
from .forms import *
from .models import *
# Create your views here.

@login_required(login_url='login')
def goods_form_view(request):
    form = GoodsForm(request.user)
    if request.method == 'POST':
        form=GoodsForm(request.user, request.POST) 
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
            for raw in g:
                z = Product.objects.get(name=raw.name, user=request.user)
                t.raw_material.add(z.id, through_defaults={'user':request.user,'required_amount': 0})

            request.user.good.add(t)
            
            return redirect('goods:goods_form_url')
                    
    return render(request,'goods/add_goods.html',context={'form': GoodsForm(request.user)})

@login_required(login_url='login')
def amount_form_view(request):
    all_goods  = Goods.objects.all().filter(user=request.user)
    all_Amount = Amount.objects.all().filter(user=request.user)
    if request.method == "POST":
        for a_good in all_goods:
            for a_raw in a_good.raw_material.all():
                x = str(a_good.good_name)+' -> '+str(a_raw)
                req_amount = request.POST.get(x)
                a_good.raw_material.remove(a_raw)
                t = Amount(user=request.user, goods=a_good, raw_mate=a_raw, required_amount= req_amount)
                t.save()

    return render(request,'goods/add_amount.html', context={'all_goods':all_goods, 'all_Amount':all_Amount})

 
@login_required(login_url='login')
def delete_goods(request):
    all_goods = Goods.objects.all().filter(user=request.user)
    all_raw   = Product.objects.all().filter(user=request.user)

    if request.method == 'POST':
        action   = request.POST.get('action')
        del_good = request.POST.get('good')
        del_raw  = request.POST.get('raw_mat')
            
        dele_good  = Goods.objects.get(good_name=del_good, user=request.user)
        dele_raw   = Product.objects.get(name=del_raw, user=request.user)
        #dele_raw   = dele_raw.id
        
        if action == 'good_name':
            dele_good.delete()
        if action == 'raw_material':
            dele_raw.delete()
        if action == 'good_raw':
            dele_good.raw_material.remove(dele_raw)

    context = {
        'all_goods' : all_goods,
        'all_raw'   : all_raw
    }
    
    return render(request,'goods/delete_goods.html', context)