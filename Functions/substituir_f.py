# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 13:04:55 2021

@author: roman
"""

import mysql.connector
import os

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


def substituir_f(DATA):
    for modelo in os.listdir(f'Prevs/{DATA}'):
        for prevs in os.listdir(f'Prevs/{DATA}/{modelo}'):
            if 'F' in prevs:
                cur.execute(f"SELECT REVS FROM revs WHERE SABADOS LIKE '{prevs[:4]}-{prevs[4:6]}%'")
                rvs = cur.fetchall()
                rvs.sort()
                rv = str(rvs[-1][0]).upper()
                new_name = f"{prevs.split('.')[0]}.{rv}"
                try:
                    os.rename(
                        f'Prevs/{DATA}/{modelo}/{prevs}',
                        f'Prevs/{DATA}/{modelo}/{new_name}')
                except FileExistsError:
                    os.remove(f'Prevs/{DATA}/{modelo}/{prevs}')