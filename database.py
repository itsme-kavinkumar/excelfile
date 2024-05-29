import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
# from log_file import createFolder
from sqlalchemy.pool import NullPool
from fastapi import APIRouter, Request
from datetime import datetime
from sqlalchemy import text
import sys
import subprocess
from typing import AsyncGenerator
import aiomysql
from fastapi import Depends
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from src.endpoints.response_json import get_exception_response
import base64
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os
# from log_file import createFolder
import traceback
import sys 


def get_exception_response(e: Exception):
    error_type = type(e).__name__
    try:
        error_line = traceback.extract_tb(e.__traceback__)[1].lineno
        error_filename = os.path.basename(traceback.extract_tb(e.__traceback__)[1].filename)
    except: 
        error_line = traceback.extract_tb(e.__traceback__)[0].lineno
        error_filename = os.path.basename(traceback.extract_tb(e.__traceback__)[0].filename)
    error_message = f"{error_type} occurred in file {error_filename}, line {error_line}: {str(e)}"
    # createFolder("Log/","Issue in returning data "+error_message)
    resarray={}
    resarray["iserror"] = True
    resarray["message"] = "Error Exception"
    resarray["error"] = error_message
    
    return JSONResponse(resarray)


# try:
#     file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "api_config.ini"))
#     # createFolder("Log/",f"file_path - {file_path} ")
    
#     if os.path.isfile(file_path):
#         try:
#             # Open the file and read the lines
#             with open(file_path, "r") as file:
#                 lines = file.readlines()

#                 # Extract each line separately
#                 if len(lines) >= 5:
#                     port_num = int(lines[1].strip())
#                     third_line = lines[2]
#                     decoded_data = base64.b64decode(third_line).decode()
#                     third_line_parts = decoded_data.strip().split('|')

#                     if len(third_line_parts) == 2:
#                         user_name, pass_word = third_line_parts
#                     else:
#                         print(f"Error: Incorrect format in third line: {lines[2]}")

#                 else:
#                     print(f"Error: Insufficient lines in {file_path}")

#         except Exception as e:
#             print(f"Error reading file: {str(e)}")
#     else:
#         print(f"Error: File {file_path} not found.")


# except Exception as e:
#         get_exception_response(e)


try:
    class Settings:
        DATABASE = {
            "HOST": "localhost",
            "PORT": 3306,  
            "USER": 'root',
            "NAME": "employee_crud",
            "PASSWORD": "8696"
        }


    settings = Settings()
    async def create_pool():
        return await aiomysql.create_pool(
            host=settings.DATABASE["HOST"],
            port=settings.DATABASE["PORT"],
            user=settings.DATABASE["USER"],
            db=settings.DATABASE["NAME"],
            password=settings.DATABASE["PASSWORD"],
            autocommit=True,
        )

    async def close_pool(pool):
        pool.close()
        await pool.wait_closed()
except Exception as e:
        get_exception_response(e)     

async def get_db(
    request: Request,
    pool=Depends(create_pool)
) -> AsyncGenerator:
    try:
    # Log information about the database connection
        # ips = request.client.host
        # path_url = request.url
        # form_data = await request.form()

        # api_reach_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # db_connecting_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # api_response_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # log_message = f"IP: {ips}, API_Reach_Time: {api_reach_time}, Db_Connection_Time: {db_connecting_time}, API_Response_Time: {api_response_time}, url: {path_url}, input_data: {form_data}"        
        # # createFolder("Log/", log_message)
        

        async with pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                yield cursor
    except Exception as e:
        get_exception_response(e)

    


