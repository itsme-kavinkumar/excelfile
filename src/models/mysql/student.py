# from database import cursor,db_conf
import traceback
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def GetTotalMarkQuery(db):

    query = """SELECT student.Name, sum(marks.subjectMark) AS Total_semester_mark FROM student
            INNER JOIN marks ON student.studentId= marks.studentId GROUP BY student.Name;
            """
    data = await db.execute(query)
    result = await db.fetchall()
    print(result)

    return result


async def GetMarkQuery(db):

    query = """ SELECT
                        st.Name,
                        sem.semNo,
                        sum(mrk.subjectMark) AS total_mark
                FROM 
                        student AS st
                        INNER JOIN marks AS mrk on mrk.studentId = st.studentId
                        INNER JOIN semester AS sem on sem.semId= mrk.semId
                GROUP BY 
                        st.Name,sem.semNo
                ORDER BY 
                        st.Name;
            """
    data = await db.execute(query)
    result = await db.fetchall()
    print(result)

    return result
