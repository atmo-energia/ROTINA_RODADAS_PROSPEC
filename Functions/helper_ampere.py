# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 15:58:06 2022

@author: victor.romano
"""

import requests
import pandas as pd
import numpy as np
import time

from Functions.get_token import get_token as get_token_ampere
from Functions.permition_token import get_permition

def aguardar_rodadas(URL_AMPERE, prevs_list, USER_TOKEN, aut_token):
    
    while len(prevs_list) != 0:
        headers = {
                'x-access-token' : aut_token,
                'x-user-token' : USER_TOKEN,
                'Content-Type' : 'application/json'
                }
        
        request = requests.post(
            f'{URL_AMPERE}/produtos/previvaz-personalizado/get-list/',
            headers=headers
            )
        
        df = pd.DataFrame()
        id_list = []
        last_response = []
        if request.json()['status'] == 0:
            headers['x-access-token'] = get_token_ampere(USER_TOKEN)
            request = requests.post(
                f'{URL_AMPERE}/produtos/previvaz-personalizado/get-list/',
                headers=headers
                )

        for estudo in request.json()['data']:
            for dict_ in estudo:
                if dict_['id'] == 'id':
                    id_list.append(dict_['value'])
                elif dict_['id'] == 'dt_last_response':
                    last_response.append(dict_['value'])
            
        df['id'] = id_list
        df['last_resp'] = last_response
        

        df_temp = df[df['id'] == prevs_list[0].get_id()]
        if not np.isnan(df_temp['last_resp'].values[0]):
            print(df_temp['last_resp'].values[0])
            prevs_list[0].download()
            prevs_list.pop(0)
        
        time.sleep(30)
        
    return df
    