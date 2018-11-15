# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 20:23:45 2018

@author: prerna.prakash
"""

import pandas as pd
import pycel as py

class OSMTriage :
    def __init__(self,dfOSM):
        self.OSM = dfOSM
        self.listOfConfigFile = py.setUpConfigFile("ConfigForARTY.txt")
   


   
    def defineAnalysis(self,dfTriage) :
        self.OSM = py.vlookup(self.OSM,dfTriage,"LAST_TASK","Category",['ANALYSIS','Next Action','Next Action Team','Status','RCA','Remedial Action','ISSUE'],"")       
        return   self.OSM 


    def Analysis(self,dfTriage) :
        self.OSM =  self.defineAnalysis(dfTriage)
        py.saveExcel(self.listOfConfigFile[2]+"\\OSMTriage.xlsx","Sheet1",self.OSM)
        return self.OSM
