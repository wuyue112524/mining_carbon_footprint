#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import DataLoader as DL
if __name__=='__main__':

	#the path of the input csv file /hash rate file
    path = './Data/apr-sep_worker_location.csv'

    #the path of the carbon emission factor file 
    filepath = './Data/IEA_Factor_clean.csv'


    data = pd.read_csv(path,na_values='-')
    df = DL.MiningHashrate(data)
    df.function_wrapper(filepath=filepath)
