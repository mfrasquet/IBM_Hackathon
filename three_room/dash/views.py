from django.shortcuts import render

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import io
import base64
import json
import web3
from web3 import Web3, IPCProvider

from .models import Contract


from datetime import datetime

import urllib.request

from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.middleware import geth_poa_middleware

#w3 = Web3(IPCProvider('/home/miguel/rinkeby/geth.ipc'))
w3 = Web3(HTTPProvider('https://rinkeby.infura.io/v3/4f76921d343748539da91921c5480804'))

#w3.middleware_stack.inject(geth_poa_middleware, layer=0)

#admin=w3.eth.accounts[1]
#otro=w3.eth.accounts[0]
#otro2=w3.eth.accounts[2]

def bytes2hex(bytes):
    return '0x'+''.join('{:x}'.format(b) for b in bytes)


# Create your views here.

def portada(request):
    return render(request, 'dash/portada.html', {})


def index(request):

    entries=Contract.objects.filter(author=request.user)
    print(entries)

    return render(request, 'dash/index.html', {'entries':entries,'address':'45','address2':'otro','address3':'otro2',})


def dispo(request,pk):
    entry=Contract.objects.get(id=pk)
    paramContract=Contract.objects.get(id=pk)

    account1='0xacE403ea60618f6Db0293ddDECcfabc60C699b81'
    account2='0xFbCa81d3f8a97e55ECE7F3aE76DE9aA911226f93'

    realdata=[]
    temperature=[]
    HR=[]
    ac=[]
    unix=[]
   

    with urllib.request.urlopen('https://cosasdejuan.000webhostapp.com/threeroom/api.php') as response:
        html = response.read()
#
    try:
        sensor=eval(html.decode("utf-8"))
    except:
        return HttpResponseRedirect('/index')

    realdata.append(sensor["realdata"])
    temperature.append(sensor["temp"])
    HR.append(sensor["hum"])
    ac.append(sensor["accel"])
    unix.append(sensor["unix"])



    HR_lim_max=paramContract.hrMAX
    HR_lim_min=paramContract.hrMIN

    temp_lim_max=paramContract.tempMAX
    temp_lim_min=paramContract.tempMIN

    ac_lim_max=paramContract.accMAX
    ac_lim_min=paramContract.accMIN

   #Incumplimientos por exceso de HR:
    hrMAX_incump=[('HR_max',datetime.utcfromtimestamp(unix[0][i]).strftime('%Y-%m-%d %H:%M:%S'),x) for (i,x) in enumerate(HR[0]) if x>HR_lim_max]
    hrMIN_incump=[('HR_min',datetime.utcfromtimestamp(unix[0][i]).strftime('%Y-%m-%d %H:%M:%S'),x) for (i,x) in enumerate(HR[0]) if x<HR_lim_min]

    tempMAX_incump=[('temp_max',datetime.utcfromtimestamp(unix[0][i]).strftime('%Y-%m-%d %H:%M:%S'),x) for (i,x) in enumerate(temperature[0]) if x>temp_lim_max]
    tempMIN_incump=[('temp_min',datetime.utcfromtimestamp(unix[0][i]).strftime('%Y-%m-%d %H:%M:%S'),x) for (i,x) in enumerate(temperature[0]) if x<temp_lim_min]

    accMAX_incump=[('acc_max',datetime.utcfromtimestamp(unix[0][i]).strftime('%Y-%m-%d %H:%M:%S'),x) for (i,x) in enumerate(ac[0]) if x>ac_lim_max]
    accMIN_incump=[('acc_min',datetime.utcfromtimestamp(unix[0][i]).strftime('%Y-%m-%d %H:%M:%S'),x) for (i,x) in enumerate(ac[0]) if x<ac_lim_min]

    incumplimientos={'HR_max':hrMAX_incump,'HR_min':hrMIN_incump,'temp_max':tempMAX_incump,'temp_min':tempMIN_incump,'acc_max':accMAX_incump,'acc_min':accMIN_incump}
    num_incumplimiento=len(hrMAX_incump)+len(hrMIN_incump)+len(tempMAX_incump)+len(tempMIN_incump)+len(accMAX_incump)+len(accMIN_incump)

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
    if num_incumplimiento>=1:
       # datetime.utcfromtimestamp(unix[0][1]).strftime('%Y-%m-%d %H:%M:%S')
        #w3.personal.unlockAccount(admin, 'lagruesa',4000)

        word = str(incumplimientos)
        word_bytes = word.encode('utf-8')
        messg=bytes2hex(word.encode('utf-8'))

        signed_txn = w3.eth.account.signTransaction(dict(
            nonce=w3.eth.getTransactionCount(account1),
            gasPrice = w3.eth.gasPrice, 
            gas = 1000000,
            data=messg,
            to='0xFbCa81d3f8a97e55ECE7F3aE76DE9aA911226f93',
            value=w3.toWei(0.00000005,'ether')
        ),'0x348ce564d427a3111b6536bbcff9390d69395b06ed6c486954e971d960fe8709')

        aa=w3.eth.sendRawTransaction(signed_txn.rawTransaction)

        #aa=w3.eth.sendTransaction({'to':otro, 'from':admin, 'value': 12345, 'data':messg})
        bb=w3.toBytes(aa)
        tx=w3.toHex(bb)
        url_txt='https://rinkeby.etherscan.io/tx/'+str(tx)
  


    return render(request, 'dash/dispo.html', {'entry':entry,'url_txt':url_txt,'incumplimiento':num_incumplimiento,'incumplimientos':incumplimientos,'image_base64':image_base64,'image_base64_2':image_base64_2,})
