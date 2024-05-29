from fastapi import APIRouter,Form,HTTPException,Depends
from src.models.mysql.employee import*
router=APIRouter()
import traceback
@router.post("/create")
async def create(emp_id:int=Form(''),name:str=Form(''),role:str=Form(''),salary:int=Form(''),db:AsyncSession=Depends(get_db)):
    try:
        result= await CreateQuery(emp_id,name,role,salary,db)
        return result

    except Exception as e:
        print('-----------',traceback.extract_tb(e.__traceback__))
        raise HTTPException(status_code=500,detail={'error':"something went wrong"})
    
@router.post("/get")
async def get_data(emp_id:int=Form(''),db:AsyncSession=Depends(get_db)):
    try:
        result= await GetQuery(emp_id,db)
        return result

    except Exception as e:
        print('-----------',traceback.extract_tb(e.__traceback__))
        raise HTTPException(status_code=500,detail={'error':"something went wrong"})
    

@router.post("/delete")
async def delete(emp_id:int,db:AsyncSession=Depends(get_db)):
    try:
        result= await DeleteQuery(emp_id,db)
        return result

    except Exception as e:
        print('-----------',traceback.extract_tb(e.__traceback__))
        raise HTTPException(status_code=500,detail={'error':"something went wrong"})
