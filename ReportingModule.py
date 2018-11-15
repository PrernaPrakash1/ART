# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 15:13:54 2018

@author: prerna.prakash
"""
import pandas as pd
from datetime import time

def removePortDateNotPopulated(df) :
   i = 0
   for each in df['SIEBEL_NUM'] :          
        if df.at[i,'ORDER_TYPE'] == 'Port_In' or df.at[i,'ORDER_TYPE'] == 'Port_Out':
            if not df.at[i,'PORTDATE'] :
                print(each,"is a porting Order but PortDate is not populated")
                df = df[df['SIEBEL_NUM']!= each]
        i = i+1  
   return df
def age(df,SubmitDate,CollectedDate,PortDate) :
    i = 0 
    for each in df['SIEBEL_NUM'] :        
        if df.at[i,'ORDER_TYPE'] == 'Port_In' or df.at[i,'ORDER_TYPE'] == 'Port_Out':
            df.at[i,'Age'] = (df.at[i,CollectedDate]-df.at[i,PortDate]).days -1
        else :
            df.at[i,'Age'] = (df.at[i,CollectedDate]-df.at[i,SubmitDate]).days
    #df['Age'] = ((df['COLLECTED_DATE']-df['SUBMIT_DATE']).seconds)//3600
        i = i+1
    return df

def ageReq(df) :
    i =0
    
    for each in df['SIEBEL_NUM'] :
        df.at[i,'AgeTemp'] =  ((df.at[i,'COLLECTED_DATE']-df.at[i,'SUBMIT_DATE']).seconds)//3600
        AgeTemp =  ((df.at[i,'COLLECTED_DATE']-df.at[i,'SUBMIT_DATE']).seconds)//3600
        if df.at[i,'Age']< 0 :
             df.at[i,'AgeReq'] = 'PortDate is Today'           
        elif AgeTemp < 12 and df.at[i,'Age']<= 0:
            df.at[i,'AgeReq'] = 'Not Backlog'
        elif  df.at[i,'Age'] < 3:
            df.at[i,'AgeReq'] = '12+'
        elif df.at[i,'Age'] <7 and df.at[i,'Age'] >=3 :
            df.at[i,'AgeReq'] = '3+'            
        elif df.at[i,'Age'] >=7 :
            df.at[i,'AgeReq'] = '7+'
        i = i+1
    df =df.drop(['AgeTemp'], axis=1)
    return df    

def setPriority(df,HP,SLP,Category) :
    i=0

    for each in df['SIEBEL_NUM'] :
        
        df.at[i,'Priority'] = "Low Priority"
        Orderlist= str(df.at[i,'ORDER TYPECODE2']).split(",")
        if df.at[i,"CHANNEL"] == 'Retail Shop' :
            if df.at[i,'ORDER_TYPE'] in ("Activation","Regrade") :
                df.at[i,'Priority'] ="Retail"
        if df.at[i,"CHANNEL"] not in SLP :
            if "RB" in Orderlist :
                if df.at[i,'ORDER_TYPE'] == 'Change' :
                    df.at[i,'Priority'] = "Remove Bar"
        if df.at[i,"CHANNEL"] in('IVR','COUK') :
        
            if df.at[i,'ORDER_TYPE'] in Category :
                df.at[i,'Priority']= "IVR and COUK"
     
        if "SS" in Orderlist :
            df.at[i,'Priority'] = "Sim Swap"
        
        if df.at[i,"CHANNEL"] in SLP :
            df.at[i,'Priority'] ="Do not Include"
    
    
        
        if df.at[i,'ORDER_TYPE'] in ['Port_In','Port_Out']:
            df.at[i,'Priority'] = 'Porting Order'
        i = i+1
    return df

def extractRelevantFromDf(df,column) :
    dfCount = df.groupby(column).size()
    dfCount = dfCount.to_dict()

    return dfCount
def timeBetween(now) :

    if time(0,00) <= now and now  <= time(4,00):
        return 1  
    elif time(4,00) <= now and now  <= time(8,00):
        return 2
    elif time(8,00) <= now and now  <= time(12,00):
        return 3
    elif time(12,00) <= now and now  <= time(16,00):
        return 4
    elif time(16,00) <= now and now  <= time(20,00):
        return 5
    elif time(20,00) <= now and now  <= time(23,59):
        return 6
    else :
        return False
    