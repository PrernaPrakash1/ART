# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 14:41:41 2018

@author: prerna.prakash
"""
import pandas as pd
import pycel as py 
class mobileAge() :
    def __init__(self,dfMain) :
        self.dfMain = dfMain
        
        self.TaskToExclude = ['CompleteShippingFunctionExitPointTask','CompleteShippingFunctionSITask','InitiateShippingFunctionTETask.manualTask','SettlePaymentFunctionFalloutRecoverTask','InitiateShippingFunctionSITask']
        self.HP = ['Retail Shop','IVR','COUK']
        self.SLP = ['Collections Barring','Back Office Disconnection','Credit Bar','OPD','VELTI','Back Office Automation']
        self.Category = ['Activation','Regrade','Box Order','Change','Regrade','Disconnect']
        
    def Main(self) :
        self.dfMain = self.RemovePortDateNotPopulated()
        self.dfMain = py.doExclude(self.dfMain,'LAST_TASK',self.TaskToExclude)
        self.dfMain = self.dfMain.reset_index(drop=True)
        self.dfMain =py.doExclude(self.dfMain,'CATEGORY',['Valid Open'])
        self.dfMain = self.reset()
        #self.dfMain = py.removeOrders(self.dfMain,self.dfCancellation,"SIEBEL_NUM","Order No.")
        self.dfMain = self.reset()
        self.dfMain.COLLECTED_DATE = pd.to_datetime(self.dfMain.COLLECTED_DATE,dayfirst=True)
        self.dfMain.SUBMIT_DATE = pd.to_datetime(self.dfMain.SUBMIT_DATE,dayfirst=True)
        self.dfMain.PORTDATE = pd.to_datetime(self.dfMain.PORTDATE,dayfirst=True)
        self.dfMain = self.reset()
        self.dfMain =  self.Age('SUBMIT_DATE','COLLECTED_DATE','PORTDATE')
        self.dfMain = self.reset()
        self.dfMain= self.AgeReq()
        self.dfMain = self.reset()
        self.dfMain = self.SetPriority(self.HP,self.SLP,self.Category)     
        return self.dfMain


    def reset(self) :
        self.dfMain = self.dfMain.reset_index(drop=True)
        return self.dfMain
    

    #for each in df1["Order No."] :
        
    def RemovePortDateNotPopulated(self) :
       i = 0
       for each in self.dfMain['SIEBEL_NUM'] :          
            if self.dfMain.at[i,'ORDER_TYPE'] == 'Port_In' or self.dfMain.at[i,'ORDER_TYPE'] == 'Port_Out':
                if not self.dfMain.at[i,'PORTDATE'] :
                    
                    print(each,"is a porting Order but PortDate is not populated")
                    self.dfMain = self.dfMain[self.dfMain['SIEBEL_NUM']!= each]
            i = i+1  
       return self.dfMain
    
    def Age(self,SubmitDate,CollectedDate,PortDate) :
        i = 0 
        for each in self.dfMain['SIEBEL_NUM'] :      
            if self.dfMain.at[i,'ORDER_TYPE'] == 'Port_In' or self.dfMain.at[i,'ORDER_TYPE'] == 'Port_Out':
                if not self.dfMain.at[i,'PORTDATE'] :
                    self.dfMain = self.dfMain[self.dfMain['SIEBEL_NUM']!= each]
                else :
                    self.dfMain.at[i,'Age'] = (self.dfMain.at[i,CollectedDate]-self.dfMain.at[i,PortDate]).days 
            else :
                self.dfMain.at[i,'Age'] = (self.dfMain.at[i,CollectedDate]-self.dfMain.at[i,SubmitDate]).days
        #df['Age'] = ((df['COLLECTED_DATE']-df['SUBMIT_DATE']).seconds)//3600
            i = i+1
            
        return self.dfMain
    
    def AgeReq(self) :
        i =0
        
        for each in self.dfMain['SIEBEL_NUM'] :
            self.dfMain.at[i,'AgeTemp'] =  ((self.dfMain.at[i,'COLLECTED_DATE']-self.dfMain.at[i,'SUBMIT_DATE']).seconds)//3600
            AgeTemp =  ((self.dfMain.at[i,'COLLECTED_DATE']-self.dfMain.at[i,'SUBMIT_DATE']).seconds)//3600
            if self.dfMain.at[i,'Age']< 0 :
                 self.dfMain.at[i,'AgeReq'] = 'PortDate is Today'           
            elif AgeTemp < 12 and self.dfMain.at[i,'Age']<= 0:
                self.dfMain.at[i,'AgeReq'] = 'Not Backlog'
            elif  self.dfMain.at[i,'Age'] < 3:
                self.dfMain.at[i,'AgeReq'] = '12+'
            elif self.dfMain.at[i,'Age'] <7 and self.dfMain.at[i,'Age'] >=3 :
                self.dfMain.at[i,'AgeReq'] = '3+'            
            elif self.dfMain.at[i,'Age'] >=7 :
                self.dfMain.at[i,'AgeReq'] = '7+'
            i = i+1
        return self.dfMain    
    
    def SetPriority(self,HP,SLP,Category) :
        i=0
    
        for each in self.dfMain['SIEBEL_NUM'] :
            
            self.dfMain.at[i,'Priority'] = "Low Priority"
            Orderlist= str(self.dfMain.at[i,'ORDER TYPECODE2']).split(",")
            if self.dfMain.at[i,"CHANNEL"] == 'Retail Shop' :
                if self.dfMain.at[i,'ORDER_TYPE'] in ("Activation","Regrade") :
                    self.dfMain.at[i,'Priority'] ="Retail"
            if self.dfMain.at[i,"CHANNEL"] not in SLP :
                if "RB" in Orderlist :
                    if self.dfMain.at[i,'ORDER_TYPE'] == 'Change' :
                        self.dfMain.at[i,'Priority'] = "Remove Bar"
            if self.dfMain.at[i,"CHANNEL"] in('IVR','COUK') :
            
                if self.dfMain.at[i,'ORDER_TYPE'] in Category :
                    self.dfMain.at[i,'Priority']= "IVR and COUK"
         
            if "SS" in Orderlist :
                self.dfMain.at[i,'Priority'] = "Sim Swap"
            
            if self.dfMain.at[i,"CHANNEL"] in SLP :
                self.dfMain.at[i,'Priority'] ="Do not Include"
        
        
            
            if self.dfMain.at[i,'ORDER_TYPE'] in ['Port_In','Port_Out']:
                self.dfMain.at[i,'Priority'] = 'Porting Order'
            i = i+1
        return self.dfMain




    



