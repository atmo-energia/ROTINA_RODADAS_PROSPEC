# -*- coding: utf-8 -*-
"""

@author: João.Gabriel

"""
import requests
import os

from datetime import date, timedelta

from Functions.get_token import get_token as get_token_ampere
from Functions.permition_token import get_permition
from Functions.get_prevs import get_prevs
from Functions.make_dirs import make_dirs
from Functions.download_files import download_files
from Functions.unzip import unzip
from Functions.delete_files import delete_files
from Functions.rename_files import rename_files
from Functions.helper import get_token, getInfoFromAPI, select_versions, get_rvs, insert_VE
from Functions.helper import select_newave, select_decomp, deck_params, download_results
from Functions.Estudo import Estudo
from Functions.prevs_personalizados import prevs_personalizados
from Functions.config import modelos
from Functions.helper_ampere import aguardar_rodadas
from Functions.make_revs import make_revs
from Functions.ajuste_diario import ajuste_diario

################################# AMPERE #####################################
URL_AMPERE = 'https://exclusivo.ampereconsultoria.com.br'
USER_TOKEN = '8f11d87c-c4bb-11ec-b809-02001700dcdd'
DATE = date.today() - timedelta(days=0)
################################# AMPERE #####################################

################################# NORUS #####################################
URL_NORUS = 'https://api.prospec.app'
USERNAME = 'desenvolvimento@atmoenergia.com.br'
PASSWORD = 'TP8p&zTC'
################################# NORUS #####################################

make_dirs(DATE)
revs = make_revs()

aut_token = get_token_ampere(USER_TOKEN)
aut_permition_token = get_permition(USER_TOKEN, aut_token, 'prevs-automatico')
per_permition_token = get_permition(USER_TOKEN, aut_token, 'prevs-personalizado')
prevs_list = get_prevs(USER_TOKEN, aut_token, aut_permition_token, URL_AMPERE)
last_acomph = list(prevs_list.keys())[0]
last_prevs = list(prevs_list[last_acomph].keys())[0]
today_prevs = prevs_list[last_acomph][last_prevs]
prevs_per = []




down_files = download_files(
    last_prevs, last_acomph, DATE, URL_AMPERE,
    USER_TOKEN, aut_token, aut_permition_token, today_prevs
    )

unzip(DATE)
delete_files(DATE)
rename_files(DATE)

token = get_token(USERNAME, PASSWORD, f'{URL_NORUS}/api/Token')
print(token)
# number_requests = getInfoFromAPI(token, f'{URL_NORUS}//api/Account/Requests')
# dict_newave = getInfoFromAPI(token, f'{URL_NORUS}/api/CepelModels/Newaves')
# dict_decomp = getInfoFromAPI(token, f'{URL_NORUS}/api/CepelModels/Decomps')
# dict_gevazp = getInfoFromAPI(token, f'{URL_NORUS}//api/CepelModels/Gevazps')
# dict_versions = select_versions(dict_newave, dict_decomp, dict_gevazp)
# newave_file = select_newave('Files/Newave')
# decomp_file = select_decomp('Files/Decomp')
#
#
# for prevs in os.listdir(f'Prevs/{DATE}'):
#
#     #insert_VE(revs_ve, 'VE/', DATE, prevs)
#
#     novo_estudo = Estudo(
#                 token,
#                 f'{URL_NORUS}',
#                 f'{prevs} - ({DATE})',
#                 '',
#                 dict_versions['id_decomp'],
#                 dict_versions['id_newave']
#                 )
#
#     novo_estudo.send_file(
#         token,
#         f'Files/Newave/{newave_file}',
#         newave_file
#         )
#
#     novo_estudo.send_file(
#         token,
#         f'Files/Decomp/{decomp_file}',
#         decomp_file
#         )
#
#     # novo_estudo.send_file(
#     #     token,
#     #     'Files/Planilha/Dados prospectivo.xlsx',
#     #     'Dados prospectivo.xlsx'
#     #     )
#
#     path_prevs = f'Prevs/{DATE}/{prevs}'
#
#     parametros_estudo = deck_params(path_prevs)
#     print(parametros_estudo)
#
#     novo_estudo.generate_decks(
#         token = token,
#         initialYear = parametros_estudo['first_year'],
#         initialMonth = parametros_estudo['first_month'],
#         duration = parametros_estudo['number_months'],
#         month = parametros_estudo['months'],
#         year = parametros_estudo['years'],
#         multipleStages = parametros_estudo['trues'],
#         multipleRevision = parametros_estudo['trues'],
#         firstNewaveFile = newave_file,
#         otherNewaveFiles = ['', '', ''],
#         decompFile = decomp_file,
#         spreadsheetFile = 'Dados prospectivo.xlsx',
#         tags = []
#     )
#
#     novo_estudo.send_prevs(token, path_prevs)
#     novo_estudo.send_aux_files(token, 'Files/Auxiliares')
#     novo_estudo.associar_cortes(token, '22114')
#     info_estudo = novo_estudo.get_prospective_studies()
#     deck_id = info_estudo['Decks'][0]['Id']
#     id_newave = dict_versions['id_newave']
#     id_decomp = dict_versions['id_decomp']
#     novo_estudo.execute(token, 0, 3, 1, 3, 1, deck_id, id_decomp, id_newave)
#
