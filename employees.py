from fastapi import FastAPI,HTTPException
import mysql.connector
from fastapi import Form
app=FastAPI()

config={
    "host":"localhost",
    "user":"root",
    "password":"8696",
    "database":""
}
db_con=mysql.connector.connect(**config)
cursor=db_con.cursor()

@app.post("/create-employee")
def CreateEmplopyee(name:str=Form(''),role:str=Form(''),salary:int=Form('')):
    query="INSERT INTO employee (emp_name,emp_role,salary) VALUES(%s,%s,%s)"
    values=(name,role,salary)
    cursor.execute(query,values)
    db_con.commit()
    

    return {'msg':"success"}

@app.get("/get-employee-details")
def GetEmployee(employee_id=None):
    values=(employee_id)
    if employee_id:
        query="SELECT * FROM employee WHERE emp_id= %s"
        cursor.execute(query,values)
    else:
        query="SELECT * FROM employee "
        cursor.execute(query )
    # db_con.commit()
    result=cursor.fetchall()
    if result is not None:
        return result 
    raise HTTPException(status_code=404,detail="No data found")


@app.put("/update-employee")
def UpdateEmployee(employee_id,name,role,salary):
    print("---------------")
    query="UPDATE employee SET emp_name=%s, emp_role=%s, salary=%s WHERE emp_id=%s"
    values=(name,role,salary,employee_id)
    cursor.execute(query,values)
    db_con.commit()
    return {'msg':"OK"}

@app.delete("/delete-employee")

def DeleteEmployee(employee_id):
    query="DELETE employee WHERE emp_id =%s"
    values=(employee_id)
    cursor.execute(query,values)



# DATABASE_URL = f"mysql+aiomysql://root@localhost:3306/ems_v1"
# engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)  

# async_session = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
# )

# async def get_db() -> AsyncSession:
#     async with async_session() as session:
#         yield session



# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine, text
# from sqlalchemy.pool import QueuePool,NullPool
# import os
# from fastapi import FastAPI,Request,Form,Body,Depends,HTTPException
# from sqlalchemy.orm import Session
# import aiomysql
# import asyncio
# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy import create_engine, text
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
