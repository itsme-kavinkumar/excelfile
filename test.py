from src.endpoints.exportexcel import CreateExcel

from datetime import datetime,timedelta
import time
import os
import traceback
import threading
from babel.numbers import format_currency
import re
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
import time
from concurrent.futures import ThreadPoolExecutor




# def currency(value):
#     output=format_currency(value, 'INR', ).replace(u'\xa0', u' ')
#     output= re.sub(r'[₹]','',output)
#     if '₹' in output:
#         print('yees')
#     indx=output.index('.')
#     print('+++++++++++++++',output[:indx])
#     return output
 
# currency(100000)
# CreateExcel()

# def create_log(folder_name,values):

#     while True:
#         try:
            
#             current_time = datetime.now().strftime("%d-%m-%Y")
#             current_path=os.getcwd()
#             folder_path = os.path.join(current_path,f"Logs\{folder_name}")

#             if not os.path.exists(folder_path):
#                 os.makedirs(folder_path)

#             file_path= os.path.join(folder_path,f"{current_time}.txt")
            
#             with open(file_path, 'a') as file:
#                 file.write(f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S %p")}  {values} \n')
            
#             delete_file_name= datetime.now()-timedelta(days=5)
#             delete_file_name=delete_file_name.strftime("%d-%m-%Y")
#             old_log_file = os.path.join(folder_path,f"{delete_file_name}.txt")
            
#             if os.path.exists(old_log_file):
#                 os.remove(old_log_file) 
            
#             time.sleep(5)
#         except Exception as e:
#             print("-------",e,traceback.extract_tb(e.__traceback__))

def create_log(folder_name,values):
    
    current_path=os.getcwd()
    folder_path = os.path.join(current_path,f"Logs\{folder_name}")
    os.makedirs(folder_path,exist_ok=True)
    while True:
        try:
            
            current_time = datetime.now().strftime("%d-%m-%Y")
            file_path= os.path.join(current_path,f"Logs\{folder_name}",f"{current_time}.txt")
            with open(file_path, 'a') as file:
                file.write(f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S %p")}  {values} \n')
            old_log_file = os.path.join(
                current_path, 
                f"Logs\{folder_name}",
                f"{(datetime.now() - timedelta(days=5)).strftime('%d-%m-%Y')}.txt"
            )
            os.remove(old_log_file) if os.path.exists(old_log_file) else None
            time.sleep(5)
            
        except Exception as e:
            print("-------",e,traceback.extract_tb(e.__traceback__))


try:

    data=[
        {'folder':"folder1",'value':'log1'},
        {'folder':"folder2",'value':'log2'},
        {'folder':"folder3",'value':'log3'},
        {'folder':"folder4",'value':'log4'},
        {'folder':"folder5",'value':'log5'},
    ]
    threads=[threading.Thread(target=create_log, args=(values['folder'], values['value'],)) for values in data]
    [thread.start() for thread in threads],[thread.join() for thread in threads]

except Exception as e:
    print("-------",e,traceback.extract_tb(e.__traceback__))








