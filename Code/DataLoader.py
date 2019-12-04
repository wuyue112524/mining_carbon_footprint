#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import datetime




def read_data(path,na_values=''):
    data = pd.read_csv(path,na_values=na_values)
    return data


def merge_country_code(dataframe,code_name_1='./Data/Country_code_BTC.csv'):
        '''merge the dataframe with country code
        :pars: dataframe, a dataframe to merge the country code
        :pars: code_name_1: the internal file which contains a country code and country name
        :pars: code_name_2: another internal file which contains a country code and country name
        
        Returns: a merged dataframe with a new column named Country_Code
        
        Note:Please use {Country_Name} for the country column, and use {Code} for the code column.Case sensitive.
        '''
        #merge the code using country name 
        
        code_1 = pd.read_csv(code_name_1)
        dataframe = dataframe.merge(code_1,how='left',on='Country_Name') 
        return dataframe


class MiningHashrate():
    
    def __init__(self,dataframe):
    
        '''This function reads data into a dataframe. The input data should be csv file, and should have the following six columns and the
        name should be the same.Note the name is case sensitive.
    
        Month:Note Month data should use {YYYYMM} only ex. 201904 
        Country_Name
        Region
        Daily_Hashrate
        Working_Days
        Pool
        
        Argument:
        path: the path for the csv file which should be a string
        na-values: NA values are represented in what values in the file, the default is ''
        '''
        self.df = dataframe
        self.region = self.df['Region']
        self.daily_hash = self.df['Daily_Hashrate']
        self.working_days = self.df['Working_Days']  
        self.pool = self.df['Pool']
        self.country = self.df['Country_Name']
        
    def parsing_the_date(self,format='%Y%m'):
        '''This function aims to create a string variable that can be grouped in the future
        '''
        self.df['Month'] = pd.to_datetime(self.df['Month'],format=format)
        new_df = self.df
        return new_df

    def drop_missing_values(self):
         
        '''
        Drop the row if there is a missing value in any column
        '''
        print('There were %d observations before droping missing value' %self.df.shape[0])
        
        self.df = self.df.dropna()
        new_df = self.df
        
        print('There were %d observations after droping missing value' %self.df.shape[0])
        
        return new_df
    
    def hash_file_merge_code(self,code_name_1='./Data/Country_code_BTC.csv'):
        self.df = merge_country_code(self.df,code_name_1)
 
        return self.df
    
    def monthly_average_sum(self):
        
        #Create monthly average = daily hashrate * Working days  
        self.df['Monthly_Average'] = self.working_days * self.daily_hash
        
        
        #add up all the pool for a specific region
        sub_df = self.df[['Month','Country_Name','Region','Pool','Code','Monthly_Average']]
        new_df = sub_df.groupby(['Month','Country_Name','Region','Code']).sum()
        new_df.reset_index(inplace = True)
        
        return new_df
    
    def monthly_share(self):

       	#Create a monthly sum of daily hashrate, rename it as Monthly_Sum
        sum_df = self.df[['Month','Monthly_Average']].groupby('Month').sum()
        name = list(sum_df.columns)
        name = ['Monthly_Sum']
        sum_df.columns = name
        #print(self.df.shape)
        
        #Merge two datasets
        
        self.df = self.df.merge(sum_df, how ='left',on='Month')
        self.df['Monthly_Share'] = self.df['Monthly_Average']/ self.df['Monthly_Sum']
        #print(self.df.shape)
        return self.df

    def merge_the_factor(self,filepath):
        '''
        merge the carbon emission factor into the dataframe
        :par: filepath - the filepath for the carbon emission factor  
        
        Note: the column name for the coutry should be {Country_Name}, which is case sensitive. 
        '''
        df_fac = pd.read_csv(filepath)
        self.df = self.df.merge(df_fac,how = 'left',on = 'Country_Name')
        return self.df


    def calcualte_weighted_average(self):
        '''
        Calculate the weighted carbon average factor 
        Return: the dataframe and a weighted sum of carbon emission factor  
        Note: the column name for the carbon factor file should be {Emission_Factor}, which is case sensitive
        
        '''
        
        self.df['Weighted_CO2_Factor'] = self.df['Monthly_Share']* self.df['Emission_Factor']
        
        sub_df = self.df[['Month','Weighted_CO2_Factor']]
        sub_df = sub_df.groupby('Month').sum()
        annual_factor = round(sub_df['Weighted_CO2_Factor'].sum()/sub_df.shape[0],4)
        sub_df['annual_factor']=annual_factor
        return  self.df, sub_df, annual_factor
    
    
    def write_the_file(self,dataframe,filename):
        
        try:
            dataframe.to_csv(filename)
            print('The file {name} has been successully created'.format(name=filename))
            
        except Exception as e:
            print('The file cannot be created due to the error'+str(e))
    
    def function_wrapper(self,filepath,format='%Y%m',filename='./Results/distribution.csv',emi_name='./Results/carbon_factor.csv',code_name_1='./Data/Country_code_BTC.csv'):
        new_df = self.parsing_the_date(format)
        new_df = self.drop_missing_values()
        new_df = self.hash_file_merge_code(code_name_1)
        new_df = self.monthly_average_sum()
        new_df = self.monthly_share()
        new_df = self.merge_the_factor(filepath)
        new_df, sub_df,annual_factor = self.calcualte_weighted_average()
        print('The weighted average carbon emission factor is {number}'.format(number=annual_factor))
        self.write_the_file(new_df,filename)
        self.write_the_file(sub_df,emi_name)
        print(sub_df)
