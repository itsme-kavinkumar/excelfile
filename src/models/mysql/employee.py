from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import traceback
from sqlalchemy import text
async def CreateQuery(emp_id,name,role,salary,db:AsyncSession):
    try:
        print(emp_id,name,role,salary)
        query= text(f"""INSERT INTO employee (emp_name, emp_role, salary) VALUES ('{name}', '{role}', {salary}) """
                    if emp_id=='' else f""" UPDATE employee SET emp_name='{name}',emp_role='{role}',salary={salary} WHERE emp_id={emp_id}""" )
        await db.execute(query)
        await db.commit()
        return {'message':"Employee created success"}

    except Exception as e:
        await db.rollback()
        print(e,'-----------',traceback.extract_tb(e.__traceback__))

async def GetQuery(emp_id,db:AsyncSession):
    try:
        where = ''
        if emp_id:
            where = f"WHERE emp_id={emp_id}"
        query = text(f"SELECT * FROM employee {where}")
        
        data = await db.execute(query)
        result=data.fetchall()
        columns = data.keys()
        result_dicts = [dict(zip(columns, row)) for row in result]
        print(result_dicts)
        return result_dicts

    except Exception as e:
        await db.rollback()
        print(e,'-----------',traceback.extract_tb(e.__traceback__))


async def DeleteQuery(emp_id,db:AsyncSession):
    try:
        query = text(
            f"""DELETE FROM employee WHERE emp_id={emp_id}""")
        await db.execute(query)
        await db.commit()
        
        return {'message':"Employee delete success"}

    except Exception as e:
        await db.rollback()
        print(e,'-----------',traceback.extract_tb(e.__traceback__))

      