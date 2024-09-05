# -*- coding: utf-8 -*-
"""

@author: João.Gabriel

"""

import os
import shutil
from datetime import date
from dateutil.relativedelta import relativedelta


def delete_files(DATE):
    hoje = date.today()
    # Adiciona um mês à data atual
    proximo_mes = hoje + relativedelta(months=1)
    hj = proximo_mes.strftime("%Y%m")

    diretorios = os.listdir(f'Prevs/{DATE}')
    for diretorio in diretorios:
        if '.zip' in diretorio:
            os.remove(f'Prevs/{DATE}/{diretorio}')

    diretorios = os.listdir(f'Prevs/{DATE}')

    for diretorio in diretorios:
        arquivos = os.listdir(f'Prevs/{DATE}/{diretorio}')
        for arquivo in arquivos:
            # Checa se o nome do arquivo contém a string 'hj'
            if hj in arquivo:
                try:
                    shutil.rmtree(f'Prevs/{DATE}/{diretorio}/{arquivo}')
                except NotADirectoryError:
                    os.remove(f'Prevs/{DATE}/{diretorio}/{arquivo}')
            elif ('DAT' not in arquivo) and ('REV' not in arquivo) or ('csv' in arquivo) or ('xlsx' in arquivo):
                try:
                    shutil.rmtree(f'Prevs/{DATE}/{diretorio}/{arquivo}')
                except NotADirectoryError:
                    os.remove(f'Prevs/{DATE}/{diretorio}/{arquivo}')