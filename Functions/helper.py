# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 09:53:40 2021

@author: roman
"""

import shutil
import requests
import json
import os
import mysql.connector

from datetime import datetime, date, timedelta
from mysql.connector import Error

def get_token(username, password, url):    
    
    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }
    
    tokenResponse = requests.post(url, headers=headers, data=data,
                                  verify=True)
    
    token_json = tokenResponse.json()
    
    token = token_json["access_token"]

    return token

def getInfoFromAPI(token, url, params=None):

    headers = {
        'Authorization': 'Bearer ' + token,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, params=params,
                            verify=True)

    if response.status_code != 200:
        raise ValueError('status do request não é o esperado, verificar token. '
                         + f'status code: {response.status_code}')

    return response.json()

def post_in_api(token, url, data, params=None):

    headers = {
        'Authorization': 'Bearer ' + token,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, params=params,
                             data=json.dumps(data), verify=True)


    if response.status_code != 200 and response.status_code != 201:
        raise ValueError(
            'status do request não é o esperado, verificar dados. ' + 
            f'{response.text}, {response.status_code}')

    return response.text

def create_study(token, url, title, description, idDecomp, idNewave, idDessem = 0):
    parameter = ''
    data = {
        "Title": title,
        "Description": description,
        "DecompVersionId": int(idDecomp),
        "NewaveVersionId": int(idNewave),
        "DessemVersionId": int(idDessem)
    }

    print("Creating study with the following configuration:")
    print(data)

    prospecStudyId = post_in_api(token, url, data)
    return prospecStudyId

def select_versions(dict_newave, dict_decomp, dict_gevazp):
    for version in dict_newave:
        if version['Default'] == True:
            id_newave = version['Id']

    for version in dict_decomp:
        if version['Default'] == True:
            id_decomp = version['Id']
            
    for version in dict_gevazp:
        if version['Default'] == True:
            id_gevazp = version['Id']

    return {
        'id_newave' : id_newave,
        'id_decomp' : id_decomp,
        'id_gevazp' : id_gevazp
        }

def select_newave(newave_path):
    lista_newave = os.listdir(newave_path)
    lista_newave = sorted(lista_newave)

    return lista_newave[-1]

def select_decomp(decomp_path):
    lista_decomp = os.listdir(decomp_path)
    lista_decomp = sorted(lista_decomp)

    return lista_decomp[-1]

def check_last_saturday(data):
    current_date = date.today()
    while True:
        if current_date.month != data.month:
            return True
        if data.isoweekday() == 6:
            data += timedelta(days=7)
            if current_date.month != date.month:
                 return True
            else:
                 return False

        data += timedelta(days=1)

def delete_old_prevs(lista_prevs, first_month, prevs_path):
    for prevs in lista_prevs:
        if first_month == 1:
            ano = int(prevs[:4]) + 1
        else:
            ano = int(prevs[:4])
        if datetime.strptime(prevs[:6], '%Y%m') < datetime(ano, first_month, 1):
            os.remove(f'{prevs_path}/{prevs}')
    

def deck_params(prevs_path):
    lista_prevs = os.listdir(prevs_path)
    dates = [prevs[:6] for prevs in lista_prevs]
    unique_dates = sorted(list(set(dates)))
    number_months = len(unique_dates)
    first_year = int(unique_dates[0][:4])
    if check_last_saturday(date.today()):
        first_month = int(unique_dates[0][4:6])
        delete_old_prevs(lista_prevs, first_month, prevs_path)
        
    else:
        first_month = int(unique_dates[0][4:6])
        
    trues = [True for date in unique_dates]
    years = [int(date[:4]) for date in unique_dates]
    months = [int(date[4:6]) for date in unique_dates]
    empty_str = ['' for date in unique_dates]

    dict_params = {
        'number_months' : number_months,
        'first_year' : first_year,
        'first_month' : first_month,
        'trues' : trues,
        'months' : months,
        'years' : years,
        'empty_str' : empty_str,
        }
    return dict_params

def download_results(token, url):

    headers = {
        'Authorization': 'Bearer ' + token,
        "Content-Type": "application/json"
    }
    

    response = requests.post(url, headers=headers, stream=True,
                             verify=True)
    
    print(response.status_code)
    print(datetime.now())
    
    with open(('Resultados/download.zip'), 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                file.write(chunk)

def get_rvs(path):
    VE = os.listdir(path)[0]
    date = VE.split('-')[0]
    CONFIG = {
        'user' : 'admin',
        'password' : 'enexenergia',
        'host' : 'middledb.cbz3e8feirto.sa-east-1.rds.amazonaws.com',
        'database' : 'estudo_casos',
        'port' : '3306'}

    try:
        connection = mysql.connector.connect(**CONFIG)
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
        
    cursor = connection.cursor()

    try:
        cursor.execute(
            f"""
            SELECT * FROM revs
            WHERE DECKS NOT LIKE '%_s1%' AND DECKS LIKE '%DC{date}%'
            """
            )
        print("query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    
    rvs = []
    for rodada in cursor.fetchall():
        rvs.append(rodada[1])


    return rvs
    
def insert_VE(revs_ve, path_ve, DATE, prevs):
    personalizados = [
        'ONS-CLIMATOLOGIA',
        'ONS-TROPICAL'
        ]
    for personalizado in personalizados:
        if personalizado in prevs:
            VE = os.listdir(path_ve)[0]
            for rv in revs_ve:
                copy = VE.split('.')[0] + '.' + rv.upper()
                shutil.copy(f'{path_ve}/{VE}', f'Prevs/{DATE}/{prevs}/{copy}')
        