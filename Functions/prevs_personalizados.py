# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 16:00:59 2022

@author: victor.romano
"""

from Functions.get_token import get_token as get_token_ampere
from Functions.permition_token import get_permition

from datetime import timedelta, datetime, date

import requests
import wget

class prevs_personalizados():
    def __init__(self, permition_token, aut_token, USER_TOKEN, previsoes):
        hoje = datetime.today()
        self.permition_token = permition_token
        self.aut_token = aut_token
        self.USER_TOKEN = USER_TOKEN
        self.headers = {
            'x-access-token' : aut_token,
            'x-user-token' : USER_TOKEN,
            'Content-Type' : 'application/json'
            }
        
        blocos = []
        for previsao in previsoes:
            blocos.append(
                {
                    "ds_modelo":previsao['modelo'],
                    "dt_data_prev":datetime.timestamp(hoje),
                    "ck_rmv":False,
                    "dt_inicio":datetime.timestamp(hoje + timedelta(days=previsao['inicio'])),
                    "dt_fim":datetime.timestamp(hoje + timedelta(days=previsao['fim']))
                }
                )
            
        self.nome = previsao['nome'].upper()

        body = {
            "ready":False,
            "vl_execution_counter":0,
            "ds_nome_estudo":f"{previsao['nome']}-{date.today()}".upper(),
            "dt_inicio":datetime.timestamp(hoje + timedelta(days=1)),
            "dt_fim":datetime.timestamp(hoje + timedelta(days=60)),
            "ds_nome_cenario":f"{previsao['nome']}-{date.today()}".upper(),
            "tipo_modelo_base":"tropical",
            "ck_prev_rmv":False,
            "dt_data_prev":datetime.timestamp(hoje + timedelta(days=1)),
            "dt_data_fim_hist":"13/08/2020",
            "dt_cenario_inicio":datetime.timestamp(hoje + timedelta(days=1)),
            "dt_cenario_fim":datetime.timestamp(hoje + timedelta(days=60)),
            "cenarios":[
                {
                    "ds_nome":f"{previsao['nome']}-{date.today()}".upper(),
                    "blocos":blocos
                }
            ]
        }
    
        r = requests.post(
        f'https://exclusivo.ampereconsultoria.com.br/produtos/previvaz-personalizado/save/?product_key={permition_token}',
        headers=self.headers,
        json=body
        )
        
        request_json = r.json()
        
        self.id = request_json['data']['id']
        print(self.id)
        
        return None
    
    def execute(self):
        r = requests.post(
            f'https://exclusivo.ampereconsultoria.com.br/produtos/previvaz-personalizado/'+
            f'send-data/?product_key={self.permition_token}&estudo={self.id}',
            headers=self.headers)
        
        
        return r.json()
    
    def get_id(self):
        
        
        return self.id
    
    def download(self):
        body = {
            'caso_id' : self.id
            }
        
        r = requests.post(
            f'https://exclusivo.ampereconsultoria.com.br/produtos/previvaz-personalizado/'+
            f'get-download-link/?product_key={self.permition_token}',
            headers=self.headers,
            json=body
            )
        
        request_json = r.json()
        if request_json['status'] == 0:
            self.aut_token = get_token_ampere(self.USER_TOKEN)
            self.permition_token = get_permition(self.USER_TOKEN, self.aut_token, 'prevs-personalizado')
            self.headers = {
                'x-access-token' : self.aut_token,
                'x-user-token' : self.USER_TOKEN,
                'Content-Type' : 'application/json'
                }
            r = requests.post(
                f'https://exclusivo.ampereconsultoria.com.br/produtos/previvaz-personalizado/'+
                f'get-download-link/?product_key={self.permition_token}',
                headers=self.headers,
                json=body
                )
            request_json = r.json()
        
            
        if request_json['status'] == 1:
            print('############### aqui ###############')
            download_request = requests.get(
                    request_json['data']['link']
                    )
            print(request_json['data']['link'])
        
            with open(f'Prevs/{date.today()}/{self.nome}.zip', 'wb') as f:
                for chunk in download_request.iter_content(chunk_size=8192):
                    f.write(chunk)
            
        return request_json['data']['link']


        