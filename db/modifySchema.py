import sqlite3
import logging
import os
logging.basicConfig(
    filename = "logfile.log"
)
BASE_DIR = os.path.dirname(os.path.dirname(__file__)) 
db_path = os.path.join(BASE_DIR, "jobs.db")
conn=sqlite3.connect(db_path)
cur=conn.cursor()
# logging.info("ade")
# cur.execute(
#     'ALTER TABLE jobs add company text'
# )
# cur.execute(
#     'CREATE UNIQUE INDEX IF NOT EXISTS idx_job_unique ON jobs (j_title, company, location)'
# )
# logging.info("Aded unique contrain on jobs")
# cur.execute(

#     "ALTER TABLE jobs RENAME COLUMN acraped_time TO scraped_time"
# )

# cur.execute(
#     "alter table skills rename to old_skil"
# )
# logging.info("Added scraped_time column to jobs table")
# cur.execute(
#     '''
#     CREATE TABLE jobsnd_skills(
#     job_id INT,
#     skill_id TEXT,
#     PRIMARY KEY(job_id,skill_id),
#     FOREIGN KEY(job_id)REFERENCES jobs(j_id) ON DELETE CASCADE,
#     FOREIGN KEY(skill_id)REFERENCES skills(s_id) ON DELETE CASCADE
#     )
# ;'''
# )
# cur.execute(
#     '''INSERT OR IGNORE INTO  jobsnd_skills(job_id,skill_id) SELECT job_id,skill_id from job_skills;
# '''
# )
# cur.execute(''' drop table jobsnd_skills''')
# cur.execute('''
# PRAGMA foreign_keys = on;
# ''')
# cur.execute('''
# ALTER TABLE jobsnd_skills rename to job_skills;
# ''')

def clearTable():
    conn=sqlite3.connect(db_path)
    cur=conn.cursor()
    cur.execute('DELETE FROM jobs')
    cur.execute('DELETE FROM skills')
    cur.execute('DELETE FROM job_skills')
    cur.execute('DELETE FROM jobSnapshot')
    conn.commit()
    conn.close()
    logging.info("cleared table...")


# cur.execute('''
# CREATE TABLE jobSnapshot(
#         job_id INT,
#         scraped_date date,
#         PRIMARY KEY(job_id,scraped_date));
# ''')

# cur.execute('''
# insert into jobSnapshot(job_id,scraped_date)
#             select j_id,scraped_time from jobs;


# ''')

clearTable()
conn.commit()
conn.close()
