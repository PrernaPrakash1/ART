# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 20:21:55 2018

@author: prerna.prakash
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:26:15 2018

@author: prerna.prakash
"""
import pandas as pd
import pycel as py
import numpy as ny

class BillingTriage :
    def __init__(self,dfBilling):

        self.Billing = dfBilling
        self.listOfConfigFile = py.setUpConfigFile("ConfigForARTY.txt")
   

    def findErrorStrings(self,dfTriage) : 

       self.Billing =  py.vlookupin(self.Billing,dfTriage,'ERROR_MESSAGE1','Field',['Field'])
       self.Billing =  py.vlookupin(self.Billing,dfTriage,'ERROR_MESSAGE1','OpCode',['OpCode']) 
       self.Billing =  py.vlookupin(self.Billing,dfTriage,'ERROR_MESSAGE1','ErrMsg',['ErrMsg']) 
       self.Billing =  py.vlookupin(self.Billing,dfTriage,'ERROR_MESSAGE1','ErrStr',['ErrStr'])  
       
       self.Billing = self.defineAnalysis(dfTriage)
       
              
       return self.Billing
   
    def defineAnalysis(self,dfTriage) :

        for each in self.Billing['ERROR_MESSAGE1'] :
            i = 0
            for each in self.Billing['ERROR_MESSAGE1'] :
                j = 0
                for feach in dfTriage['STRCAT']: 
                    if (self.Billing.at[i,'OpCode'] == dfTriage.at[j,'OpCode']) & (self.Billing.at[i,'ErrMsg'] == dfTriage.at[j,'ErrMsg']) & (self.Billing.at[i,'ErrStr'] == dfTriage.at[j,'ErrStr'])  & (self.Billing.at[i,'Field'] == dfTriage.at[j,'Field']):
                        self.Billing.at[i,'ANALYSIS'] = str(dfTriage.at[j,'SOP to be Assigned'])
                        self.Billing.at[i,'ISSUE'] = str(dfTriage.at[j,'ISSUE'])
                        #self.Billing.at[i,'NEXT ACTION'] = str(dfTriage.at[j,'Comments'])
                        break             
                    j = j+1
                i = i+1
        i = 0        
        
        return   self.Billing 


    def Analysis(self,dfTriage) :

        self.findErrorStrings(dfTriage)
        self.Billing = self.Billing.fillna('')
        py.saveExcel(self.listOfConfigFile[2]+"\\BillingTriage.xlsx","Sheet1",self.Billing)
        return self.Billing


"""       
class UIMTriage :
    def __init(self)__ :
        

class OSMTriage :
    def __init(self)__ :
        
"""