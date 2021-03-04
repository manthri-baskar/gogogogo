from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.aggregates import Avg, StdDev,Sum,Variance
from django.db.models.expressions import F
from django.views.generic import TemplateView, View 
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse
from .models import Product, Purchase
from .utils import get_simple_plot, get_salesman_from_id, get_image
from numpy.core.fromnumeric import product
from .forms import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Create your views here.

@login_required(login_url='login')
def sales_dist_view(request):
    df = pd.DataFrame(Purchase.objects.all().values())
    print(df)
    df['user_id']=df['user_id'].apply(get_salesman_from_id)
    df.rename({'user_id':'user'}, axis=1, inplace=True)
    df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    
    plt.switch_backend('Agg')
    plt.xticks(rotation=90)
    sns.barplot(x='date', y='total_price', hue='user', data=df)
    plt.tight_layout
    graph = get_image()

    #return HttpResponse("Hello Salesman")
    return render(request, 'products/sales.html', {'graph':graph})

@login_required(login_url='login')
def chart_select_view(request):
    error_message = None
    df = None
    graph = None
    price = None

    product_df = pd.DataFrame(Product.objects.all().values())
    purchase_df = pd.DataFrame(Purchase.objects.all().values())
    if product_df.shape[0]>0 :
        product_df['product_id'] = product_df['id']
    
    if purchase_df.shape[0]>0 :
        df = pd.merge(purchase_df, product_df, on='product_id').drop(['id_y', 'date_y'], axis=1).rename({'id_x':'id', 'date_x':'date'}, axis=1)
        price = df['price']
        if request.method == 'POST':
            chart_type = request.POST.get('sales')
            date_from  = request.POST.get('date_from') 
            date_to    = request.POST.get('date_to')

            df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
            df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')

            if chart_type!="":
                if date_from!="" and date_to!="":
                    df = df[(df['date']>date_from)&(df['date']<date_to)]
                    df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')
                # function to get a graph
                graph = get_simple_plot(chart_type, x=df2['date'], y=df2['total_price'] ,data=df)
            else:
                error_message = 'please select a chart to continue'

    else:
        error_message = 'no records in database'
        
    context ={
        'error_message': error_message,
        'graph' : graph,
        'price' : price,
        #'products' : product_df.to_html(),
        #'purchase' : purchase_df.to_html(),
        #'df'       : df,
    }
    return render(request, 'products/main.html', context)

@login_required(login_url='login')
def add_purchase_view(request):
        form=PurchaseForm(request.user)
        if request.method == 'POST':
            form=PurchaseForm(request.user,request.POST) 
            if form.is_valid():
                n = form.cleaned_data["product"]
                l = form.cleaned_data["quantity"]
                c = form.cleaned_data["price"]
                o = form.cleaned_data["recieve_quantity"]
                d = form.cleaned_data["date"]

                reporter = request.user.products.get(name=n)
                reporter.total_inventory = F('total_inventory')-l+o
                reporter.save()
                t = Purchase(product=n,quantity=l,price=c,recieve_quantity=o,date=d)
                t.save()
                request.user.purchases.add(t)

                return redirect('products:add-purchase-view')
                    
        return render(request,'products/add.html',context={'form':PurchaseForm(request.user) })

@login_required(login_url='login')
def items_list(request):
    ite   = None
    total = None

    try:
        ite = request.user.items.all()
        #ite = Product.objects.all()
    except ObjectDoesNotExist:
        messages.info(request,"There are no items.....")
    form = ItemSearchForm(request.POST or None)

    if request.method == 'POST':
            try:
                ite = request.user.items.filter(name__icontains=form['name'].value())
            except ObjectDoesNotExist:
                messages.info(request,"There are no items.....")
    
    context = {
        "form": form,
        "items":ite,
        "total":total
    }
    return render(request,'products/items_list.html',context)

@login_required(login_url='login')
def demand_list(request,*args,**kwargs):
    itee=None
    
    try:
        itee=request.user.demand.all()
    except ObjectDoesNotExist:
        messages.info(request,"No purchases has been recorded.....")

    return render(request,'products/demand_list.html',context={'demand':itee})

@login_required(login_url='login')
def DemandCreate(request):
        form = PurchaseForm(request.user)

        if request.method == 'POST':
            form = PurchaseForm(request.user,request.POST) 
            if form.is_valid():
                n = form.cleaned_data["product"]
                l = form.cleaned_data["quantity"]
                c = form.cleaned_data["price"]
                o = form.cleaned_data["recieved"]
                d = form.cleaned_data["date"]

                reporter = request.user.items.get(name=n)
                reporter.total_inventory = F('total_inventory')-l+o
                reporter.save()
                t = Purchase(product=n,quantity=l,price=c,recieved=o,date=d)
                t.save()
                request.user.demand.add(t)

                return redirect('product:demand_create_url')
                    
        return render(request,'products/demand_create.html',context={'form':PurchaseForm(request.user) })

@login_required(login_url='login')
def ItemCreate(request):
        form = ItemsForm()
        if request.method == 'POST':
            form=ItemsForm(request.POST) 
            if form.is_valid():
                n = form.cleaned_data["name"]
                l = form.cleaned_data["lead_time"]
                c = form.cleaned_data["carrying_cost"]
                o = form.cleaned_data["ordering_cost"]
                t = form.cleaned_data["total_inventory"]
                u = form.cleaned_data["unit_costprice"]
                s = form.cleaned_data["service_level"]
                w = form.cleaned_data["no_of_workingdays"]
                d = form.cleaned_data["standard_deviation"]
                a = form.cleaned_data["average_daily_demand"]

                for i in request.user.items.all():
                    if i.name==n:
                        messages.error(request, n +' Item Already Created')
                        return redirect('products:item_create_url')
              
                t = Product(name=n,lead_time=l,average_daily_demand=a,carrying_cost=c,ordering_cost=o,total_inventory=t,unit_costprice=u,service_level=s,no_of_workingdays=w,standard_deviation=d)
                t.save()
                request.user.items.add(t) 
                messages.success(request, n +' Item Created')
                return redirect('products:items_list_url')
                    
        return render(request,'products/item_create.html',context={'form':form, 'product_message':None })

@login_required(login_url='login')
def delete_items(request,pk):
    query_set = Product.objects.get(id=pk)
    
    if request.method =='POST':
        query_set.delete()
        messages.success(request,query_set.name + ' Removed')
        return redirect('products:items_list_url')
    
    context={
        'item':query_set.name
        }
    return render(request,'products/delete_items.html',context)

@login_required(login_url='login')
def update_items(request,pk):
    query_set = Product.objects.get(id=pk)
    form      = ItemsForm(instance=query_set)
    n         = query_set.name
    
    if request.method=='POST':
        form = ItemsForm(request.POST,instance=query_set)
        if form.is_valid():
            form.save()
            messages.info(request, n + '  Updated to ' + query_set.name)
            return redirect('products:items_list_url')
    
    context={
        'form':form
    }
    return render(request,'products/update_item.html',context)

@login_required(login_url='login')
def calculations(request):
    item_df   = pd.DataFrame(Product.objects.all().values().filter(user=request.user))
    demand_df = pd.DataFrame(Purchase.objects.all().values().filter(user=request.user))
    
    if demand_df.shape[0]>0:
        item_df['item_id'] = item_df['id']
        df = pd.merge(item_df,demand_df,on='item_id').drop(['id_y','id_x','carrying_cost','ordering_cost','unit_costprice','lead_time','service_level','standard_deviation','average_daily_demand','total_inventory','eoq','no_of_workingdays','rq','z','user_id_y','price','recieve_quantity'],axis=1).rename({'item_id':'id'},axis=1)
        del df['user_id_x']
        del df['id']
        df.rename(columns = {'date':'End of the Month'}, inplace = True)
        df.rename(columns = {'name':'Item Name'}, inplace = True)
        df['End of the Month'] = pd.to_datetime(df['End of the Month'])
        df = df.groupby([pd.Grouper(key='End of the Month', freq='1M'),'Item Name']).aggregate({'quantity':['mean','std','count','sum']}) # groupby each 1 month
        df.rename(columns = {'quantity':'Demand'}, inplace = True) 
        df.rename(columns = {'mean':'Daily Average'}, inplace = True) 
        df.rename(columns = {'std':'Standard deviation'}, inplace = True) 
        df.rename(columns = {'count':'Frequency'}, inplace = True) 
        df.rename(columns = {'sum':'Total Demand'}, inplace = True) 
        df=df.to_html(classes=('table table-striped'))
        return render(request,'products/calculations.html',context={'df2':df})

    else:
        error='<h3>No Data to Analyze</h3>'
        return render(request,'products/calculations.html',context={'df2':error})