# -*- coding: utf-8 -*-
"""

@author: João.Gabriel

"""
import os
from datetime import date, timedelta

# Calcula a data de ontem
ontem = date.today() - timedelta(days=1)
ontem_date = ontem.strftime("%Y%m%d")

# Nomes dos arquivos de acordo com a data de ontem
ONS_OFICIAL = f'ONS-OFICIAL-NT00752020-RVEXT-VMEDPONDERADA'
GFS35_ATUAL = f'GFS-ATUAL-GEFS35-PREV-{ontem_date}-RMV'
EC15 = f'EC15-ATUAL-EC45-PREV-{ontem_date}-RMV'
GEFS_35_DIAS = f'GEFS-35DIAS-PREV-{ontem_date}-RMV'


def rename_files(date_str):

    base_path = f'Prevs/{date_str}'

    if not os.path.exists(base_path):
        print(f"Diretório {base_path} não encontrado.")
        return

    # Lista todos os diretórios em 'Prevs/{date_str}'
    try:
        diretorios = os.listdir(base_path)
    except Exception as e:
        print(f"Erro ao listar diretórios: {e}")
        return

    for diretorio in diretorios:
        dir_path = os.path.join(base_path, diretorio)

        if not os.path.isdir(dir_path):
            continue

        try:
            arquivos = os.listdir(dir_path)
        except Exception as e:
            print(f"Erro ao listar arquivos em {dir_path}: {e}")
            continue

        ########### Verifica se o nome do diretório corresponde a ONS_OFICIAL ###########
        # Verifica se o diretório contém "ONS_OFICIAL"
        if ONS_OFICIAL in diretorio:
            for arquivo in arquivos:
                if 'REVF' not in arquivo:
                    # Verifica se "DAT" está no nome do arquivo
                    if "DAT" in arquivo:
                        continue  # Passa para o próximo arquivo sem fazer nada
                    partes = arquivo.split('.')
                    mes_ano = partes[-2]
                    rv = partes[-1].replace("E", "")
                    prefixo = 'Prevs'
                    novo_nome = f'{mes_ano}-{prefixo}.{rv}'
                    print(novo_nome)
                    try:
                        os.rename(
                            os.path.join(dir_path, arquivo),
                            os.path.join(dir_path, novo_nome)
                        )
                    except Exception as e:
                        print(f"Erro ao renomear {arquivo}: {e}")

                # Caso contrário, remove o arquivo que contém 'REVF'
                else:
                    try:
                        os.remove(os.path.join(dir_path, arquivo))
                    except Exception as e:
                        print(f"Erro ao remover {arquivo}: {e}")
        #
        # ########### Verifica se o nome do diretório corresponde a GEFS35_ATUAL ###########
        elif GFS35_ATUAL in diretorio:
            for arquivo in arquivos:

                if 'DAT' in arquivo:
                    os.remove(os.path.join(dir_path, arquivo))

                elif 'REVF' not in arquivo:
                    partes = arquivo.split('.')
                    mes_ano = partes[-2]
                    rv = partes[-1].replace("E", "")
                    prefixo = 'GFS35_ATUAL'
                    novo_nome = f'{mes_ano}-prevs-{prefixo}.{rv}'
                    try:
                        os.rename(
                            os.path.join(dir_path, arquivo),
                            os.path.join(dir_path, novo_nome)
                        )
                    except Exception as e:
                        print(f"Erro ao renomear {arquivo}: {e}")

                else:
                    try:
                        os.remove(os.path.join(dir_path, arquivo))

                    except Exception as e:
                        print(f"Erro ao remover {arquivo}: {e}")
        #
        # ########### Verifica se o nome do diretório corresponde a ETA40 ###########
        if EC15 in diretorio:
            for arquivo in arquivos:

                if 'DAT' in arquivo:
                    os.remove(os.path.join(dir_path, arquivo))

                elif 'REVF' not in arquivo:
                    partes = arquivo.split('.')
                    mes_ano = partes[-2]
                    rv = partes[-1].replace("E", "")
                    prefixo = 'ATUAL-EC15'
                    novo_nome = f'{mes_ano}-prevs-{prefixo}.{rv}'
                    try:
                        os.rename(
                            os.path.join(dir_path, arquivo),
                            os.path.join(dir_path, novo_nome)
                        )
                    except Exception as e:
                        print(f"Erro ao renomear {arquivo}: {e}")

                else:
                    try:
                        os.remove(os.path.join(dir_path, arquivo))

                    except Exception as e:
                        print(f"Erro ao remover {arquivo}: {e}")


        # ########### Verifica se o nome do diretório corresponde a GEFS_35_DIAS ###########
        elif GEFS_35_DIAS in diretorio:
            for arquivo in arquivos:

                if 'DAT' in arquivo:
                    os.remove(os.path.join(dir_path, arquivo))

                elif 'REVF' not in arquivo:
                    partes = arquivo.split('.')
                    mes_ano = partes[-2]
                    rv = partes[-1].replace("E", "")
                    prefixo = 'GEFS-35DIAS'
                    novo_nome = f'{mes_ano}-prevs-{prefixo}.{rv}'
                    try:
                        os.rename(
                            os.path.join(dir_path, arquivo),
                            os.path.join(dir_path, novo_nome)
                        )
                    except Exception as e:
                        print(f"Erro ao renomear {arquivo}: {e}")

                else:
                    try:
                        os.remove(os.path.join(dir_path, arquivo))

                    except Exception as e:
                        print(f"Erro ao remover {arquivo}: {e}")