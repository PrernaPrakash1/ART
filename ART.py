# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 14:30:44 2018

@author: prerna.prakash
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 18:47:32 2018

@author: prerna.prakash
"""
import pandas as pd
import webbrowser
import pycel as py
import BillingTriage as BT
import OSMTriage as OT
import ExternalTriage as ET
import UIMTriage as UT
import mobileAge as ma
import prep as pr
import os
class ART :
    Billing = 0
    External = 0 
    Network = 0
    UIM = 0
    OSM = 0
    def main(self):
        self.listOfConfigFile = py.setUpConfigFile("ConfigForARTY.txt")
        self.dfMainReport = pd.read_excel(self.listOfConfigFile[3])
        print(self.listOfConfigFile[3])
        self.makeReport()
        self.browser()
        
        
    def makeReport(self) :

        dfTeamMap = pd.read_excel(self.listOfConfigFile[0],'Sheet1')
    
        self.dfMainReport = self.dfMainReport.reset_index(drop=True)
        p = pr.prep()
        p.addLocation(self.dfMainReport)
        p.NextTaskExpected(self.dfMainReport)
        self.dfMainReport = p.change(self.dfMainReport)
       # py.saveExcel(self.listOfConfigFile[2],"Sheet1",self.dfMainReport)
        py.saveExcel("C:\\Users\\prerna.prakash\\Desktop\\Input\\checkthis.xlsx","Sheet1",self.dfMainReport)
        self.dfMainReport=py.vlookupin(self.dfMainReport,dfTeamMap,'LAST_TASK','TASK',['TEAM'])
        MA =  ma.mobileAge(self.dfMainReport)
        self.dfMainReport = MA.Main()
        self.makeTriageSheet()
        
        
        self.makeTriage()
       # reportingData = R.Reporting(self.dfMainReport,self.EntireSheet)
       # reportingData.setUp()
       # reportingData.saveCount()
        

        
    
    def makeTriageSheet(self) :
        dfBillingTriage = pd.read_excel(self.listOfConfigFile[1],"Billing")
        dfOSMTriage = pd.read_excel(self.listOfConfigFile[1],"OSM")
        dfExternalTriage = pd.read_excel(self.listOfConfigFile[1],"External")
        dfUIMTriage = pd.read_excel(self.listOfConfigFile[1],"UIM")
        
        self.Billing =str(len(self.dfMainReport[(self.dfMainReport['TEAM']=='Billing')].index) )
        self.UIM =str(len(self.dfMainReport[(self.dfMainReport['TEAM']=='UIM')].index))
        self.OSM =str(len(self.dfMainReport[(self.dfMainReport['TEAM']=='OSM')].index))
        self.External =str(len(self.dfMainReport[(self.dfMainReport['TEAM']=='External')].index))
        self.Network =str(len(self.dfMainReport[(self.dfMainReport['TEAM']=='Network')].index))
        
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
        
        uim =  UT.UIMTriage(dfUIM)
        uim.Analysis(dfUIMTriage)


    def makeTriage(self) :
        
        cols = ['SIEBEL_NUM','CTN','ACCOUNT_NUMBER','LAST_TASK','CHANNEL','SHIPPING','ORDER_TYPE','ORDERTYPECODE','ORDER TYPECODE2','COLLECTED_DATE','ORDER_STATUS','SUBMIT_DATE','PAYMENT_TYPE','PORTDATE','SUBMIT_DATE_ONLY','ORDER_DATE_ONLY','DAYS_OPEN','AGE','REFERENCE_NUMBER','ORDER_SEQ_ID','CARTRIDGE_ID','NEXT_ACTION','CATEGORY','TASK_START_TIME','ERROR_MESSAGE1','ERROR_MESSAGE2','TASK_DESCRIPTION','TXN_REASON','PAC_CODE','DONOR_NO','DONOR_SP','RECIPIENT_NO','RECIPIENT_SP','DIVISION','PREVIOUSNUM','SHIPPINGDATE','PORTING_SLA','SHIPPING_SLA','ATTRIB_55','ATTRIB_60','IMSI','Iphone Order','OLD/NEW OSM','COLLECT_TO_STORE/DELIVER_TO_STORE','PRIORITY','NEW_SIM','OLD_SIM','Unnamed: 47','TEAM','Age','AgeTemp','AgeReq','Priority','ANALYSIS','ISSUE','LOCATION','Next Task']
        files = os.listdir(self.listOfConfigFile[2])
        dftemp1 = pd.read_excel(self.listOfConfigFile[4]+"\\Analysis.xlsx",'Sheet1')
        cwd =os.getcwd()
        print("Files in '%s': %s" % (cwd, files))
        files_xlsx = [f for f in files if f[-4:] == 'xlsx']
        df = pd.DataFrame()
        for f in files_xlsx:
            
            dftemp = pd.read_excel(self.listOfConfigFile[2]+"\\"+f)
            dftemp = dftemp[cols]
            df =df.append(dftemp)
        
        df = df.reset_index(drop=True)
        i = 0
        for each in df['ANALYSIS'] :
            j = 0
            for feach in dftemp1['ANALYSIS']: 
                feach = str(feach)
                each = str(each)
                if feach in each :
                   
                    df.at[i,'DeeDee'] = str(dftemp1.at[j,'DD'])
                   
                    
                j = j+1
            i = i+1
        
        #df =py.DD(df,self.listOfConfigFile[0])
        py.saveExcel(self.listOfConfigFile[4]+"\\ARTAnalysis.xlsx","Sheet1",df)


            
    def browser(self) :
        f = open('Report.html','w')
        message = """<!DOCTYPE html>
        <html>
        <head>
        <style>
        table, th, td {
            border: 1px solid black;text-align: center;
        }
        </style>
        </head>
        <body>
        <h1> ART REPORTING</h1> 
        <h2>TEAM-WISE DISTRIBUTION OF ORDERS</h2>
        
        <table id = "ARTBOX">
          <tr>
            <th>TEAM</th>
            <th>COUNT</th>
          </tr>
          <tr>
            <td> EXTERNAL</td>
            <td>"""+self.External+"""</td>
          </tr>
          <tr>
            <td>UIM</td>
            <td>"""+self.UIM+"""</td>
          </tr>
          <tr>
            <td>OSM</td>
            <td>"""+self.OSM+"""</td>
          </tr>
            <td>BILLING</td>
            <td>"""+self.Billing+"""</td>
          </tr>
        </table>
        
        </body>
        </html>"""
        
        f.write(message)
        f.close()
        
        webbrowser.open_new_tab('Report.html')
            
art = ART()
art.main()