# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 18:45:49 2018

@author: prerna.prakash
"""

import pandas as pd
import random
import pycel as py

class prep() :
    def __init__(self):
        pass
        
    def change(self,df) :
        #df = self.changeOrderNo(df)
        df = self.replaceFone(df)
        df = self.addLocation(df)
        df = self.NextTaskExpected(df)
        return df
        
    def changeOrderNo(self,df) :
        i = 0
        for each in df['SIEBEL_NUM'] :
            df.at[i,'SIEBEL_NUM'] = "Order No. "+str(i)
            i = i+1
        return df
    

    def addLocation(self,df) :
        df['LOCATION'] = ''
        locationList = ['Bradgate Mall','Fairhill Shopping Centre','Marygate','Castle Court Shopping Centre','Oracle Centre Reading','High Street Chippenham','St Marys Street','Mather Way Salford','Bakers Lane Lichfield','Broadmead Bristol','34 Clumber Street']
        i = 0
        for each in df['SIEBEL_NUM'] :
            if df.at[i,'CHANNEL'] in ['Retail Sites','Telesales','Accord','Autilia'] :
                
                df.at[i,'LOCATION'] = random.choice(locationList)
            i = i+1
        
        return df
    
    def NextTaskExpected(self,df) :
        df['Next Task'] = ''
        TaskList = ['FulfillBillingFalloutRecoverTask','PMS020_ASAP_FailEventAnalyze','']
        i = 0
        for each in df['SIEBEL_NUM'] :
            if df.at[i,'LAST_TASK'] in ['UIM_GetServiceInfo_BE','SyncCustomerSITask','PMS020.CUR_UpdateOnCUR_BE'] :
                
                df.at[i,'Next Task'] = random.choice(TaskList)
            i = i+1
        
        return df
                
       
    
    def replaceFone(self,df) :
        
        df = df.replace("Call Centre","Call Center")
        df = df.replace("Chordiant","Accord")
        df = df.replace("Retail Shop","Retail Sites")
        df = df.replace("eShop","Shopprix")
        df = df.replace("FMW","Middleware")
        df = df.replace("COUK","Online 1")
        df = df.replace("TalkMobile","App1")
        df = df.replace("CPW","Warehouse")
        df = df.replace("Channels","Backend")
        df = df.replace("Back Office Disconnection","BACKRUN1")
        df = df.replace("Youth eCare","Online 2")
        df = df.replace("Collections Barring","Barring Channel 1")
        df = df.replace("Back Office Automation","BACKRUN2")
        df = df.replace("TIL","Ilayer")
        df = df.replace("PONTIS","Offer1")
        df = df.replace("OPD","Offer2")
        df = df.replace("UC4","Autilia")
        df = df.replace("VELTI","Loyalty")
        df = df.replace("Credit Bar","Barring Channel 2")
        df = df.replace("Youth eShop","Shopprix2")
        df = df.replace("2020","Telesales")
        df = df.replace("Administration Accenture","Administration office")
        df = df.replace("VISPL Webchat","Webchat")
        df = df.replace("Webchat Care - PAYM & Tech India - VISPL","WebCare")
        df = df.replace("NewCo Orders","Stacorders")
        df = df.replace("Siebel Administration","SBLadministration")
        df = df.replace("Webchat Care - PAYM & Tech India - FIS","Webcare1")
        df = df.replace("TCS - UK","TCS – UK")
        df = df.replace("SMB Care Egypt","SMB Care")
        df = df.replace("SMB TSAR IB Telesales Stoke","SMB TSAR IB Telesales")
        df = df.replace("Error Handling - VISPL","Error Handling")
        df = df.replace("Staff Accounts VISPL","Staff Accounts ")
        df = df.replace("SMB TSAR OB Telesales Stoke","SMB TSAR OB Telesales ")
        df = df.replace("eShop","Shopprix")
        df = df.replace("VOXI Customer Relations and Porting","Customer Relations and Porting")
        df = df.replace("VF Red Brand","Red Brand")
        df = df.replace("SMB TSAR IB Upgrades Belfast","SMBTSAR")
        df = df.replace("Enterprise Credit admin India","EnterpriseCredit")
        df = df.replace("Carphone Warehouse","Warehouse")
        return df



        