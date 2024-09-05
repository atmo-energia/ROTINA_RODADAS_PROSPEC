# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 10:24:27 2021

@author: roman
"""
import pandas as pd

from datetime import date, timedelta
from calendar import monthrange

def bug_dia1(data, df):
    if data.day == 1:
        index = df[df['Sabados'] == data].index[0]
        df.loc[index, 'primeiroSabado'] = False
        df.loc[index + 1, 'primeiroSabado'] = True

def primeiroSabado(data):
    mes = data.month
    num_days = monthrange(data.year, data.month)[1]
    prevs_data = data - timedelta(days=7)

    if prevs_data.month != mes:
        return True
    else:
        return False

def rev(primeiroSabado):
    revs = []
    a = 0
    for index in range(len(primeiroSabado)):
        try:
            if primeiroSabado[index + 1] == True:
                a = 0
                revs.append(f'rv{a}')
                continue
        except KeyError:
            pass
        a += 1
        revs.append(f'rv{a}')

    return revs

def decks(revs, sabados):
    decks = []
    for index in range(len(sabados)):
        rev = int(revs[index][2])
        semana = rev + 1
        if rev == 0 and sabados[index].day >= 15:
            decks.append("DC{:%Y}{:%m}-sem{}".format(sabados[index]+ timedelta(days=20) , sabados[index]+ timedelta(days=20), semana))
        else:
            decks.append("DC{:%Y}{:%m}-sem{}".format(sabados[index], sabados[index], semana))

    return decks

def get_month(deck):
    return int(deck[6:8])

def get_year(deck):
    year = int(deck[2:6])
    return year


def make_revs():
    lista_sabados = []
    
    data = date.today() - timedelta(days=60)
    year = data.year
    
    while data.isoweekday() != 6:
        data += timedelta(days=1)
    
    while data.year <= year + 2:
        lista_sabados.append(data)
        data += timedelta(days=7)

        
    df = pd.DataFrame(lista_sabados, columns=['Sabados'])
    
    df['primeiroSabado'] = df['Sabados'].apply(lambda row: primeiroSabado(row))
    df['Sabados'].apply(lambda row: bug_dia1(row, df))
    primeiroTrue = df[df['primeiroSabado'] == True].index[0]
    df = df.loc[primeiroTrue:, :].reset_index(drop=True)
    df['revs'] = rev(df['primeiroSabado'])
    df['decks'] = decks(df['revs'], df['Sabados'])
    df['month'] = df['decks'].apply(lambda row: get_month(row))
    df['year'] = df['decks'].apply(lambda row: get_year(row))

    
    df.drop(columns=['primeiroSabado'], inplace=True)

    return df

if __name__ == '__main__':
    df = make_revs()

