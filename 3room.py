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

w3 = Web3(IPCProvider('/home/miguel/rinkeby/geth.ipc'))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)
#w3 = Web3(HTTPProvider('http://localhost:8545'))

admin=w3.eth.accounts[1]
otro=w3.eth.accounts[0]

w3.personal.unlockAccount(admin, 'lagruesa',4000)

word = 'Hola Juan'
word_bytes = word.encode('utf-8')
messg=bytes2hex(word.encode('utf-8'))


print(w3.eth.getBalance(admin))
aa=w3.eth.sendTransaction({'to':otro, 'from':admin, 'value': 12345, 'data':messg})
print(w3.eth.getBalance(admin))

bb=w3.toBytes(aa)
cc=w3.toHex(bb)
print(cc)

#bytes.fromhex('486f6c61204a75616e').decode('utf-8')