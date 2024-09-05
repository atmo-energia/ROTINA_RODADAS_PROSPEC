# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 15:17:03 2021

@author: victor.romano
"""

import requests
import json

def get_permition(user_token, aut_token, item):

    header = {
        'x-access-token' : aut_token,
        'x-user-token' : user_token
        }
    
    params = {
        'item' : item
        }
    
    access_key = requests.get(
        f"https://exclusivo.ampereconsultoria.com.br/admin/contratos/current-user-has-permission",
        headers = header,
        params = params)
    
    access_key = json.loads(access_key.content.decode('utf-8'))

    return access_key['data']['product_key']