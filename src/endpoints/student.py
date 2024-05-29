from fastapi import APIRouter,HTTPException,Depends
from src.models.mysql.student import*
import traceback
from database import get_db
import os
from fastapi.responses import JSONResponse
router=APIRouter()

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os
# from log_file import createFolder
import traceback
import sys 
from typing import AsyncGenerator  

def _getReturnResponseJson(datas):
    resarray={}
    resarray["iserror"] = False
    resarray["message"] = "Data Received Successfully."
    resarray["data"] =datas
    return JSONResponse(jsonable_encoder(resarray))

def get_exception_response(e: Exception):
    error_type = type(e).__name__
    try:
        error_line = traceback.extract_tb(e.__traceback__)[1].lineno
        error_filename = os.path.basename(traceback.extract_tb(e.__traceback__)[1].filename)
    except: 
        error_line = traceback.extract_tb(e.__traceback__)[0].lineno
        error_filename = os.path.basename(traceback.extract_tb(e.__traceback__)[0].filename)
    error_message = f"{error_type} occurred in file {error_filename}, line {error_line}: {str(e)}"
    
    resarray={}
    resarray["iserror"] = True
    resarray["message"] = "Error Exception"
    resarray["error"] = error_message
    
    return JSONResponse(resarray)


@router.post("/student-total-marks")
async def GetTotalMarkList(db:AsyncGenerator=Depends(get_db)):
    try:
        result= await GetTotalMarkQuery(db)
        return  result
    except Exception as e :
        return get_exception_response(e)
@router.post("/student-marks")
async def GetMarkList(db:AsyncGenerator=Depends(get_db)):
    try:
        result= await GetMarkQuery(db)
        return  result
    except Exception as e :
        return get_exception_response(e)