# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 13:00:15 2018

@author: prerna.prakash
"""

import pandas as pd
import pycel as py

class ExternalTriage :
    def __init__(self,dfExternal):
        self.External = dfExternal
        self.listOfConfigFile = py.setUpConfigFile("ConfigForARTY.txt")
   


   
    def defineAnalysis(self,dfTriage) :
        for index,row in self.External.iterrows() :
            for sindex,rows in dfTriage.iterrows() :
                 if py.mathching(dfTriage.at[sindex,'Task Name'],self.External.at[index,'LAST_TASK']) & py.mathching(dfTriage.at[sindex,'Error'],self.External.at[index,'ERROR_MESSAGE1']) & py.mathching(dfTriage.at[sindex,'CHANNEL'],self.External.at[index,'CHANNEL']) :
                 #if py.mathching(dfTriage.at[sindex,'Task Name'],self.External.at[index,'LAST_TASK']) :    
                    #print(dfTriage.at[index,'Task Name'],self.External.at[sindex,'LAST_TASK'])
                    self.External.at[index,'ANALYSIS'] = str(dfTriage.at[sindex,'Analysis'])
                    self.External.at[index,'ISSUE'] = str(dfTriage.at[sindex,'ISSUE'])
                    
                        #self.Billing.at[i,'NEXT ACTION'] = str(dfTriage.at[j,'Comments'])
                    break             
     
        return   self.External


    def Analysis(self,dfTriage) :
        self.External=  self.defineAnalysis(dfTriage)
        py.saveExcel(self.listOfConfigFile[2]+"\\ExternalTriage.xlsx","Sheet1",self.External)
        return self.External
    

   

