from fastapi import APIRouter,HTTPException,Depends
from typing import AsyncGenerator
from database import get_db
from jose import JWTError,jwt
from datetime import datetime,timedelta
from passlib.context import CryptContext
import secrets
import traceback
from src.endpoints.student import get_exception_response
router=APIRouter()
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"


@router.post('/user-register')
async def Register(studentName:str,email:str,password:str,db:AsyncGenerator=Depends(get_db)):

    try:
        
        

        query=  '''
                SELECT
                    email 
                FROM
                    User
                '''
        data=await db.execute(query)
        result= await db.fetchall()
        print('---------',result)
        if any(data['email']==email for data in result):
            return HTTPException (status_code=404,detail={'msg':"email already exists"})
        
        hashed_password= CryptContext(schemes=['bcrypt'],deprecated="auto").hash(password)
     
        query=  """
                INSERT INTO     
                    User(studentName,email,password) 
                VALUES(%s,%s,%s);
                """
        values=(studentName,email,hashed_password)
        await db.execute(query, values)
        return {'msg':'user created sucessfully'}

    except Exception as e:
        return str(e)
                
@router.post('/login')
async def Login(email:str,password:str, db:AsyncGenerator=Depends(get_db)):

    try:
        user= await authenticate(email,password,db)
        print("user------",user)
        if not user:
            raise HTTPException(status_code=404,detail={'message':"user not found"})
        
        access_token = create_access_token(data={"sub": user[0]['email']}, expires_delta=timedelta(minutes=30))

        print("token---",access_token)
        return {"access_token": access_token}

    except Exception as e:
        return str(e)
    

def create_access_token(data: dict, expires_delta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate(email, password, db):
    try:
        print("------auth", email)
        query = '''
            SELECT 
                *
            FROM 
                User 
            WHERE       
                email = %s
            '''
        values = (email,)
        result = await db.execute(query, values)
        
        user = await db.fetchall()
        if not user:
            return None
        hashed_pw = user[0].get('password')
        print(hashed_pw, 'verify password', password, user)
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        password_verify = pwd_context.verify(password, hashed_pw)
        if not password_verify:
            return None
        
        return user
    except Exception as e:
        print(get_exception_response(e),'+}+}+', traceback.extract_tb(e.__traceback__))
        return get_exception_response(e)