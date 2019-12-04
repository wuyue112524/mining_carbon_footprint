#!/usr/bin/env python
# coding: utf-8


from tkinter import *
from tkinter import ttk


# 1. create a window and a frame
def print_path_hash():
	
    path = hash_path.get()
    # Label_3 =Label(frame)
    # Label_3['text']= path
    # Label_3.grid(row=4,padx=4)
    new_path = './Data/' + path
    return new_path


def print_path_carbon():
    carbon = carbon_path.get()
    # Label_4 =Label(frame)
    # Label_4['text']= carbon
    # Label_4.grid(row=6,padx=4)
    new_carbon = './Data/' + carbon
    return new_carbon


def calculate_function():
    import os
    import pandas as pd
    import numpy as np
    import datetime
    
    import DataLoader as DL
    
  
    if __name__ == '__main__':
        try:
            # the path of the input csv file /hash rate file
          
            path = print_path_hash()
            
            # the path of the carbon emission factor file

            filepath = print_path_carbon()
           
            data = pd.read_csv(path, na_values='-')
            
            df = DL.MiningHashrate(data)
            df.function_wrapper(filepath=filepath)
            Label(frame, text="Files have been created successfully.").grid(row=8, padx=4)
        except Exception as e:
            Label(frame, text="Files cannot be created due to reason /n." + str(e)).grid(row=8, padx=4)


root = Tk()
root.title('CO2 Calculation')
root.geometry('500x300')
frame = Frame(root)

# 2. create two labels

# get the path for the hashrate distribution
Label(frame, text='Please enter the path of the py file').grid(row=0, padx=4)
moduel_path = StringVar()
entry_0 = Entry(frame, width=50, textvariable=moduel_path)
entry_0.grid(row=1, padx=4)

Label(frame, text='Please enter the name of hashrate distribution file').grid(row=2, padx=4)

hash_path = StringVar()
entry_1 = Entry(frame, width=50, textvariable=hash_path)
entry_1.grid(row=3, padx=4)

Button(frame, text='Submit', command=print_path_hash).grid(row=3, sticky=E, padx=4)

# get the path for the carbon dioxide
carbon_path = StringVar()
Label(frame, text='Please enter the name of carbon dioxide file').grid(row=4, padx=4)
entry_2 = Entry(frame, width=50, textvariable=carbon_path)
entry_2.grid(row=5, padx=4)
Button(frame, text='Submit', command=print_path_carbon).grid(row=5, sticky=E, padx=4)

Button(frame, text='Calculate', command=calculate_function).grid(row=7, padx=4)

frame.pack()
root.mainloop()
