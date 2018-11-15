# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 18:50:20 2017

@author: prerna.prakash
"""

import pandas as pd
import os
import pycel as py
import BillingTriage as BT
import OSMTriage as OT
import ExternalTriage as ET
import Reporting as R

class ARTY :
    def __init__(self,df,dfEntire):
        self.dfMainReport = df
        self.EntireSheet = dfEntire
        self.listOfConfigFile = py.setUpConfigFile("ConfigForARTY.txt")
        
        
        
    def makeReport(self) :

        dfTeamMap = pd.read_excel(self.listOfConfigFile[2],'Sheet1')
        self.dfMainReport = self.dfMainReport.reset_index(drop=True)
        py.vlookup(self.dfMainReport,dfTeamMap,'LAST_TASK','TASK',['TEAM'],'')
        reportingData = R.Reporting(self.dfMainReport,self.EntireSheet)
        reportingData.setUp()
        reportingData.saveCount()
        
    
    def makeTriageSheet(self) :
        dfBillingTriage = pd.read_excel(self.listOfConfigFile[3],"Billing")
        dfOSMTriage = pd.read_excel(self.listOfConfigFile[3],"OSM")
        dfExternalTriage = pd.read_excel(self.listOfConfigFile[3],"External")

        self.dfMainReport = self.dfMainReport.reset_index(drop=True)
        
        dfBRM = py.onlyInclude(self.dfMainReport,'TEAM','Billing')

        dfUIM = py.onlyInclude(self.dfMainReport,'TEAM','UIM')

        dfOSM = py.onlyInclude(self.dfMainReport,'TEAM','OSM')

        dfNetwork = py.onlyInclude(self.dfMainReport,'TEAM','Network')

        dfExternal = py.onlyInclude(self.dfMainReport,'TEAM','External')

        br =  BT.BillingTriage(dfBRM)
        br.Analysis(dfBillingTriage)

        osm =  OT.OSMTriage(dfOSM)
        osm.Analysis(dfOSMTriage)
        
        external =  ET.ExternalTriage(dfExternal)
        external.Analysis(dfExternalTriage)

    def makeTriage(self) :
        userreply = input("Do you want to make Triage Sheet?")
        if userreply == 'y' :
          self.makeTriageSheet()
        else :
            print("OK Then")
            
        


