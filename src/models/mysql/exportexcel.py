async def GetQuery(db):

    query = """
            SELECT
                st.Name,
                st.studentCode, 
                SUM(mrk.subjectMark) AS total_mark,
                SUM(CASE WHEN sem.semNo=1 THEN mrk.subjectMark ELSE 0 END) AS sem1,
                sum(CASE WHEN sem.semNo=2 THEN mrk.subjectMark ELSE 0 END) AS sem2,
                sum(CASE WHEN sem.semNo=3 THEN mrk.subjectMark ELSE 0 END) AS sem3,
                sum(CASE WHEN sem.semNo=4 THEN mrk.subjectMark ELSE 0 END) AS sem4,
                sum(case when sem.semNo=5 then mrk.subjectMark else 0 end) as sem5,
                sum(case when sem.semNo=6 then mrk.subjectMark else 0 end) as sem6
            FROM 
                student AS st
                INNER JOIN marks AS mrk on mrk.studentId = st.studentId
                INNER JOIN semester AS sem on sem.semId= mrk.semId
                
            GROUP BY 
                st.Name,st.studentCode
            ORDER BY 
	            st.Name;
            """
    await db.execute(query)

    result = await db.fetchall()
    return result
