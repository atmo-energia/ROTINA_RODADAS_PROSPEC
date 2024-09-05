# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 13:05:24 2022

@author: victor.romano
"""

import os
import shutil

from datetime import date

def ajuste_diario(DATE, revs):

    def get_date(revs, DATE):
        for index, row in revs.iterrows():
            if DATE > row['Sabados']:
                continue

            month = int(row['decks'][6:8])
            year = int(row['decks'][2:6])
            return date(year, month, 1)

    def missing_prevs(revs, last_prevs, data):
        prevs = revs[(revs['month'] == data.month) & (revs['year'] == data.year)]
        revisao = last_prevs.split('.')[1]

        for index, row in prevs.iterrows():
            if row['revs'].upper() == revisao:
                return prevs.loc[index:]

    def copy_prevs(prevs_faltantes, last_prevs, path):
        if prevs_faltantes is None:
            return None

        for index, row in prevs_faltantes.iterrows():
            new_prevs = f"{path}/{last_prevs.split('.')[0]}.{row['revs'].upper()}"
            try:
                shutil.copyfile(f'{path}/{last_prevs}', new_prevs)
            except shutil.SameFileError:
                pass


    data = get_date(revs, DATE)
    diretorios = os.listdir(f'Prevs/{DATE}')
    for diretorio in diretorios:
        files = os.listdir(f'Prevs/{DATE}/{diretorio}')
        for file in files:
            if int(file[4:6]) != data.month:
               os.remove(f'Prevs/{DATE}/{diretorio}/{file}')

        files = os.listdir(f'Prevs/{DATE}/{diretorio}')
        last_prevs = files[-1]
        print(last_prevs)
        prevs_faltantes = missing_prevs(revs, last_prevs, data)
        copy_prevs(prevs_faltantes, last_prevs, f'Prevs/{DATE}/{diretorio}')
