import sqlite3
import os
BASE_DIR=os.path.commonpath(__file__)
db_path=os.path.join(BASE_DIR,"jobs.db")
conn=sqlite3.connect(db_path)
cur=conn.cursor()
cur.execute(
    '''
CREATE TABLE IF NOT EXISTS jobs(
j_id INTEGER PRIMARY KEY AUTOINCREMENT,
J_title TEXT,
location TEXT,
salary TEXT,
status TEXT
)
'''
)
cur.execute(
    '''
CREATE TABLE IF NOT EXISTS skills(
s_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT
)
'''
)
cur.execute(
    '''
CREATE TABLE IF NOT EXISTS job_skills(
job_id INTEGER,
skill_id TEXT,
FOREIGN KEY (job_id) references jobs(j_id),
FOREIGN KEY (skill_id) REFERENCES skills(s_id) 
)
'''
)


conn.commit()
conn.close()