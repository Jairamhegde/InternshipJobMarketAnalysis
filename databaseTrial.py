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

trends='''
    SELECT J_title ,count(J_title) as NO_of_jobs,scraped_time
    FROM jobs
    GROUP BY scraped_time;
   
'''
# last_scraped_date='''
# SELECT max(scraped_time)
# from jobs;'''


mont_year='''
WITH role_counts AS (
    SELECT 
        strftime('%H', scraped_time) AS hour,
        J_title,
        COUNT(*) AS role_count
    FROM jobs
    GROUP BY hour, J_title
),
ranked_roles AS (
    SELECT 
        hour,
        J_title,
        role_count,
        ROW_NUMBER() OVER (
            PARTITION BY hour 
            ORDER BY role_count DESC
        ) AS rank
    FROM role_counts
)
SELECT 
    hour,
    J_title,
    role_count
FROM ranked_roles
WHERE rank <= 3
ORDER BY hour, role_count DESC;
'''

skill="""

SELECT count(distinct(name)) FROM skills;
"""
query=pd.read_sql_query(skill,conn)
print(query)

# query=pd.read_sql_query(trends,conn)
# print(query.loc[:,"scraped_time"])
# qr=pd.read_sql_query(developer_skills,conn)
# qr2=pd.read_sql_query(no_of_jobs,conn)
# print(qr)
# print(qr2)
conn.commit()
conn.close()
