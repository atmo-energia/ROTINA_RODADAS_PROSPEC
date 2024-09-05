# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 14:18:39 2021

@author: roman
"""


import mysql.connector
import os
import shutil

global CONFIG
global con
global cur

CONFIG = {
    'user' : 'admin',
    'password' : 'enexenergia',
    'host' : 'middledb.cbz3e8feirto.sa-east-1.rds.amazonaws.com',
    'database' : 'estudo_casos',
    'port' : '3306'}

con = mysql.connector.connect(**CONFIG)
cur = con.cursor()

def copiar_primeira(DATA):
    for modelo in os.listdir(f'Prevs/{DATA}'):
        try:
            lista_prevs = os.listdir(f'Prevs/{DATA}/{modelo}')
            fir_date = lista_prevs[0].split('-')[0]
            sec_date = lista_prevs[1].split('-')[0]
            thi_date = lista_prevs[-1].split('-')[0]
            cur.execute(f"""
                        SELECT DISTINCT(SABADOS), REVS FROM revs 
                        WHERE SABADOS LIKE '{fir_date[:4]}-{fir_date[4:6]}%'
                        OR SABADOS LIKE '{sec_date[:4]}-{sec_date[4:6]}%'
                        OR SABADOS LIKE '{thi_date[:4]}-{thi_date[4:6]}%'
                        """)
            prevs_banco = []
        
        except IndexError:
            prevs_banco = []
            continue
        
        for tupla in cur.fetchall():
            prevs_banco.append(f'{tupla[0][0:4]}{tupla[0][5:7]}-PREVS.{tupla[1]}'.upper())

        lista_prevs.sort()
        prevs_banco.sort(reverse=True)
        for prevs in prevs_banco:
            numero = int(prevs[-1]) + 1
            next_prevs = f'{prevs[:-1]}{numero}'
            if prevs not in lista_prevs and next_prevs in lista_prevs:
                shutil.copy(
                    f'Prevs/{DATA}/{modelo}/{next_prevs}',
                    f'Prevs/{DATA}/{modelo}/{prevs}'
                    )
