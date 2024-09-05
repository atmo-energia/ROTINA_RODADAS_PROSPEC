# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 17:40:15 2021

@author: victor.romano
"""
from datetime import date, timedelta

import requests

def download_files(prevs, acomph, DATE, URL, USER_TOKEN, aut_token, permition_token, today_prevs):

    ontem = date.today() - timedelta(days=1)
    ontem_date = ontem.strftime("%Y%m%d")

    files = [
        'ONS-OFICIAL-NT00752020-RVEXT-VMEDPONDERADA.zip',
        f'GFS-ATUAL-GEFS35-PREV-{ontem_date}-RMV.zip',
        f'EC15-ATUAL-EC45-PREV-{ontem_date}-RMV.zip',
        f'GEFS-35DIAS-PREV-{ontem_date}-RMV.zip'
        # 'NOVAPREVC-ONS-OFICIAL-NT00752020.zip',
        # 'ECMWF-ENSEMBLE-RMV.zip',
#        'ECMWF-46DIAS-ENSEMBLE-PMED-RMV.zip',
#        'ECMWF-46DIAS-ENSEMBLE-PMED.zip',
#        'ONS-OFICIAL-ATUAL-CLIMATOLOGIA-RMV.zip',
#        'ONS-OFICIAL-ATUAL-TROPICAL-ATUAL-RMV.zip'
        ]
    
    downloaded_files = []

    headers = {
        'x-access-token' : aut_token,
        'x-user-token' : USER_TOKEN
        }
    
    
    for file in files:
        if file in today_prevs:
            params = {
                'product_key' : permition_token,
                'acomph' : acomph,
                'data_prev' : prevs,
                'modelos' : file.split('.')[0]}
            
            print(f'ACOMPH: {acomph}')
            print(f'DATA PREVS: {prevs}')
            
            download_request = requests.get(
                    f'{URL}/produtos/previvaz-automatico/get-zip',
                    headers=headers,
                    params = params
                    )

            if download_request.status_code == 200:
                downloaded_files.append(file)
                
                with open(f'Prevs/{DATE}/{file}', 'wb') as f:
                    for chunk in download_request.iter_content(chunk_size=8192):
                        f.write(chunk)
    
    return downloaded_files