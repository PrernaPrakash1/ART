# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 15:15:38 2018

@author: prerna.prakash
"""
import pandas as pd
import pycel as py
import ReportingModule as rm
import os

class Reporting:
    def __init__(self,df,dataTotal):
        self.dataEntire = dataTotal
        self.mainreport = df
        self.mainreport.COLLECTED_DATE = pd.to_datetime(self.mainreport.COLLECTED_DATE,dayfirst=True)
        self.mainreport.SUBMIT_DATE = pd.to_datetime(self.mainreport.SUBMIT_DATE,dayfirst=True)
        self.mainreport.PORTDATE = pd.to_datetime(self.mainreport.PORTDATE,dayfirst=True)
        self.reportTime = df.at[2,'COLLECTED_DATE']
    
    def setUp(self) :

      self.mainreport=  rm.removePortDateNotPopulated(self.mainreport)
      self.mainreport =rm.age(self.mainreport,'SUBMIT_DATE','COLLECTED_DATE','PORTDATE')
      self.mainreport= rm.ageReq(self.mainreport)
    
    def saveCount(self):
        cwd = os.getcwd()
        TeamDict = rm.extractRelevantFromDf(self.mainreport,'TEAM')
        TeamDict['DateTime'] = self.reportTime
        dfTeam = pd.DataFrame(data=TeamDict,index = [0])  
        dfsaveit = pd.read_excel(cwd+"\\HistoricData.xlsx","Sheet1")
        dfsaveit = pd.concat([pd.DataFrame(dfTeam), dfsaveit], ignore_index=True)
        py.saveExcel(cwd+"\\HistoricData.xlsx","Sheet1",dfsaveit)
        TeamDict = rm.extractRelevantFromDf(self.mainreport,'LAST_TASK')
        TeamDict['DateTime'] = self.reportTime
        dfTeam = pd.DataFrame(data=TeamDict,index = [0])  
        dfsaveit = pd.read_excel(cwd+"\\HistoricDataTask.xlsx","Sheet1")
        dfsaveit = pd.concat([pd.DataFrame(dfTeam), dfsaveit], ignore_index=True)
        py.saveExcel(cwd+"\\HistoricDataTask.xlsx","Sheet1",dfsaveit)
    
"""    
    def saveOrderDetail(self) :
        for each in dfTotal :
            if 
        
 """       
        
    
        