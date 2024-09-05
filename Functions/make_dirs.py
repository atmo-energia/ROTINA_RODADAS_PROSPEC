# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 17:34:09 2021

@author: victor.romano
"""

import os

def make_dirs(date):
    try:
        os.mkdir(f'Prevs/{date}')
    except FileExistsError:
        pass