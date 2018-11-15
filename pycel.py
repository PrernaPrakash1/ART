# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 20:16:56 2018

@author: prerna.prakash
"""

import pandas as pd
import time
import os

def timeCheck() :
    return time.time()

def timeMeasure(starttime,endtime) :
    timetaken = endtime-starttime
    print("Time Taken in Seconds :",timetaken)
    
def saveExcel(FileName,Sheetname,df) :
    print(FileName)
    writer = pd.ExcelWriter(FileName,engine = 'xlsxwriter')
    df.to_excel(writer,index = False)
    writer.save()
    #print("Your File has been saved.")
  
def setUpConfigFile(name) :
    listOfConfigDetails = []
    cwd = os.getcwd()
    print(cwd+"\\"+name)
    fobj = open(cwd+"\\"+name)   
    for line in fobj:
        listOfConfigDetails.append(line.rstrip())
    return listOfConfigDetails

def saveExcelWithIndex(FileName,Sheetname,df) :
    print(FileName)
    writer = pd.ExcelWriter(FileName,engine = 'xlsxwriter')
    df.to_excel(writer,index = True)
    writer.save()
    print("Your File has been saved.")

def vlookup(dfbase,dfcopyfrom,DfBaseElement,DfCopyFromeElement,listofElements,prefix) :
    print("Applying Vlookup.")
    i = 0
    for each in dfbase[DfBaseElement] :
        j = 0
        for feach in dfcopyfrom[DfCopyFromeElement]:          
            if str(each) in str(feach) :
                for preach in listofElements :               
                    dfbase.at[i,prefix+preach] = dfcopyfrom.at[j,preach]
                break
                
            j = j+1
        i = i+1
    return dfbase 

def mathching(col1,col2) :
    
    if str(col1) in str(col2) :
        return True
    if str(col1) == 'nan' :
        return True
    return False
"""
def vlookupMultipleConditions(dfbase,dfcopyfrom,DfBaseElement,BaseElementList,DfCopyFromeElement,CopyElementList,listofElements,prefix) :
    print("Applying Vlookup.")
    i = 0
    for each in dfbase[DfBaseElement] :
        j = 0
        for feach in dfcopyfrom[DfCopyFromeElement]:          
            if df.at[i,] == feach and :
                for preach in listofElements :               
                    dfbase.at[i,prefix+preach] = dfcopyfrom.at[j,preach]
                break
                
            j = j+1
        i = i+1
    return dfbase 
"""
def vlookupin(dfbase,dfcopyfrom,DfBaseElement,DfCopyFromeElement,listofElements) :
    i = 0
    for each in dfbase[DfBaseElement] :
        j = 0
        for feach in dfcopyfrom[DfCopyFromeElement]: 
            feach = str(feach)
            each = str(each)
            if feach in each :
                for preach in listofElements :    
                    dfbase.at[i,preach] = str(dfcopyfrom.at[j,preach])
                break
                
            j = j+1
        i = i+1
    return dfbase 

def vlookupine(dfbase,dfcopyfrom,DfBaseElement,DfCopyFromeElement,listofElements) :
    print("Applying Vlookup.")
    i = 0
    for each in dfbase[DfBaseElement] :
        j = 0
        for feach in dfcopyfrom[DfCopyFromeElement]: 
            feach = str(feach)
            each = str(each)
            if feach in each :
                for preach in listofElements : 
                    print(preach,dfbase.at[i,preach])
                    dfbase.at[i,preach] = str(dfcopyfrom.at[j,preach])
                break
                
            j = j+1
        i = i+1
    return dfbase 

def doExclude(df,column,name) :
    for each in name:
        df = df[df[column]!=each]
        df = df.reset_index(drop=True)
    return df

def onlyInclude(df,column,name) :
        df = df[df[column]==name]
        df = df.reset_index(drop=True)
        return df

def removeOrders(dfbase,dfdelete,DfBaseElement,DfDeleteElement) :
    
    count = 0
    for each in dfbase[DfBaseElement] :
        for feach in dfdelete[DfDeleteElement] :
            if each == feach :
                count = count +1
                dfbase = dfbase[dfbase.SIEBEL_NUM != feach]
    print("Number on Cancellation Orders Removed are",count)
    return dfbase 
    #for each in df1["Order No."] :
def takeInput(Question,ExpectedAnswer) :
    answer = input(Question)
    if answer != ExpectedAnswer:
        print("Ok then.")

def saveData (df):
    takeInput("Do you want to save this data","y")

def AddMachine(df) :
    pass

def DD(df,filepath) :
    
    dfnew = pd.read_excel(filepath,'Sheet2')
    vlookupine(df,dfnew,['ANALYSIS'],['ANALYSIS'],['DD'])
    return df
    
    