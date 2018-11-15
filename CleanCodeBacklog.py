# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 19:10:54 2018

@author: prerna.prakash
"""

import pandas as pd
import time
import os
from datetime import timedelta
from ART import ART
import Sendmail as sm
def timecheck() :
    return time.time()

def timemeasure(starttime,endtime) :
    timetaken = endtime-starttime
    print("Time Taken in Seconds :",timetaken)
    
def saveExcel(FileName,Sheetname,df) :
    print(FileName)
    writer = pd.ExcelWriter(FileName,engine = 'xlsxwriter')
    df.to_excel(writer,index = False)
    writer.save()
    print("Your File has been saved.")
    
def SetUpConfigFile(name) :
    listOfConfigDetails = []
    cwd = os.getcwd()
    print(cwd)
    fobj = open(cwd+"\\"+name)   
    for line in fobj:
        listOfConfigDetails.append(line.rstrip())
    return listOfConfigDetails

def vlookup(dfbase,dfcopyfrom,DfBaseElement,DfCopyFromeElement,listofElements,prefix) :
    dfbase['TEAM'] = 'OSM'
    print("Applying Vlookup.Sit Back and Relax.Go get some soda")
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

def DoExclude(df,column,name) :
    for each in name:
        df = df[df[column]!=each]
    return df

def RemoveOrders(dfbase,dfdelete,DfBaseElement,DfDeleteElement) :
    
    count = 0
    for each in dfbase[DfBaseElement] :
        for feach in dfdelete[DfDeleteElement] :
            if each == feach :
                count = count +1
                dfbase = dfbase[dfbase.SIEBEL_NUM != feach]
    print("Number on Cancellation Orders Removed are",count)
    return dfbase 
    #for each in df1["Order No."] :
        
def RemovePortDateNotPopulated(df) :
   i = 0
   for each in df['SIEBEL_NUM'] :          
        if df.at[i,'ORDER_TYPE'] == 'Port_In' or df.at[i,'ORDER_TYPE'] == 'Port_Out':
            if not df.at[i,'PORTDATE'] :
                print(each,"is a porting Order but PortDate is not populated")
                df = df[df['SIEBEL_NUM']!= each]
        i = i+1  
   return df
def Age(df,SubmitDate,CollectedDate,PortDate) :
    i = 0 
    for each in df['SIEBEL_NUM'] :        
        if df.at[i,'ORDER_TYPE'] == 'Port_In' or df.at[i,'ORDER_TYPE'] == 'Port_Out':
            df.at[i,'Age'] = (df.at[i,CollectedDate]-df.at[i,PortDate]).days -1
        else :
            df.at[i,'Age'] = (df.at[i,CollectedDate]-df.at[i,SubmitDate]).days
    #df['Age'] = ((df['COLLECTED_DATE']-df['SUBMIT_DATE']).seconds)//3600
        i = i+1
    return df

def AgeReq(df) :
    i =0
    
    for each in df['SIEBEL_NUM'] :
        df.at[i,'AgeTemp'] =  ((df.at[i,'COLLECTED_DATE']-df.at[i,'SUBMIT_DATE']).seconds)//3600
        AgeTemp =  ((df.at[i,'COLLECTED_DATE']-df.at[i,'SUBMIT_DATE']).seconds)//3600
        if df.at[i,'Age']< 0 :
             df.at[i,'AgeReq'] = 'PortDate is Today'           
        elif AgeTemp < 12 and df.at[i,'Age']<= 0:
            df.at[i,'AgeReq'] = 'Not Backlog'
        elif  df.at[i,'Age'] < 3:
            df.at[i,'AgeReq'] = '12+'
        elif df.at[i,'Age'] <7 and df.at[i,'Age'] >=3 :
            df.at[i,'AgeReq'] = '3+'            
        elif df.at[i,'Age'] >=7 :
            df.at[i,'AgeReq'] = '7+'
        i = i+1
    return df    

def SetPriority(df,HP,SLP,Category) :
    i=0

    for each in df['SIEBEL_NUM'] :
        
        df.at[i,'Priority'] = "Low Priority"
        Orderlist= str(df.at[i,'ORDER TYPECODE2']).split(",")
        if df.at[i,"CHANNEL"] == 'Retail Shop' :
            if df.at[i,'ORDER_TYPE'] in ("Activation","Regrade") :
                df.at[i,'Priority'] ="Retail"
        if df.at[i,"CHANNEL"] not in SLP :
            if "RB" in Orderlist :
                if df.at[i,'ORDER_TYPE'] == 'Change' :
                    df.at[i,'Priority'] = "Remove Bar"
        if df.at[i,"CHANNEL"] in('IVR','COUK') :
        
            if df.at[i,'ORDER_TYPE'] in Category :
                df.at[i,'Priority']= "IVR and COUK"
     
        if "SS" in Orderlist :
            df.at[i,'Priority'] = "Sim Swap"
        
        if df.at[i,"CHANNEL"] in SLP :
            df.at[i,'Priority'] ="Do not Include"
    
    
        
        if df.at[i,'ORDER_TYPE'] in ['Port_In','Port_Out']:
            df.at[i,'Priority'] = 'Porting Order'
        i = i+1
    return df

def PrintStatements(df) :
   
    Counter = {}
    
    TotalBacklog =len(df[((df['AgeReq']=='Not Backlog') | (df['ORDER_TYPE']=='PortDate is Today')) & (df['Priority']!='Do not Include')].index)
    #print("Total 0-12+ count is",TotalBacklog)
    Counter['Total Backlog 0-12'] = TotalBacklog

    Porting =len(df[(df['Priority']=='Porting Order')  & ((df['AgeReq'] == '12+') | (df['AgeReq'] == '3+')|(df['AgeReq'] == '7+'))].index)
    #print("Porting Orders are",Porting)
    Counter['Porting'] = Porting
    
    Backlog =len(df[((df['AgeReq'] == '12+') | (df['AgeReq'] == '3+')|(df['AgeReq'] == '7+'))  & ((df['ORDER_TYPE']!='PortDate is Today') & (df['Priority']!='Do not Include'))].index)
    #print("Total Backlog count is",Backlog)
    Counter['Total Backlog'] = Backlog
    
    BacklogPriority =len(df[((df['AgeReq'] == '12+') | (df['AgeReq'] == '3+')|(df['AgeReq'] == '7+') ) & ((df['Priority']=='Retail') | (df['Priority']=='Sim Swap') | (df['Priority']=='IVR and COUK') | (df['Priority']=='Remove Bar') | (df['Priority']=='Porting Order')) ].index)
    #print("High Priority 12+ is",Backlog)
    Counter['Backlog Priority'] = BacklogPriority

    RetailPriority =len(df[((df['AgeReq'] == '12+') | (df['AgeReq'] == '3+')|(df['AgeReq'] == '7+')) & ((df['Priority']=='Retail') ) ].index)
    #print("High Priority 12+ Retail is",RetailPriority)
    Counter['Retail Priority'] = RetailPriority

    IVRPriority =len(df[((df['AgeReq'] == '12+') | (df['AgeReq'] == '3+')|(df['AgeReq'] == '7+')) & ((df['Priority']=='IVR and COUK') ) ].index)
    #print("High Priority 12+ IVR and COUK is",IVRPriority)
    Counter['IVR Priority'] = IVRPriority

    RemovePriority =len(df[((df['AgeReq'] == '12+') | (df['AgeReq'] == '3+')|(df['AgeReq'] == '7+')) & ((df['Priority']=='Remove Bar') ) ].index)
    #print("High Priority 12+ Remove Bar is",RemovePriority)
    Counter['Remove Priority'] = RemovePriority

    SSPriority =len(df[((df['AgeReq'] == '12+') | (df['AgeReq'] == '3+')|(df['AgeReq'] == '7+')) & ((df['Priority']=='Sim Swap') ) ].index)
    #print("High Priority 12+ Sim Swap is",SSPriority)
    Counter['SS Priority'] = SSPriority
    
    Porting =len(df[(df['Priority']=='Porting Order')  & ( (df['AgeReq'] == '3+')|(df['AgeReq'] == '7+'))].index)
    #print("Porting Orders 3+ are",Porting)
    Counter['Porting 3+'] = Porting
    
    Backlog =len(df[((df['AgeReq'] == '3+')|(df['AgeReq'] == '7+') ) & ((df['ORDER_TYPE']!='PortDate is Today') & (df['Priority']!='Do not Include'))].index)
   # print("Total Backlog 3+ count is",Backlog)
    Counter['Backlog 3+'] = Backlog
    
    BacklogPriority =len(df[( (df['AgeReq'] == '3+')|(df['AgeReq'] == '7+') ) & ((df['Priority']=='Retail') | (df['Priority']=='Sim Swap') | (df['Priority']=='IVR and COUK') | (df['Priority']=='Remove Bar') | (df['Priority']=='Porting Order')) ].index)
    #print("High Priority 3+ is",BacklogPriority)
    Counter['Backlog Priority 3+'] = BacklogPriority

    RetailPriority =len(df[( (df['AgeReq'] == '3+')|(df['AgeReq'] == '7+')) & ((df['Priority']=='Retail') ) ].index)
    #print("High Priority 3+ Retail is",RetailPriority)
    Counter['Retail Priority 3+'] = RetailPriority

    IVRPriority =len(df[( (df['AgeReq'] == '3+')|(df['AgeReq'] == '7+')) & ((df['Priority']=='IVR and COUK') ) ].index)
    #print("High Priority 3+ IVR and COUK is",IVRPriority)
    Counter['IVR Priority 3+'] = IVRPriority

    RemovePriority =len(df[( (df['AgeReq'] == '3+')|(df['AgeReq'] == '7+')) & ((df['Priority']=='Remove Bar') ) ].index)
    #print("High Priority 3+ Remove Bar is",RemovePriority)
    Counter['Remove Bar Priority 3+'] = RemovePriority

    SSPriority =len(df[( (df['AgeReq'] == '3+')|(df['AgeReq'] == '7+')) & ((df['Priority']=='Sim Swap') ) ].index)
    #print("High Priority 3+ /Sim Swap is",SSPriority)
    Counter['SS Priority 3+'] = SSPriority
    
    Porting =len(df[(df['Priority']=='Porting Order')  & ((df['AgeReq'] == '7+'))].index)
    #print("Porting Orders 7+ are",Porting)
    Counter['Porting 7+'] = Porting
    
    Backlog =len(df[(df['AgeReq'] == '7+')  & ((df['ORDER_TYPE']!='PortDate is Today') & (df['Priority']!='Do not Include'))].index)
    #print("Total Backlog 7+ count is",Backlog)
    Counter['Backlog 7+'] = Backlog
    
    BacklogPriority =len(df[((df['AgeReq'] == '7+') ) & ((df['Priority']=='Retail') | (df['Priority']=='Sim Swap') | (df['Priority']=='IVR and COUK') | (df['Priority']=='Remove Bar') | (df['Priority']=='Porting Order')) ].index)
    #print("High Priority 7+ is",BacklogPriority)
    Counter['Backlog Priority 7+'] = BacklogPriority

    RetailPriority =len(df[((df['AgeReq'] == '7+')) & ((df['Priority']=='Retail') ) ].index)
    #print("High Priority 7+ Retail is",RetailPriority)
    Counter['Retail Priority 7+'] = RetailPriority

    IVRPriority =len(df[((df['AgeReq'] == '7+')) & ((df['Priority']=='IVR and COUK') ) ].index)
    #print("High Priority 7+ IVR and COUK is",IVRPriority)
    Counter['IVR Priority 7+'] = IVRPriority

    RemovePriority =len(df[((df['AgeReq'] == '7+')) & ((df['Priority']=='Remove Bar') ) ].index)
    #print("High Priority 7+ Remove Bar is",RemovePriority)
    Counter['RemoveBar Priority 7+'] = RemovePriority

    SSPriority =len(df[((df['AgeReq'] == '7+')) & ((df['Priority']=='Sim Swap') ) ].index)
    #print("High Priority 7+ Sim Swap is",SSPriority)
    Counter['SS Priority 7+'] = SSPriority
    
    return Counter

def SaveKar(coldate,list2):
   saveit = input("Do you want to save this data?")
   
   if saveit == "y" :
       cd = coldate + 1  
       today = {'Date':[cd],'12+':list2[0],'3+':list2[1],'7+':list2[2]}
       dfnewdate = pd.DataFrame(data=today)
       print(dfnewdate)
       
       dfsaveit = pd.read_excel("C:\\Users\\prerna.prakash\\Desktop\\Input\\AgeDataNew.xlsx","TrackIt2.0")
       dfsaveit =dfsaveit.append(dfnewdate)
       saveExcel("C:\\Users\\prerna.prakash\\Desktop\\Input\\AgeDataNew.xlsx","TrackIt2.0",dfnewdate)
   else :
       time.sleep(60)
    
    

    
def sendMail():
    
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
starttime = timecheck()

default = "C:\\Users\\prerna.prakash\\Desktop\\Input\\"
TaskToExclude = ['CompleteShippingFunctionExitPointTask','CompleteShippingFunctionSITask','InitiateShippingFunctionTETask.manualTask','SettlePaymentFunctionFalloutRecoverTask','InitiateShippingFunctionSITask']
HP = ['Retail Shop','IVR','COUK']
SLP = ['Collections Barring','Back Office Disconnection','Credit Bar','OPD','VELTI','Back Office Automation']
Category = ['Activation','Regrade','Box Order','Change','Regrade','Disconnect']

list1 = SetUpConfigFile("Config.txt") 
dfMain = pd.read_excel("C:\\Users\\prerna.prakash\\Desktop\\Input\\Consolidated Stuck Order Report.xlsx")

dfCancellation = pd.read_excel("C:\\Users\\prerna.prakash\\Desktop\\Input\\Cancellation data orders.xlsx") 
dfTeamMap = pd.read_excel("C:\\Users\\prerna.prakash\\Desktop\\Input\\3+\\4.xlsx")
dfOldReport = pd.read_excel("C:\\Users\\prerna.prakash\\Desktop\\Input\\Consolidated Stuck Order Report_old.xlsx")
dfAppendHere = pd.read_excel("C:\\Users\\prerna.prakash\\Desktop\\Input\\Source.xlsx")
dfMain = dfMain.drop_duplicates(["SIEBEL_NUM"]).reset_index(drop=True)
dfMain = RemovePortDateNotPopulated(dfMain)
dfMain = DoExclude(dfMain,'LAST_TASK',TaskToExclude)
dfMain = dfMain.reset_index(drop=True)
dfMain =DoExclude(dfMain,'CATEGORY',['Valid Open'])
dfMain = dfMain.reset_index(drop=True)

dfMain = RemoveOrders(dfMain,dfCancellation,"SIEBEL_NUM","Order No.")
dfMain = dfMain.reset_index(drop=True)



dfMain.COLLECTED_DATE = pd.to_datetime(dfMain.COLLECTED_DATE,dayfirst=True)
dfMain.SUBMIT_DATE = pd.to_datetime(dfMain.SUBMIT_DATE,dayfirst=True)
dfMain.PORTDATE = pd.to_datetime(dfMain.PORTDATE,dayfirst=True)
coldate = dfMain.at[0,'COLLECTED_DATE']
#art = ART.ART()
#art.main()
coldate = coldate.date()
month = str(coldate.month)
day = str(coldate.day)
print(dfMain.at[0,'COLLECTED_DATE'])
dfMain = dfMain.reset_index(drop=True)
dfMain =  Age(dfMain,'SUBMIT_DATE','COLLECTED_DATE','PORTDATE')
dfMain = dfMain.reset_index(drop=True)
dfMain= AgeReq(dfMain)
dfMain = dfMain.reset_index(drop=True)
dfMain = SetPriority(dfMain,HP,SLP,Category)
vlookup(dfMain,dfTeamMap,"LAST_TASK","TASK",['TEAM'],"")
Backlog =dfMain[((dfMain['AgeReq'] == '12+') | (dfMain['AgeReq'] == '3+')|(dfMain['AgeReq'] == '7+'))  & ((dfMain['ORDER_TYPE']!='PortDate is Today') & (dfMain['Priority']!='Do not Include'))]
dfPivot = pd.pivot_table(Backlog,index = ['TEAM','LAST_TASK'],values =['SIEBEL_NUM'], aggfunc="count",margins = True).astype(int)
style = """
<style type="text/css">

table {

font-family: "Lato","sans-serif";   }       /* added custom font-family  */

table.one {                                 

margin-bottom: 3em;

border-collapse:collapse;   }  

td {                            /* removed the border from the table data rows  */

text-align: center;    

width: 1em;                   

padding: 0.5em;       }      



thead {                              /* removed the border from the table heading row  */

text-align: center;                

padding: 0.5em;

background-color: #e8503a;       /* added a red background color to the heading cells  */

color: white;       }                 /* added a white font color to the heading text */

th {                            /* removed the border from the table data rows  */

text-align: center;    

width: 1em;                   

padding: 0.5em;       }  

tr {   

height: 1em;    }

table tr:nth-child(even) {            /* added all even rows a #eee color  */

    background-color: #eee;     }

table tr:nth-child(odd) {            /* added all odd rows a #fff color  */

background-color:#fff;      }

</style>
"""
style1 = """
<style>
	
	table{
		border-style:solid;
    
	}
	
	thead {
		background-color : #ff6666;
		border-style:solid;
		color : white;
	}
	
	thead tr{
		background-color : #ff6666;
		border-style:solid;
		color : white;
	}
	
	
	
	td {
		border-style:solid;
		font: 15px helvetica, sans-serif;
		text-align : center;
       
	}
	
	th {
		border-style:solid;
		text-align : left;
       min-width: 20%;
		font: 15px helvetica, sans-serif;
	}
	
	.dataframe {
		border-style: none;
		padding: 0px;
		margin: 0;
	}
	
	tbody td{
		font-weight: normal;
		
		
	}
    
    tbody th{
		font-weight: normal;
		
		
	}
	
</style>

"""


sign = """
This is an auto-generated email
"""
html = dfPivot.to_html()
#html = html.replace("border=\"1\" ",'')
html = style +html+sign

#df2 = pd.pivot_table(df, values =['SIEBEL_NUM'],index=['SHIPPING','Age1'], aggfunc='count',margins= True,margins_name='Sum')
#dfPivot = pd.pivot_table(Backlog, values='SIEBEL_NUM', index=['TEAM', 'LAST_TASK'],columns=[], aggfunc='count')
#dfPivot = Backlog.pivot_table(index=['TEAM','LAST_TASK'],columns = ['TEAM','LAST_TASK'] ,aggfunc='count')
#print(dfPivot)
#dfPivot1.sort_values(by=('TEAM', 'All'), ascending=False,inplace=True)
#dfPivot.sort_values(by=('LAST_TASK', 'All'), ascending=False,inplace=True)
writer = pd.ExcelWriter(default+"Backlog\\"+day+"_"+month+".xlsx",engine = 'xlsxwriter')
Backlog.to_excel(writer,'Sheet1',index = False)
dfPivot.to_excel(writer,'Sheet2',index = True)
writer.save()
saveExcel(default+"Main.xlsx",'Sheet1',dfMain)
Dict = PrintStatements(dfMain)
Dict['Date'] = coldate + timedelta(days=1) 
for keys,values in Dict.items():
    print(keys ,":",values)
#print(pd.crosstab(dfMain["TEAM"],dfMain["AgeReq"],margins=True))
TO = 'VF_CCS_MobileOps@accenture.com; VF_CCS_OrderTriage@accenture.com;uday.singh01@vodafone.com;deepankar.a.sharma@accenture.com; Abhisek.Das01@vodafone.com;dipankar.kumar.gaine@accenture.com; u.pratap.singh@accenture.com;shilpi.hingorani@accenture.com'
#TO = 'shashank.mutgi@accenture.com'
triage = 'C:\\Users\\prerna.prakash\\Desktop\\Input\\TriageSheet\\'
attch = [default+"Backlog\\"+day+"_"+month+".xlsx",triage+'BillingTriage.xlsx',triage+'ExternalTriage.xlsx',triage+'OSMTriage.xlsx',triage+'UIMTriage.xlsx']
sm.send_Mail(TO,'12+ Status',attch,html)
#print(dfMain.groupby("LAST_TASK").filter(lambda x :x['LAST_TASK'].aggregate("count") > 4))

save = input("DO you want to save this data?")
if save == ('y') :

  
    dfSaver = pd.DataFrame(data=Dict,index = [0])  
    dfsaveit = pd.read_excel("C:\\Users\\prerna.prakash\\Desktop\\Input\\AgeDataNew.xlsx","Sheet1")

#dfsaveit =dfsaveit.append(dfSaver)
    dfsaveit = pd.concat([pd.DataFrame(dfSaver), dfsaveit], ignore_index=True)
    saveExcel("C:\\Users\\prerna.prakash\\Desktop\\Input\\AgeDataNew.xlsx","Sheet1",dfsaveit)
    saveExcel("Z:\\Postpay\\WAR ROOM ORDERS\\Backlog_OSM_UIM\\AgeDataNew.xlsx","Sheet1",dfsaveit)

    

else :
    print("Bye")
    



endtime = timecheck()
timemeasure(starttime,endtime)
#SaveKar()