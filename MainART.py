# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 18:48:40 2018

@author: prerna.prakash
"""
import pandas as pd
import os
from datetime import datetime,timedelta
from ReportingModule import timeBetween
import pycel as py
import ARTY



class MainART :
    def main():
        listOfConfigFile = py.setUpConfigFile("ConfigForARTY.txt")
        historicData = pd.read_excel(listOfConfigFile[0])
        files = os.listdir(listOfConfigFile[1])
        cwd = os.getcwd()
        print("Files in '%s': %s" % (cwd, files))
        files_xlsx = [f for f in files if f[-4:] == 'xlsx']
        for f in files_xlsx:
            data = pd.read_excel(listOfConfigFile[1]+"\\"+f, 'Sheet1')
            col = data.at[1,'COLLECTED_DATE']
            print(col)
            col = datetime.strptime(col, '%d-%m-%Y %H:%M:%S')
            col = col + timedelta(hours = 8)
            datenow = col.date()  
            timenow = col.time()
            timeSlot = timeBetween(timenow)
            dataEntire = data
            data = py.doExclude(data,'CATEGORY',["Valid Open"]) 
            nonValidCount = len(data.index)
            a = ARTY.ARTY(data,dataEntire)
            a.makeReport()
            a.makeTriage()
            """
            if datenow in historicData.Date :
                historicData.at[datenow,timeSlot] = nonValidCount

            else :
                
                historicData.append({'Date':datenow,1:0,2:0,3:0,4:0,5:0,6:0},ignore_index = True)
                historicData.at[datenow,timeSlot] = nonValidCount
                print(historicData)
        py.saveExcelWithIndex(listOfConfigFile[0],"Sheet1",historicData) 
        """
    main()  