#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 21:57:21 2018

@author: miguel
"""
import json
import web3
from web3 import Web3, IPCProvider

from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.middleware import geth_poa_middleware

def bytes2hex(bytes):
    return '0x'+''.join('{:x}'.format(b) for b in bytes)

w3 = Web3(HTTPProvider('https://rinkeby.infura.io/v3/4f76921d343748539da91921c5480804'))
#w3.middleware_stack.inject(geth_poa_middleware, layer=0)


account1='0xacE403ea60618f6Db0293ddDECcfabc60C699b81'
account2='0xFbCa81d3f8a97e55ECE7F3aE76DE9aA911226f93'
bal=w3.eth.getBalance(account1)
bal2=w3.eth.getBalance(account2)

signed_txn = w3.eth.account.signTransaction(dict(
    nonce=w3.eth.getTransactionCount(account1),
    gasPrice = w3.eth.gasPrice, 
    gas = 100000,
    to='0xFbCa81d3f8a97e55ECE7F3aE76DE9aA911226f93',
    value=w3.toWei(0.000005,'ether')
  ),
  '0x348ce564d427a3111b6536bbcff9390d69395b06ed6c486954e971d960fe8709')

aa=w3.eth.sendRawTransaction(signed_txn.rawTransaction)

