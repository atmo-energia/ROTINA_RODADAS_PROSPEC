# -*- coding: utf-8 -*-
"""

    --------------------------------------------------------------------------------------------------------------------

    Description: Modelo de integração com o Espaço exclusivo Ampere Consultoria
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.: O modelo foi criado pensando na execução procedural do sistema como um script único.

    Author:           @diego.yosiura
    Last Update:      11/02/21 12:10
    Created:          11/02/21 18:10
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: espaco-exclusivo
    IDE:              PyCharm
"""

import re
import os
import sys
import requests
import traceback
import hashlib
from json import loads
from json import dumps
from datetime import datetime
from datetime import timedelta


""" -- -------------------------------------------------------------------------- """
""" -- PREENCHER COM SEUS DADOS """
""" -- -------------------------------------------------------------------------- """
AUTH = {
    "username": "SEU USUARIO",
    "password": "SUA SENHA MD5",
    "token": "SEU TOKEN"
}
""" -- -------------------------------------------------------------------------- """

URL = 'https://exclusivo.ampereconsultoria.com.br'
URI = {
    'auth': URL + '/automated-login/',
    'permission': URL + '/admin/contratos/current-user-has-permission/?item={item}',
    'prevs-auto-list': URL + '/produtos/previvaz-automatico/get-list/?product_key={key}',
    'prevs-auto-download': URL + '/produtos/previvaz-automatico/get-zip/?product_key={key}&acomph='
                                 '{str_acomp}&data_prev={str_dia}&modelos={str_modelo}',

    'prevs-personalizado-create-request': URL + '/produtos/previvaz-personalizado/save/?product_key={key}',
    'prevs-personalizado-execution-queue': URL + '/produtos/previvaz-personalizado/send-data/?product_key={key}&estudo={id_estudo}',
}
ERROR_TEMPLATE = """
# ######################################################################################################################
# Date: {exception_date}
# Description: {description}
# File Name: {file_name}
# Code Line: {code_line}
# Code Name: {code_name}
# Exception Type: {exception_type}
#
# ----------------------------------------------------------------------------------------------------------------------
# [TRACEBACK]
# ===========
# 
# {traceback}
# ######################################################################################################################
"""


def exception_handler(exception, break_system=False):
    try:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        message = ERROR_TEMPLATE.format(
            description='\n#              '.join(str(exception).split('\n')),
            file_name=str(exc_traceback.tb_frame.f_code.co_filename),
            code_line=str(exc_traceback.tb_lineno),
            code_name=str(exc_traceback.tb_frame.f_code.co_name),
            exception_type=str(exc_type.__name__),
            exception_date=datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S'),
            traceback=re.sub(r'\n', '\n# ', traceback.format_exc())
        )
        print(message)
    except Exception as exce:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        message = ERROR_TEMPLATE.format(
            description=str(exce),
            file_name=str(exc_traceback.tb_frame.f_code.co_filename),
            code_line=str(exc_traceback.tb_lineno),
            code_name=str(exc_traceback.tb_frame.f_code.co_name),
            exception_type=str(exc_type.__name__),
            exception_date=datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S'),
            traceback=re.sub(r'\n', '\n# ', traceback.format_exc())
        )
        print(message)
    finally:
        if break_system:
            sys.exit(999)


class Integracao:
    """
    Classe Exemplo: Integração com o Espaço Exclusivo Ampere Consultoria.
    O sistema de autenticação usa um arquivo de texto para manter os dados de autenticação persistentes.

    Obs:
        Não use em ambiente de produção pois os dados de autenticação podem ser expostos;

    Dica:
        A persistencia pode ser obtida através de uma conexão com o Redis ou Banco de dados Relacional.
    """
    def __init__(self):
        try:
            self.access_token = None
            self.access_token_timeout = None
            self.username = AUTH['username']
            self.md5_password_hash = AUTH['password']
            self.user_token = AUTH['token']
        except Exception as ex:
            exception_handler(ex, True)

    def auth(self):
        try:
            if self.__check_auth():
                return
            payload = '{{"username":"{usr}","password":"{pwd}"}}'.format(
                usr=self.username, pwd=self.md5_password_hash)

            response = self.request_json(URI['auth'], "PUT", dumps({
                "username": self.username,
                "password": self.md5_password_hash
            }))

            if response is not None:
                if response['status']:
                    self.access_token = response['data']['access_token']
                    self.access_token_timeout = datetime.now() + timedelta(0, response['data']['timeout'])
                    self.__save_auth()
                    return
                else:
                    raise Exception("Auth Error: " + response['message'])
            raise Exception("Auth Error: Invalid status Code")
        except Exception as ex:
            exception_handler(ex, True)

    def __check_auth(self):
        try:
            if not os.path.exists('./auth.txt'):
                return False

            with open('./auth.txt', 'r') as f:
                info = str(f.read()).split('|')
                self.access_token = info[0]
                self.access_token_timeout = datetime.strptime(str(info[1]), '%Y-%m-%d %H:%M:%S.%f')
                if datetime.now() > self.access_token_timeout:
                    return False
                return True
        except Exception as ex:
            exception_handler(ex, False)
            return False

    def __save_auth(self):
        try:
            if os.path.isfile('./auth.txt'):
                os.remove('./auth.txt')

            with open('./auth.txt', 'w') as f:
                f.write('{token}|{timeout}'.format(token=self.access_token, timeout=self.access_token_timeout))
        except Exception as ex:
            exception_handler(ex, False)
            return None

    def request_prod_key(self, product):
        try:
            self.auth()
            response = self.request_json(URI['permission'].format(item=product), 'GET')
            if response is None:
                return None

            if response['status'] == 1 or response['status'] == True:
                return response['data']['product_key']
            return None
        except Exception as ex:
            exception_handler(ex, False)
            return None

    def request_json(self, uri, method, payload=None):
        try:
            response = self.__request(uri, method, {
                'x-user-token': self.user_token,
                'x-access-token': self.access_token,
                'Content-Type': 'application/json'
            }, payload)
            if response is None:
                return None

            return loads(response.text)
        except Exception as ex:
            exception_handler(ex, False)
            return None

    def request_file(self, uri, method, payload=None):
        try:
            print("Baixando arquivo")
            response = self.__request(uri, method, {
                'x-user-token': self.user_token,
                'x-access-token': self.access_token,
                'Content-Type': 'application/json'
            }, payload)
            if response is None:
                return None
            print("Arquivo baixado")
            return response.content
        except Exception as ex:
            exception_handler(ex, False)
            return None

    def __request(self, uri, method, headers, payload=None):
        try:
            response = requests.request(method, uri, headers=headers, data=payload)
            if response.status_code == 200:
                return response
            raise Exception("Invalid Status Code [{code}]: {text}".format(code=response.status_code,
                                                                          text=response.text))
        except Exception as ex:
            exception_handler(ex, False)
            return None

integracao = Integracao()

key_prevs_auto = integracao.request_prod_key('prevs-personalizado')

response_personalizado = integracao.request_json(URI['prevs-personalizado-create-request'].format(key=key_prevs_auto),
                                                 'POST', dumps({
                                                     "ready": False,
                                                     "vl_execution_counter": 0,
                                                     "ds_nome_estudo": "TESTE-AUTOMATE",
                                                     "dt_inicio": 1596803430,
                                                     "dt_fim": 1601814630,
                                                     "ds_nome_cenario": "TESTE-AUTOMATE-CENARIO",
                                                     "tipo_modelo_base": "tropical",
                                                     "ck_prev_rmv": False,
                                                     "dt_data_prev": 1596717030,
                                                     "dt_data_fim_hist": "13/08/2020",
                                                     "dt_cenario_inicio": 1601814630,
                                                     "dt_cenario_fim": 1601814630,
                                                     "cenarios": [
                                                         {
                                                             "ds_nome": "TESTE-AUTOMATE-CENARIO",
                                                             "blocos": [
                                                                 {
                                                                     "ds_modelo": "informes",
                                                                     "dt_data_prev": 1596717030,
                                                                     "ck_rmv": False,
                                                                     "dt_inicio": 1596803430,
                                                                     "dt_fim": 1601209830
                                                                 },
                                                                 {
                                                                     "ds_modelo": "tropical",
                                                                     "dt_data_prev": 1596717030,
                                                                     "ck_rmv": False,
                                                                     "dt_inicio": 1601209830,
                                                                     "dt_fim": 1601814630
                                                                 }
                                                             ]
                                                         }
                                                     ]
                                                 }))


if response_personalizado is None:
    print("Verifique os logs")
    sys.exit(0)

if response_personalizado['status'] != 1 or response_personalizado['status'] is False:
    print("Verifique os logs")
    sys.exit(0)

response_personalizado = response_personalizado['data']

response_personalizado = integracao.request_json(URI['prevs-personalizado-execution-queue'].format(
    key=key_prevs_auto,
    id_estudo=response_personalizado['id'],
), 'POST', dumps(response_personalizado))


if response_personalizado is None:
    print("Verifique os logs")
    sys.exit(0)

if response_personalizado['status'] != 1 or response_personalizado['status'] is False:
    print("Verifique os logs")
    sys.exit(0)

print("Enviado para a fila")
# Exemplo Prevs Auto
# key_prevs_auto = integracao.request_prod_key('prevs-automatico')
#
# prevs_list = integracao.request_json(URI['prevs-auto-list'].format(key=key_prevs_auto), 'GET')
#
# if prevs_list is None:
#     sys.exit(0)
#
# if prevs_list['status'] != 1 and prevs_list['status'] is not False:
#     sys.exit(0)
# prevs_list = prevs_list['data']
#
#
# str_acomp = 'ACOMPH20210209'
# str_dia = '20210210'
# str_modelo = 'CFSV2-INFORMES-RMV'
#
# if str_acomp not in prevs_list.keys():
#     print("Arquivo não encontrado")
#     sys.exit(0)
# acomp = prevs_list['ACOMPH20210209']
#
# if str_dia not in acomp.keys():
#     print("Dia não encontrado")
#     sys.exit(0)
#
# found = False
# for modelo in acomp['20210210']:
#     if modelo.lower() == (str_modelo + '.zip').lower():
#         found = True
#         break
#
# if not found:
#     print("Modelo não encontrado")
#     sys.exit(0)
#
# data_file = integracao.request_file(URI['prevs-auto-download'].format(
#     key=key_prevs_auto,
#     str_acomp=str_acomp,
#     str_dia=str_dia,
#     str_modelo=str_modelo
# ), 'GET')
#
#
# if data_file is not None:
#     with open(str_modelo + '.zip', "wb") as f:
#         f.write(data_file)
