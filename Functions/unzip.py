# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 17:53:13 2021

@author: victor.romano
"""

import zipfile
import os

def unzip(DATE):
    files= os.listdir(f'Prevs/{DATE}')
    for file in files:
        with zipfile.ZipFile(f'Prevs/{DATE}/{file}', 'r') as zip_ref:
            zip_ref.extractall(f'Prevs/{DATE}')