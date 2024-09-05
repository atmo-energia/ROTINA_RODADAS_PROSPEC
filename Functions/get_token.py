# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 14:31:42 2021

@author: victor.romano
"""
import requests
import hashlib
import json

def get_token(user_token):

    login = 'victor.romano@atmoenergia.com.br'
    senha_hash = hashlib.md5(b'Cobra23040640!').hexdigest()
    
    
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