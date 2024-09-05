# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 16:30:33 2021

@author: victor.romano
"""
import requests
import hashlib
import json


def get_prevs(USER_TOKEN, aut_token, permition_token, URL):
    headers = {
        'x-access-token' : aut_token,
        'x-user-token' : USER_TOKEN
        }
    
    params = {
        'product_key' : permition_token
        }
    
    
    prevs_list = requests.get(
       f"{URL}/produtos/previvaz-automatico/get-list",
       headers = headers,
       params = params
    )
    
    prevs_list = json.loads(prevs_list.content.decode('utf-8'))['data']
    
    return prevs_list