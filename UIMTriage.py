# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 15:34:46 2018

@author: prerna.prakash
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 13:00:15 2018

@author: prerna.prakash
"""

import pandas as pd
import pycel as py

class UIMTriage :
    def __init__(self,UIMTriage):
        self.UIM = UIMTriage
        self.listOfConfigFile = py.setUpConfigFile("ConfigForARTY.txt")
   


   
    def defineAnalysis(self,dfTriage) :
        for index,row in self.UIM.iterrows() :
            for sindex,rows in dfTriage.iterrows() :
                  if py.mathching(dfTriage.at[sindex,'LAST_TASK'],self.UIM.at[index,'LAST_TASK']) & py.mathching(dfTriage.at[sindex,'ERROR_MESSAGE1'],self.UIM.at[index,'ERROR_MESSAGE1']) & py.mathching(dfTriage.at[sindex,'ORDERTYPECODE'],self.UIM.at[index,'ORDERTYPECODE'])& py.mathching(dfTriage.at[sindex,'ORDER_TYPE'],self.UIM.at[index,'ORDER_TYPE']) & py.mathching(dfTriage.at[sindex,'SHIPPING'],self.UIM.at[index,'SHIPPING'])& py.mathching(dfTriage.at[sindex,'ORDER TYPECODE2'],self.UIM.at[index,'ORDER TYPECODE2']) & py.mathching(dfTriage.at[sindex,'COLLECT_TO_STORE/DELIVER_TO_STORE'],self.UIM.at[index,'COLLECT_TO_STORE/DELIVER_TO_STORE']) :
                 #if py.mathching(dfTriage.at[sindex,'Task Name'],self.External.at[index,'LAST_TASK']) :    
                    #print(dfTriage.at[index,'Task Name'],self.External.at[sindex,'LAST_TASK'])
                    
                    self.UIM.at[index,'ANALYSIS'] = str(dfTriage.at[sindex,'Analysis'])
                    self.UIM.at[index,'ISSUE'] = str(dfTriage.at[sindex,'ISSUE'])
                    self.UIM.at[index,'Next Action'] = str(dfTriage.at[sindex,'Next Action'])
                    self.UIM.at[index,'Next Action Team'] = str(dfTriage.at[sindex,'Next Action Team'])
                    self.UIM.at[index,'RCA'] = str(dfTriage.at[sindex,'RCA'])
                    self.UIM.at[index,'Remedial Action'] = str(dfTriage.at[sindex,'Remedial Action'])
                                           #self.Billing.at[i,'NEXT ACTION'] = str(dfTriage.at[j,'Comments'])
                    break             
     
        return   self.UIM


    def Analysis(self,dfTriage) :
        self.UIM=  self.defineAnalysis(dfTriage)
        py.saveExcel(self.listOfConfigFile[2]+"\\UIMTriage.xlsx","Sheet1",self.UIM)
        return self.UIM