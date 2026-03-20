import sqlite3
import pandas as pd

conn=sqlite3.connect('jobs.db')
cur=conn.cursor()
developer_skills='''
SELECT s.name,count(s.name) as max_count
FROM jobs j
JOIN job_skills jb ON j.j_id = jb.job_id
JOIN skills s ON s.s_id = jb.skill_id
WHERE j.j_title = 'Full Stack Developer'
group by s.name
order by max_count desc
limit 6;

'''

no_of_jobs='''
SELECT count(J_title) as no_of_jobs
FROM jobs
WHERE J_title='Full Stack Developer';
'''
desc='''PRAGMA table_info(jobs);
'''
query=pd.read_sql_query(desc,conn)
print(query)
# qr=pd.read_sql_query(developer_skills,conn)
# qr2=pd.read_sql_query(no_of_jobs,conn)
# print(qr)
# print(qr2)
conn.commit()
conn.close()
