from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from products.utils import get_image
from goods.models import *
from products.models import *
from .models import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Create your views here.
def raw_material_demand(comp_info, goods_data):
    good_data = {}
    for data in goods_data:
        good_data['%s'%data['item']] = [data['next_demand'], data['std']]
    all_raw    = Product.objects.all().filter(user=comp_info.user)
    all_goods  = Goods.objects.all().filter(user=comp_info.user)
    good_raw_data = {}
    raw_demand = {}
    for a_good in all_goods:
        a = {}
        all_Amount = Amount.objects.all().filter(user=comp_info.user, goods=a_good.id)
        for a_amount in all_Amount:
            a['%s'%a_amount.raw_mate] = a_amount.required_amount
        good_raw_data['%s'%a_good.good_name] = a
    for a_good in good_raw_data.keys():
        a  = good_raw_data[a_good]
        a1 = good_data['%s'%a_good]
        for b in a.keys():
            if b in raw_demand.keys():
                b1 = a[b]
                c  = raw_demand[b]
                c['mean'].append(a1[0]*b1)
                c['std'].append(a1[1]*b1)
                raw_demand[b] = c
            else:
                raw_demand['%s'%b] = {}
                b1 = a[b]
                c  = raw_demand[b]
                c['mean'] = []
                c['std']  = []
                c['mean'].append(a1[0]*b1)
                c['std'].append(a1[1]*b1)
                raw_demand[b] = c
    res_raw = []
    for a_raw in raw_demand.keys():
        a         = raw_demand[a_raw]
        a['raw']  = a_raw
        a['std']  = math.sqrt(sum([a['std'][i] * a['std'][i] for i in range(len(a['std']))]))
        a['mean'] = sum(a['mean'])
        res_raw.append(a)

    return res_raw

def winters_model_dict(info,pk1,d,y,p):
    alpha = info.level_sc
    beta  = info.trend_sc
    gaama = info.seasonal_factor_sc
    row                  = pk1.iloc[0]
    pk1.loc[len(pk1)]    = row
    pk1.loc[1,'year']    = int(y)
    pk1.loc[1,'period']  = int(p)
    pk1.loc[1,'demand']  = int(d)
    pk1.loc[1,'seasonal_factor'] = float(pk1.loc[0,'next_1'])
    pk1.loc[1,'level']   = alpha*(pk1.loc[1,'demand']/pk1.loc[1,'seasonal_factor']) + (1-alpha)*float((pk1.loc[0,'level'])+float(pk1.loc[0,'trend']))
    pk1.loc[1,'trend']   = beta*(pk1.loc[1,'level']-float(pk1.loc[0,'level'])) + (1-beta)*float(pk1.loc[0,'trend'])
    pk1.loc[1,'forcast'] = (pk1.loc[1,'level']+pk1.loc[1,'trend'])*pk1.loc[1,'seasonal_factor']
    pk1.loc[1,'error']   = pk1.loc[1,'forcast']-pk1.loc[1,'demand']
    pk1.loc[1,'n']       = float(pk1.loc[0,'n'])+1
    pk1.loc[1,'MSEt']    = (float(pk1.loc[0,'MSEt'])*float(pk1.loc[0,'n']) + pk1.loc[1,'error']*pk1.loc[1,'error'])/pk1.loc[1,'n']
    pk1.loc[1,'MADt']    = (float(pk1.loc[0,'MADt'])*float(pk1.loc[0,'n']) + abs(pk1.loc[1,'error']))/pk1.loc[1,'n']
    pk1.loc[1,'std']     = 1.25*pk1.loc[1,'MADt']
    pk1.loc[1,'MAPEt']   = (float(pk1.loc[0,'MAPEt'])*float(pk1.loc[0,'n']) + (pk1.loc[1,'error']/pk1.loc[1,'demand'])*100)/pk1.loc[1,'n']
    pk1.loc[1,'biast']   = float(pk1.loc[0,'biast']) + pk1.loc[1,'error']
    pk1.loc[1,'TSt']     = pk1.loc[1,'biast']/pk1.loc[1,'MADt']
    pk1.loc[1,'next_1']  = float(pk1.loc[0,'next_2'])
    pk1.loc[1,'next_2']  = float(pk1.loc[0,'next_3'])
    pk1.loc[1,'next_3']  = float(pk1.loc[0,'next_4'])
    pk1.loc[1,'next_4']  = float(pk1.loc[0,'next_5'])
    pk1.loc[1,'next_5']  = float(pk1.loc[0,'next_6'])
    pk1.loc[1,'next_6']  = gaama*(pk1.loc[1,'demand']/pk1.loc[1,'level']) + (1-gaama)*pk1.loc[1,'seasonal_factor']
    pk1        = pk1.drop(0)
    pk1_dict   = pk1.to_dict('records')[0]
    del_list   = past_data.objects.get(user=info.user, good_name=pk1_dict['item'])
    del_list.delete()
    print(str(pk1_dict))
    pk1_dict['next_demand']  = int((pk1_dict['level'] + pk1_dict['trend'])*pk1_dict['next_1'])

    return pk1_dict

def winters_model_shape(info,pk1,p):
    alpha = info.level_sc
    beta  = info.trend_sc
    gaama = info.seasonal_factor_sc
    row    = [0 for i in range(0, pk1.shape[1])]
    pk1.loc[len(pk1)] = row
    no_row = pk1.shape[0]
    for i in range(no_row-1):
        b, c = pk1.iloc[no_row-i-1-1].copy(), pk1.iloc[no_row-i-1].copy()
        pk1.iloc[no_row-i-1-1],pk1.iloc[no_row-i-1] = c,b
    for i in range(p):
        pk1.loc[len(pk1)] = row
    pk1.loc[0,'level'] = pk1.loc[1,'level']
    pk1.loc[0,'trend'] = pk1.loc[1,'trend']
    for i in range(1, pk1.shape[0]-p):
        pk1.loc[i,'level']   = alpha*(pk1.loc[i,'demand']/pk1.loc[i,'seasonal_factor']) + (1-alpha)*(pk1.loc[i-1,'level']+pk1.loc[i-1,'trend'])
        pk1.loc[i,'trend']   = beta*(pk1.loc[i,'level']-pk1.loc[i-1,'level']) + (1-beta)*pk1.loc[i-1,'trend']
        pk1.loc[i+p,'seasonal_factor'] = gaama*(pk1.loc[i,'demand']/pk1.loc[i,'level']) + (1-gaama)*pk1.loc[i,'seasonal_factor']
    pk1['forcast'] = (pk1['level'] + pk1['trend'])*pk1['seasonal_factor']
    pk1['error']   = pk1['forcast'] - pk1['demand']
    pk1['MSEt']    = [0 for i in range(0, pk1.shape[0])]
    pk1['MADt']    = [0 for i in range(0, pk1.shape[0])]
    pk1['MAPEt']   = [0 for i in range(0, pk1.shape[0])]
    pk1['biast']   = [0 for i in range(0, pk1.shape[0])]
    pk1['TSt']     = [0 for i in range(0, pk1.shape[0])]
    for i in range(1, pk1.shape[0]-p):
        f = 0; g = 0; h = 0; r = 0; s = 0
        for j in range(1,i+1):
            f = f + pk1.loc[j,'error']*pk1.loc[j,'error']
            g = g + abs(pk1.loc[j,'error'])
            h = h + abs(pk1.loc[j,'error']/pk1.loc[j,'demand'])*100
            r = r + pk1.loc[j,'error']
        pk1.loc[i,'MSEt']  = f/i
        pk1.loc[i,'MADt']  = g/i
        pk1.loc[i,'MAPEt'] = h/i
        pk1.loc[i,'biast'] = r/i
        pk1.loc[i,'TSt']   = pk1.loc[i,'biast']/pk1.loc[i,'MADt']
        
    return pk1

       
@login_required(login_url='login') 
def demand_prediction(request):
    try:
        comp_info     = company_details.objects.get(user=request.user)
        g_details     = pd.DataFrame(Goods.objects.all().values().filter(user=request.user))
        g_demand      = pd.DataFrame(goods_demand.objects.all().values().filter(user=request.user))
        all_goodnames = g_details.loc[:,'good_name']
        #all_goodnames = all_goodnames.T 
    except:
        all_goods     = None        
        forcast       = None
        error         = 'no data available'
        form          = None
        raw_demand    = None
        return render(request,'demand_predict/forcast.html',context={'all_goods':all_goods, 'form':form, 'forcast':forcast, 'error_message':error})
    forcast       = None
    error         = None
    form          = True
    raw_demand    = None
    all_goods     = []
    for A in all_goodnames.values:
        all_goods.append(A)
    all_past_data = past_data.objects.all().filter(user=request.user)

    if request.method == 'POST': 
        form    = False
        forcast = []
        confirm = request.POST.get('file')
        year    = request.POST.get('year')
        period  = request.POST.get('period')
        if all_past_data.count() == 0 or confirm == 'yes':
            data = {}
            for i in all_goods:
                data['%s' %i] = []
            p  = comp_info.periods #number of periods in a year
            p0 = int(12/p); error = None; df2 = None

            if g_details.shape[0]>0:
                g_demand.rename(columns={'id':'demand_id'}, inplace = True)
                g_demand['year']          = g_demand['date'].dt.strftime('%Y')
                g_demand['month']         = g_demand['date'].dt.strftime('%m')
                g_demand['month']         = g_demand['month'].astype(int) #converting str column into int
                g_demand['month_2']       = g_demand['month'] - 1
                g_demand['period']        = g_demand['month_2']//p0 + 1
                g_demand                  = g_demand.groupby(['year','period','item_name'], as_index=False).aggregate({'demand': 'sum'}) 
                all_goods                 = []
                g_demand[['user','item']] = g_demand.item_name.str.split(" => ",expand=True)  
                del [g_demand['user'], g_demand['item_name']]
                inter = g_demand.values #convert dataframe to array
                for B in inter.tolist(): #conert array to list
                    if B[3] in all_goods:
                        data['%s' %B[3]].append(B)
                    else:
                        all_goods.append(B[3])
                        data['%s' %B[3]].append(B)
                data0 = {}
                for C in all_goods:
                    table         = data['%s' %C]
                    table         = pd.DataFrame(table)
                    table.columns = ['year','period','demand','item']
                    table         = table[['year','period','item','demand']] #swaping the columns in dataframe
                    table1        = trend_seasonal(table, p)
                    table2        = winters_model_shape(comp_info,table1, p)

                    past_dict        = table2.to_dict('records')[table2.shape[0]-p-1]
                    past_dict['n']   = table2.shape[0]-p-1
                    past_dict['std'] = 1.25*past_dict['MADt'] 
                    past_dict_df     = pd.DataFrame([past_dict]) # converting dictionary to dataframe 
                    for j in range(1,p+1):
                        past_dict['next_%s' %j] = table2.loc[table2.shape[0]-p-1+j,'seasonal_factor']
                    
                    try:    
                        del_list = past_data.objects.get(user=request.user, good_name=C)
                        del_list.delete()                        
                        save_table  = past_data(user=request.user, good_name=C, demand_List = str(past_dict))
                        save_table.save()
                    except:
                        save_table  = past_data(user=request.user, good_name=C, demand_List = str(past_dict))
                        save_table.save()
                    past_dict['next_demand']  = int((past_dict['level'] + past_dict['trend'])*past_dict['next_1'])
                    forcast.append(past_dict)
                raw_demand = raw_material_demand(comp_info, forcast)

            return render(request,'demand_predict/forcast.html',context={'raw_demand':raw_demand, 'all_goods':all_goods, 'form':form, 'forcast':forcast, 'error_message':error})
        
        else:
            form    = False
            forcast = []
            for a_good in all_goods:
                data       = past_data.objects.get(user=request.user, good_name=a_good)
                Dict       = eval(data.demand_List) # converting string into dictionary
                df         = pd.DataFrame([Dict])
                d          = request.POST.get(a_good)
                user       = request.user
                table      = winters_model_dict(comp_info, df, d, year, period)
                save_table = past_data(user=request.user, good_name=pk1_dict['item'], demand_List = str(table))
                save_table.save()
                forcast.append(table)
            raw_demand = raw_material_demand(comp_info, forcast)
            return render(request,'demand_predict/forcast.html',context={'raw_demand':raw_demand, 'all_goods':all_goods, 'form':form, 'forcast':forcast, 'error_message':error})

    return render(request,'demand_predict/forcast.html',context={'raw_demand':raw_demand, 'all_goods':all_goods, 'form':form, 'forcast':forcast, 'error_message':error})

 
def sim_linear_reg(x,y):
    x     = np.array(x)
    y     = np.array(y)
    n     = np.size(x)    # number of observations/points
    m_x   = np.mean(x)  # mean of x and y vector
    m_y   = np.mean(y)
    SS_xy = np.sum(y*x) - n*m_y*m_x # calculating cross-deviation and deviation about x
    SS_xx = np.sum(x*x) - n*m_x*m_x
    b     = SS_xy / SS_xx # calculating regression coefficients
    a     = m_y - b*m_x

    return [a,b]

def trend_seasonal(pk,p):
    list1 = []; x = []; y = []
    num_rows = pk.count()[0]
    if p%2 == 0:
        for i in range(1,num_rows+1):
            if i<int((p/2)+1) or i>int(num_rows-(p/2)):
                list1.append(0)
            else:
                a  = pk.loc[i-(p/2)-1,"demand"] + pk.loc[i+(p/2)-1,"demand"]
                a1 = range(int(i+1-(p/2)-1), int(i-1+(p/2)))
                for D in a1:
                    a = a + 2*pk.loc[D,"demand"]
                a = a/(2*p)
                x.append(i); y.append(a); list1.append(a)
    else:
        for i in range(1,num_rows+1):
            if i<=int((p-1)/2) or i>int(num_rows-((p-1)/2)):
                list1.append(0)
            else:
                a  = 0
                a1 = range(int(i-((p-1)/2)-1), int(i+((p-1)/2)))
                for D in a1:
                    a = a + pk.loc[D,"demand"]
                a = a/p
                x.append(i); y.append(a); list1.append(a)

    pk['deseasonalised'] = list1
    reg = sim_linear_reg(x,y)
    L = []; T = []; V = []
    for i in range(1,num_rows+1):
        L.append(reg[0]); T.append(i*reg[1]); V.append(reg[0]+i*reg[1])
    pk['level'] = L;  pk['trend'] = T;  pk['deseason'] = V
    del pk['deseasonalised']
    pk['season_factor']   = pk['demand']/pk['deseason']
    pk['seasonal_factor'] = pk['season_factor']
    no_col = len(pk['season_factor'])
    for i in range(1,p+1):
        k = 0
        for j in range(int(no_col/p)):
            k = k + pk.loc[i+j*p-1,"seasonal_factor"]
        k = k/(no_col/p)
        for m in range(int(no_col/p)):
            pk.loc[i+m*p-1,"seasonal_factor"] = k
    del [pk['season_factor'], pk['deseason']]
    
    return pk