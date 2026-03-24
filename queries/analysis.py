import sqlite3
import pandas as pd


import os
BASE_DIR=os.path.commonpath(__file__)
db_path=os.path.join(BASE_DIR,"jobs.db")
def topSkills():
    # db_path = 'jobs.db'
    conn = sqlite3.connect(db_path)
    query = '''
    SELECT s.name, count(*) as demand
    FROM skills s
    JOIN job_skills js ON s.s_id = js.skill_id
    GROUP BY s.name
    ORDER BY demand DESC
    limit 10;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
def roles():
    # db_path = 'jobs.db'
    conn=sqlite3.connect(db_path)
    query='''
    SELECT j.j_title,count(*) as demand
    FROM jobs j
    GROUP BY j_title
    ORDER BY demand DESC
    LIMIT 10;
    '''
    df=pd.read_sql_query(query,conn)
    conn.close()
    return df
def topLocations():
    # db_path = 'jobs.db'
    conn=sqlite3.connect(db_path)
    query='''
    SELECT j.location ,count(j.location) as count
    FROM jobs j
    GROUP BY j.location
    ORDER BY count DESC
    limit 10;
'''
    df=pd.read_sql_query(query,conn)
    conn.close()
    return df
def commonRoles():
    # db_path = 'jobs.db'
    conn=sqlite3.connect(db_path)
    query='''
        SELECT
        s.name AS skill,
        COUNT(DISTINCT j.j_title) AS role_count,
        COUNT(*) AS total_occurrences
    FROM jobs j
    JOIN job_skills js ON j.j_id = js.job_id
    JOIN skills s ON s.s_id = js.skill_id
    WHERE j.j_title IN (
        SELECT j_title
        FROM jobs
        GROUP BY j_title
        ORDER BY COUNT(*) DESC
        LIMIT 2
    )
    GROUP BY s.name
    HAVING COUNT(DISTINCT j.j_title) = 2
ORDER BY total_occurrences DESC;

'''
    df=pd.read_sql_query(query,conn)
    conn.close()
    return df
def TopSkillsOfRole(role):
    # db_path = 'jobs.db'
    conn=sqlite3.connect(db_path)
    query='''
    SELECT s.name,count(*) as demand
    FROM jobs j
    JOIN job_skills js ON j.j_id = js.job_id
    JOIN skills s ON s.s_id = js.skill_id
    WHERE j.j_title = ?
    GROUP BY s.name
    ORDER BY demand DESC
    LIMIT 10;
    '''
    df=pd.read_sql_query(query,conn,params=(role,))
    conn.close()
    return df
def jobCount(job):
    # db_path = 'jobs.db'
    conn=sqlite3.connect(db_path)
    query='''
    SELECT count(J_title) as no_of_jobs
    FROM jobs
    WHERE J_title=?;
'''
    df=pd.read_sql_query(query,conn,params=(job,))
    conn.close()
    return df
def sortRoles(role):
    # db_path = 'jobs.db'
    conn=sqlite3.connect(db_path)
    query='''
SELECT job,count(job) jobcount,
FROM jobs

'''
def last_scraped_time():
    # db_path = 'jobs.db'
    conn=sqlite3.connect(db_path)

    query='''
    SELECT max(scraped_time)
    from jobs;'''
    df=pd.read_sql_query(query,conn)
    conn.close()
    return df

# print(commonRoles())

