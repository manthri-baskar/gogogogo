from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .forms import *
from .models import *
import math
import scipy.stats as st
import datetime

@login_required(login_url='login')
def goods_form_view(request):
    form  = GoodsForm(request.user)
    items = Product.objects.all().filter(user=request.user)
    len   = Product.objects.all().filter(user=request.user).count()
    forma = AmountForm()
    if request.method == 'POST':
        form=GoodsForm(request.user, request.POST) 
        forma=AmountForm(request.POST) 
        if form.is_valid() :
            a = form.cleaned_data["good_name"]
            b = form.cleaned_data["setup_cost"]
            c = form.cleaned_data["production_cost"]
            d = form.cleaned_data["holding_cost"]
            e = form.cleaned_data["production_rate"]
            f = form.cleaned_data["production_quantity"]
            h = form.cleaned_data["total_demand"]
                
            for i in request.user.good.all():
                if i.good_name==a:
                    messages.error(request, a +' good Already Created')
                    return redirect('goods:goods_form_url')

            t = Goods(good_name=a, setup_cost=b, production_cost=c, holding_cost=d, production_rate=e, production_quantity=f, total_demand=h)
            t.save() 
            for y in range(len):
                x   = 'raw_material'+str(y)
                ram = 'required_amount'+str(y)
                if request.POST.get(x) and request.POST.get(ram) :
                    g = request.POST.get(x)
                    k = request.POST.get(ram)
                    z = Product.objects.get(name=g,user=request.user)
                    t.raw_material.add(z.id, through_defaults={'required_amount': k , 'user' : request.user})

            request.user.good.add(t)
            return redirect('goods:goods_form_url')
                    
        
    return render(request,'goods/add_goods.html',context={'form1': GoodsForm(request.user),'form2':AmountForm(),'items' : items , 'length':len})

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
        try:  
            dele_good  = Goods.objects.get(good_name=del_good, user=request.user)
        except:
              dele_good =  None
        try:
            dele_raw   = Product.objects.get(name=del_raw, user=request.user)
        except:
            dele_raw   =  None
        
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


@login_required(login_url='login')
def add_rawTo_good(request,pk):    
    all_goods = Goods.objects.all().filter(user=request.user)
    par_good    = Goods.objects.get(id=pk)
    goodname=par_good.good_name
    
    if request.method == 'POST': 
        goodname         = par_good.good_name
        name             = request.POST.get('name')
        lead_time        = request.POST.get('lead_time')
        std              = request.POST.get('std')
        carry            = request.POST.get('carry_cost')
        order            = request.POST.get('order_cost')
        unit_cost        = request.POST.get('unit_cost')
        demand           = request.POST.get('avg_daily_demand')
        total_inventory  = request.POST.get('total_inventory')

        a = 2*300*float(demand)*float(order)
        b = float(unit_cost)*float(carry)/100
        eoq  = math.sqrt(a/b)
        z    = (st.norm.ppf(90/100))
        rq   = float(lead_time)*float(demand)+float(z)*float(std)*float(lead_time)
       
        good  = Goods.objects.get(good_name=goodname, user=request.user)
        raw_to_good = good.raw_material.create(user=request.user, date=datetime.date.today(), 
        name=name, lead_time=lead_time, standard_deviation=std, service_level=90, 
        no_of_workingdays=300, carrying_cost= carry, ordering_cost=order, 
        unit_costprice=unit_cost, average_daily_demand=demand, total_inventory=total_inventory, 
        eoq=eoq, rq=rq, z=z,  through_defaults={'user':request.user,'required_amount': 0})
        
        return redirect('goods:amount_form_url')

    context = {
        'all_goods' : all_goods,      
        'goodname' : goodname,      
    }

    return render(request,'goods/rawTo_good.html', context)

@login_required(login_url='login')
def update_items(request,pk):
    par_good    = Goods.objects.get(id=pk)
    all_raw     = Product.objects.all().filter(user=request.user)
    all_amount  = Amount.objects.all().filter(user=request.user, goods=par_good)    
    length      = par_good.raw_material.all().filter(user=request.user).count()
    prod_length = Product.objects.all().filter(user=request.user).count()
    form        = GoodsForm(instance=par_good)
    n           = par_good.good_name
    rawmate     = par_good.raw_material.all()

    
    length = length+1
    if request.method=='POST':

            for y in range(prod_length):
                x   = 'raw_material'+str(y)
                ram = 'required_amount'+str(y)
                if request.POST.get(x) and request.POST.get(ram) :
                    g = request.POST.get(x)
                    k = request.POST.get(ram)
                    z = Product.objects.get(name=g,user=request.user)
                    par_good.raw_material.add(z.id, through_defaults={'required_amount': k , 'user' : request.user})




            #messages.info(request, n + '  Updated to ' + par_good.good_name)
            return redirect('goods:amount_form_url')
    
    context={
        'form'     :form,
        'rawmate'  :rawmate,
        'items'    :all_raw,
        'a_good' :par_good,
        'all_amount' :all_amount,
        'length'   :length
    }
    return render(request,'goods/update_item.html',context)