
"""
Created on Sun Apr 29 15:53:34 2018

@author: prerna.prakash
"""

import win32com.client as win32
import os

#this module is used for opening outlook and sending a mail with multiple attachments
def send_Mail(to:str,subject:str,attachment:list,html:str):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = to
    mail.Subject = subject
    mail.HTMLBody= html
    for each in attachment :
        mail.Attachments.Add(each)    
    mail.Send()
    print('Your mail has been sent')


