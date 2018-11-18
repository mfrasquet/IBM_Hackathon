from django.shortcuts import render

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import io
import base64
import json
import web3
from web3 import Web3, IPCProvider


from datetime import datetime

import urllib.request

from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.middleware import geth_poa_middleware

w3 = Web3(IPCProvider('/home/miguel/rinkeby/geth.ipc'))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

admin=w3.eth.accounts[1]
otro=w3.eth.accounts[0]
otro2=w3.eth.accounts[2]

def bytes2hex(bytes):
    return '0x'+''.join('{:x}'.format(b) for b in bytes)


# Create your views here.

def portada(request):
    return render(request, 'dash/portada.html', {})


def index(request):

    #w3 = Web3(HTTPProvider('http://localhost:8545'))



    w3.personal.unlockAccount(admin, 'lagruesa',4000)

    word = 'Hola Juan'
    word_bytes = word.encode('utf-8')
    messg=bytes2hex(word.encode('utf-8'))


    #print(w3.eth.getBalance(admin))
    #w3.eth.sendTransaction({'to':otro, 'from':admin, 'value': 12345, 'data':messg})
    #print(w3.eth.getBalance(admin))

    """
    This is an example script from the Matplotlib website, just to show 
    a working sample >>>
    """
    

    return render(request, 'dash/index.html', {'address':admin,'address2':otro,'address3':otro2,})


def dispo(request):

    temperature=[]
    HR=[]
    ac=[]
    unix=[]
   

    with urllib.request.urlopen('https://cosasdejuan.000webhostapp.com/threeroom/api.php') as response:
        html = response.read()
#
    sensor=eval(html.decode("utf-8"))
    temperature.append(sensor["temp"])
    HR.append(sensor["hum"])
    ac.append(sensor["accel"])
    unix.append(sensor["unix"])



    HR_lim_max=70
    HR_lim_min=40

    temp_lim_max=30
    temp_lim_min=5

    ac_lim_max=2
    ac_lim_min=.5

    incumplimiento=0
    if max(temperature[0])>temp_lim_max:
        incumplimiento=1
        incum=temperature[0].index(max(temperature[0]))
    if min(temperature[0])<temp_lim_min:
        incumplimiento=1
        incum=temperature[0].index(min(temperature[0]))
    if max(HR[0])>HR_lim_max:
        incumplimiento=1
        incum=HR[0].index(max(HR[0]))
    if min(HR[0])<HR_lim_min:
        incumplimiento=1
        incum=HR[0].index(min(HR[0]))
    if max(ac[0])>ac_lim_max:
        incumplimiento=1
        incum=ac[0].index(max(ac[0]))
    if min(ac[0])<ac_lim_min:
        incumplimiento=1
        incum=ac[0].index(min(ac[0]))
    
    incum=temperature[0].index(max(temperature[0]))


    """
    This is an example script from the Matplotlib website, just to show 
    a working sample >>>
    """
    fig = plt.figure()
    x=list(range(0,len(HR[0])))

    fig.suptitle('Temperatura y Humedad', fontsize=14, fontweight='bold')
    ax1 = fig.add_subplot(111)  
    ax1 .plot(x, temperature[0],'.r--',label="Temperatura")
    
    #ax1 .plot(x, [-2,-2,-2],'.m-',label="Temperatura MIN")
    #ax1 .plot(step_sim, Q_prod_lim,'.b-',label="Produccion util")
    #ax1 .plot(step_sim, Q_prod_rec,'.g-',label="Produccion Rec")
    ax1 .axhline(y=temp_lim_max,xmin=0,xmax=100,c="red",linewidth=2,zorder=0)
    ax1 .axhline(y=temp_lim_min,xmin=0,xmax=100,c="red",linewidth=2,zorder=0)
    ax1.set_xlabel('simulación (últimos 15 min)')
    ax1.set_ylabel('Temperatura ºC',color="r")
    ax1.set_ylim([-5,35])
    plt.legend(loc='upper left', borderaxespad=0.)
    ax2 = ax1.twinx()  
    ax2 .plot(x, HR[0],'.b--',label="Humedad")
    ax2 .axhline(y=HR_lim_max,xmin=0,xmax=100,c="blue",linewidth=2,zorder=0)
    ax2 .axhline(y=HR_lim_min,xmin=0,xmax=100,c="blue",linewidth=2,zorder=0)
    ax2.set_ylabel('HR %',color="b")
    ax2.set_ylim([30,80]) 
    plt.legend(loc='upper right', borderaxespad=0.)      
    #ax2 .plot(step_sim, DNI,'.-',color = 'red',label="DNI")
    #ax2.set_ylabel('Radiación solar - W/m2',color='red')

    """
    Now the redirect into the cStringIO or BytesIO object >>>
    """
    f = io.BytesIO()           # Python 3
    plt.savefig(f, format="png", facecolor=(0.95,0.95,0.95))
    plt.clf()
    image_base64 = base64.b64encode(f.getvalue()).decode('utf-8').replace('\n', '')
    f.close()
    """
    Add the contents of the StringIO or BytesIO object to the response, matching the
    mime type with the plot format (in this case, PNG) and return >>>
    """


    fig = plt.figure()

    fig.suptitle('Aceleración', fontsize=14, fontweight='bold')
    ax1 = fig.add_subplot(111)  
    #ax1 .plot(x, [35,35,35],'.k-',label="Temperatura MAX")
    #ax1 .plot(x, [-2,-2,-2],'.m-',label="Temperatura MIN")
    #ax1 .plot(step_sim, Q_prod_lim,'.b-',label="Produccion util")
    #ax1 .plot(step_sim, Q_prod_rec,'.g-',label="Produccion Rec")
    ax1 .plot(x, ac[0],'.r--',label="Aceleración")
    ax1 .axhline(y=ac_lim_max,xmin=0,xmax=100,c="red",linewidth=2,zorder=0)
    ax1 .axhline(y=ac_lim_min,xmin=0,xmax=100,c="red",linewidth=2,zorder=0)
    ax1.set_xlabel('simulación (últimos 15 min)')
    ax1.set_ylabel('Aceleración g',color="r")
    ax1.set_ylim([0,3])
    plt.legend(loc='upper left', borderaxespad=0.)
  
    plt.legend(loc='upper right', borderaxespad=0.)
    """
    Now the redirect into the cStringIO or BytesIO object >>>
    """
    f = io.BytesIO()           # Python 3
    plt.savefig(f, format="png", facecolor=(0.95,0.95,0.95))
    plt.clf()
    image_base64_2 = base64.b64encode(f.getvalue()).decode('utf-8').replace('\n', '')
    f.close()
    """
    Add the contents of the StringIO or BytesIO object to the response, matching the
    mime type with the plot format (in this case, PNG) and return >>>
    """
    
    url_txt=""
    date_for_plot=""
    if incumplimiento==1:
        date_for_plot=(datetime.utcfromtimestamp(unix[0][incum]).strftime('%Y-%m-%d %H:%M:%S'))
        datetime.utcfromtimestamp(unix[0][1]).strftime('%Y-%m-%d %H:%M:%S')
        w3.personal.unlockAccount(admin, 'lagruesa',4000)

        word = 'incumplimiento en' +str(date_for_plot)
        word_bytes = word.encode('utf-8')
        messg=bytes2hex(word.encode('utf-8'))

        aa=w3.eth.sendTransaction({'to':otro, 'from':admin, 'value': 12345, 'data':messg})
        bb=w3.toBytes(aa)
        tx=w3.toHex(bb)
        url_txt='https://rinkeby.etherscan.io/tx/'+str(tx)
  


    return render(request, 'dash/dispo.html', {'date_for_plot':date_for_plot,'url_txt':url_txt,'incumplimiento':incumplimiento,'image_base64':image_base64,'image_base64_2':image_base64_2,})
