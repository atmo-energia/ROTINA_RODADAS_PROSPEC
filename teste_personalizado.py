# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 11:28:26 2022

@author: victor.romano
"""

import requests
import json
import hashlib

from datetime import date, timedelta, datetime

URL_AMPERE = 'https://exclusivo.ampereconsultoria.com.br'
USER_TOKEN = 'fdeec452-ceae-11eb-ae55-02001700dcdd'

def get_token(user_token):

    login = 'victor.romano@mpccomercializadora.com.br'
    senha_hash = hashlib.md5(b'Rom@no662607').hexdigest()
    
    
    token_header = {
        'x-user-token' : user_token,
        'Content-Type' : 'application/json'
        }
    
    
    token_body = {
    	"username": login,
    	"password": senha_hash
    }
    
    token_json = json.dumps(token_body).encode("utf-8")
    
    token = requests.put(
        'https://exclusivo.ampereconsultoria.com.br/automated-login/',
        headers = token_header,
        data = token_json
        )
    
    token = json.loads(token.content.decode('utf-8'))
    token = token['data']['access_token']
    
    return token

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

aut_token = get_token(USER_TOKEN)
permition_token = get_permition(USER_TOKEN, aut_token, 'prevs-personalizado')


hoje = datetime.today()



body = {
    "ready":False,
    "vl_execution_counter":0,
    "ds_nome_estudo":"ESTUDO-TESTE",
    "dt_inicio":datetime.timestamp(hoje + timedelta(days=1)),
    "dt_fim":datetime.timestamp(hoje + timedelta(days=60)),
    "ds_nome_cenario":"CENARIO-TESTE",
    "tipo_modelo_base":"tropical",
    "ck_prev_rmv":False,
    "dt_data_prev":datetime.timestamp(hoje + timedelta(days=1)),
    "dt_data_fim_hist":"13/08/2020",
    "dt_cenario_inicio":datetime.timestamp(hoje + timedelta(days=1)),
    "dt_cenario_fim":datetime.timestamp(hoje + timedelta(days=60)),
    "cenarios":[
        {
            "ds_nome":"TESTANDO",
            "blocos":[
                {
                    "ds_modelo":"climatologia",
                    "dt_data_prev":datetime.timestamp(hoje + timedelta(days=1)),
                    "ck_rmv":False,
                    "dt_inicio":datetime.timestamp(hoje + timedelta(days=1)),
                    "dt_fim":datetime.timestamp(hoje + timedelta(days=60))
                }
            ]
        }
    ]

}

headers = {
    'x-access-token' : aut_token,
    'x-user-token' : USER_TOKEN,
    'Content-Type' : 'application/json'
    }


"""r = requests.post(
f'https://exclusivo.ampereconsultoria.com.br/produtos/previvaz-personalizado/save/?product_key={permition_token}',
headers=headers,
json=body
)

lista = requests.post(
        'https://exclusivo.ampereconsultoria.com.br/produtos/previvaz-personalizado/get-list/',
        headers=headers
        )

b = requests.post(
    f'https://exclusivo.ampereconsultoria.com.br/produtos/previvaz-personalizado/send-data/?product_key={permition_token}&estudo=5568',
    headers=headers)"""
r = requests.get(
f'https://exclusivo.ampereconsultoria.com.br/produtos/previvaz-ena-diaria/get-data/?product_key={permition_token}',
headers=headers,
)
