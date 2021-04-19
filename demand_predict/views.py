from django.shortcuts import render
from goods.models import *
from django.contrib.auth.decorators import login_required
from products.utils import get_image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create your views here. 
 
def sim_linear_reg(x,y):
    x = np.array(x)
    y = np.array(y)
    # number of observations/points
    n = np.size(x)
     # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)
     # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x
     # calculating regression coefficients
    b = SS_xy / SS_xx
    a = m_y - b*m_x
    return [a,b]

def trend_seasonal(pk,p):
    list1 = []
    x = []
    y = []
    num_rows = pk.count()[0]
    if p%2 == 0:
        for i in range(1,num_rows+1):
            if i<int((p/2)+1) or i>int(num_rows-(p/2)):
                list1.append(0)
            else:
                a = pk.loc[i-(p/2)-1,"demand"] + pk.loc[i+(p/2)-1,"demand"]
                a1 = range(int(i+1-(p/2)-1), int(i-1+(p/2)))
                for D in a1:
                    a = a + 2*pk.loc[D,"demand"]
                a = a/(2*p)
                x.append(i)
                y.append(a)
                list1.append(a)
    else:
        for i in range(1,num_rows+1):
            if i<=int((p-1)/2) or i>int(num_rows-((p-1)/2)):
                list1.append(0)
            else:
                a = 0
                a1 = range(int(i-((p-1)/2)-1), int(i+((p-1)/2)))
                for D in a1:
                    a = a + pk.loc[D,"demand"]
                a = a/p
                x.append(i)
                y.append(a)
                list1.append(a)

    pk['deseasonalised'] = list1
    reg = sim_linear_reg(x,y)
    L = []
    T = []
    V = []
    for i in range(1,num_rows+1):
        L.append(reg[0])
        T.append(i*reg[1])
        V.append(reg[0]+i*reg[1])
    pk['level'] = L
    pk['trend'] = T
    pk['deseason'] = V
    del pk['deseasonalised']
    pk['season_factor'] = pk['demand']/pk['deseason']
    pk['seasonal_factor'] = pk['season_factor']
    no_col = len(pk['season_factor'])
    for i in range(1,p+1):
        k = 0
        for j in range(int(no_col/p)):
            k = k + pk.loc[i+j*p-1,"seasonal_factor"]
        k = k/(no_col/p)
        for m in range(int(no_col/p)):
            pk.loc[i+m*p-1,"seasonal_factor"] = k
    del pk['season_factor']
    del pk['deseason']
    
    return pk

def winters_model_shape(pk1,p):
    alpha = 0.05
    beta  = 0.1
    gaama = 0.1
    row = [0 for i in range(0, pk1.shape[1])]
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


def winters_model(pk2, p):
    x = 2
    
       
@login_required(login_url='login') 
def demand_prediction(request):
    g_details = pd.DataFrame(Goods.objects.all().values().filter(user=request.user))
    all_goodnames = g_details.loc[:, ['good_name']]
    all_goodnames = all_goodnames.T 
    all_goods = []
    for A in all_goodnames.values:
        for i in A:
            all_goods.append(i)
    data = {}
    for i in all_goods:
        data['%s' %i] = []
    g_demand  = pd.DataFrame(goods_demand.objects.all().values().filter(user=request.user))
    p         = 6 #number of periods in a year
    p0        = int(12/p)
    error     = None
    df2       = None

    if g_details.shape[0]>0:
        g_demand.rename(columns = {'id':'demand_id'}, inplace = True)
        g_demand['year']        = g_demand['date'].dt.strftime('%Y')
        g_demand['month']       = g_demand['date'].dt.strftime('%m')
        g_demand['month']       = g_demand['month'].astype(int) #converting str column into int
        g_demand['month_2']     = g_demand['month'] - 1
        g_demand['period']      = g_demand['month_2']//p0 + 1
        g_demand = g_demand.groupby(['year','period','item_name'], as_index=False).aggregate({'demand': 'sum'}) 
        all_goods = []
        g_demand[['user','item']] = g_demand.item_name.str.split(" => ",expand=True)  
        del g_demand['user']
        del g_demand['item_name']
        inter = g_demand.values #convert dataframe to array
        for B in inter.tolist(): #conert array to list
            if B[3] in all_goods:
                data['%s' %B[3]].append(B)
            else:
                all_goods.append(B[3])
                data['%s' %B[3]].append(B)
        data0 = {}
        for C in all_goods:
            table = data['%s' %C]
            table = pd.DataFrame(table)
            table.columns = ['year','period','demand','item']
            table = table[['year','period','item','demand']] #swaping the columns in dataframe
            print(table)
            table1 = trend_seasonal(table, p)
            table2 = winters_model_shape(table1, p)
            data0['%s' %C] = []
            for j in range(1,p+1):
                y = round((table2.loc[table2.shape[0]-p-1,'level'] + table2.loc[table2.shape[0]-p-1,'trend']*j)*table2.loc[table2.shape[0]-p-1+j,'seasonal_factor'])
                data0['%s' %C].append(y)

        col = ['period '+str(i) for i in range(1,p+1)]
        df = pd.DataFrame(data0, columns = ['Name', 'Age'])
        data0 = pd.DataFrame.from_dict(data0)
        df     = pd.DataFrame(data0.values, columns=all_goods, index=col)
        table3 = winters_model(table2, p)
    return render(request,'demand_predict/forcast.html',context={'all_goods':all_goods, 'forcast':df.to_html(classes=('table table-striped')), 'error':error})

@login_required(login_url='login')
def customer_corr_view(request):
    df = pd.DataFrame(Customer.objects.all().values())
    corr = round(df['budget'].corr(df['employment']),2)
    
    plt.switch_backend('Agg')
    sns.jointplot(x='budget', y='employment', kind='reg', data=df).set_axis_labels('Company budget', 'No. of employees')
    graph = get_image()

    context = { 
        'graph':graph,
        'corr':corr,
    }

    return render(request, 'customers/main.html', context)