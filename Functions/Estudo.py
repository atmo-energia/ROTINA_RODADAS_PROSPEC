# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 11:41:20 2021

@author: roman
"""

import requests
import json
import os


class Estudo():
    def __init__(self, token, basic_url, title, description, id_decomp, 
                 id_newave, id_dessem=0, params=None):

        self.params=params
        self.basic_url = basic_url
        url = basic_url + '/api/prospectiveStudies'
        data = {
            "Title": title,
            "Description": description,
            "DecompVersionId": int(id_decomp),
            "NewaveVersionId": int(id_newave),
            "DessemVersionId": int(id_dessem)
        }

        print("Creating study with the following configuration:")
        print(data)

        self.headers = {
        'Authorization': 'Bearer ' + token,
        "Content-Type": "application/json"
    }

        response = requests.post(url, headers=self.headers, params=params,
                             data=json.dumps(data), verify=True)

        if response.status_code != 200 and response.status_code != 201:
            raise ValueError(
                'status do request não é o esperado, verificar dados. ' +
                f'{response.text}, {response.status_code}')

        self.id_estudo = response.text


    def get_info(self, token):
        headers = {
            'Authorization': 'Bearer ' + token,
            "Content-Type": "application/json"
        }

        url = self.basic_url + '/api/prospectiveStudies/' + self.id_estudo

        response = requests.get(url, headers=headers, params=self.params, verify=True)

        if response.status_code != 200:
            raise ValueError('status do request não é o esperado, verificar token')

        self.info_estudo = json.loads(response.text)

        return self.info_estudo

    def send_file(self, token, filepath, filename):
        url = f'{self.basic_url}/api/prospectiveStudies/{self.id_estudo}/UploadFiles'

        headers = {
            'Authorization': 'Bearer ' + token
        }

        files = {
            'file': (filename, open(filepath, 'rb'),
                     'multipart/form-data', {'Expires': '0'})
        }

        response = requests.post(url, headers=headers, files=files,
                                 verify=True)
        
        print(response.text)
        print(response.status_code)


    def generate_decks(self, token, initialYear, initialMonth, duration, month,
                           year, multipleStages, multipleRevision, firstNewaveFile,
                           otherNewaveFiles, decompFile, spreadsheetFile, tags,
                           params=''):

        url = f'{self.basic_url}/api/prospectiveStudies/{self.id_estudo}/Generate'
        listOfDeckConfiguration = []
        listOfTags = []
        i = 0
        for deck in month:
            deckConfiguration = {}
            deckConfiguration['Year'] = year[i]
            deckConfiguration['Month'] = month[i]
            deckConfiguration['MultipleStages'] = multipleStages[i]
            deckConfiguration['MultipleRevisions'] = multipleRevision[i]
            if (i > 0):
                if (otherNewaveFiles[i] != ''):
                    deckConfiguration['NewaveUploaded'] = otherNewaveFiles[i]
            listOfDeckConfiguration.append(deckConfiguration)
            i = i + 1

        for tag in tags:
            tagsConfiguration = {}
            tagsConfiguration['Text'] = tag
            listOfTags.append(tagsConfiguration)

        data = {
            "InitialYear": initialYear,
            "InitialMonth": initialMonth,
            "Duration": duration,
            "DeckCreationConfigurations": listOfDeckConfiguration,
            "Tags": listOfTags,
            "InitialFiles": {
                "NewaveFileName": firstNewaveFile,
                "DecompFileName": decompFile,
                "SpreadsheetFileName": spreadsheetFile
            }
        }

        print("Gerando decks com as seguintes configuracoes para o estudo: ",
              str(self.id_estudo))
        print(data)
        print(40*'#')

        response = requests.post(url, headers=self.headers, params=params,
                         data=json.dumps(data), verify=True)
        
        print(response.json())

        self.info_estudo = self.get_info(token)
        
        for deck in self.info_estudo['Decks']:
            if deck['Model'] == 'NEWAVE':
                self.id_deck_nw = deck['Id']
                break

        return None

    def send_prevs(self, token, prevs_path):
        dict_prevs = {}
        for deck in self.info_estudo['Decks']:
            id_deck = deck['Id']
            filename = deck['FileName']
            data_prevs = filename[2:8]
            if deck['Model'] == 'DECOMP':
                rv = f'.RV{int(filename[12]) - 1}'
            else:
                rv = '.RV0'
            prevs_name = f'{data_prevs}-PREVS{rv}'

            headers = {
                'Authorization': 'Bearer ' + token
            }
            
            print(headers)
            try:
                dict_prevs[prevs_name] =[
                        prevs_name, open(f'{prevs_path}/{prevs_name}', 'rb'),
                        'multipart/form-data', {'Expires': '0'}
                    ]

            except FileNotFoundError:
                print(f'Prevs {prevs_name} correspondente ao deck {filename} ' + 
                      'não foi encontrado')
                continue

        url = (
            f'{self.basic_url}/api/prospectiveStudies/{self.id_estudo}'
            + '/UploadMultiplePrevs'
        )

        response = requests.post(url, headers=headers, files=dict_prevs, verify=True)

    def send_aux_files(self, token, aux_path):
        for deck in self.info_estudo['Decks']:
            if deck['Model'] == 'DECOMP':
                id_deck = deck['Id']
                break
        
        dict_files = {}
        for file in os.listdir(aux_path):
            headers = {
                'Authorization': 'Bearer ' + token
            }

            dict_files[file] = [
                file, open(f'{aux_path}/{file}', 'rb'),
                             'multipart/form-data', {'Expires': '0'}
                ]

        url = (
            f'{self.basic_url}/api/prospectiveStudies/{self.id_estudo}'
            + f'/UploadFiles?deckId={id_deck}'
        )

        response = requests.post(url, headers=headers, files=dict_files, verify=True)
        print(response.text)

    def execute(
            self, token, 
            execution_mode, 
            infeasibility_handling, 
            max_restarts, 
            InfeasibilityHandlingSensibility, 
            MaxTreatmentRestartsSensibility,
            deckId,
            decompVersionId,
            newaveVersionId
            ):
        
        
        data = {
          "StartingDeckId": deckId,
          "EphemeralInstanceType": 'c5.18xlarge',
          "SecondaryServer": 0,
          "ServerId": 0,
          "QueueId": 0,
          "ExecutionMode": execution_mode,
          "InfeasibilityHandling": infeasibility_handling,
          "InfeasibilityHandlingSensibility": InfeasibilityHandlingSensibility,
          "MaxTreatmentRestarts": max_restarts,
          "MaxTreatmentRestartsSensibility": MaxTreatmentRestartsSensibility,
          "MaxExtraTreatmentRestarts": 0,
          "MaxExtraTreatmentRestartsSensibility": 0,
          "ServerPurchaseOption": 0,
          "SpotBreakdownOption": 0,
        #   "DecksRunModel": [
        #     {
        #       "DeckId": deckId,
        #       "DecompVersionId": decompVersionId,
        #       "NewaveVersionId": newaveVersionId,
        #       "DessemVersionId": 1,
        #       "InfeasibilityHandling": 0,
        #       "InfeasibilityHandlingSensibility": 0,
        #       "MaxTreatmentRestarts": 0,
        #       "MaxTreatmentRestartsSensibility": 0,
        #       "MaxExtraTreatmentRestarts": 0
        #     }
        #   ]
        }

        url = (
            f'{self.basic_url}/api/prospectiveStudies/{self.id_estudo}/Run'
        )

        response = requests.post(
            url, headers=self.headers, data=json.dumps(data), verify=True
            )
        
        print(data)
        print(response.json())
        
    def associar_cortes(self, token, id_nw):

        listOfAssociation = []

        associationConfiguration = {}
        associationConfiguration['DestinationDeckId'] = self.id_deck_nw
        associationConfiguration['SourceStudyId'] = id_nw
        listOfAssociation.append(associationConfiguration)

        parameter = ''
        data = {
            "cortesAssociation": listOfAssociation,
        }

        print("Usando a seguinte configuracao do estudo: ", str(self.id_estudo))
        print(data)

        url = self.basic_url + '/api/prospectiveStudies/' + str(self.id_estudo) + '/Associate'


        response = requests.post(
            url, headers=self.headers, params='', data=json.dumps(data),
            verify=True
            )
        
        print(response.status_code)
        print(response.text)

    
    def get_prospective_studies(self):
        url = self.basic_url + '/api/prospectiveStudies/' + str(self.id_estudo)
        response = requests.get(
            url, headers=self.headers, verify=True
            )
        
        return response.json()
        