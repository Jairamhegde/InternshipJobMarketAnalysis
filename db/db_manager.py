import sqlite3
# from scraper.extractor import scrape_data
# from scraper.fetcher import get_soup
# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__)) 
db_path = os.path.join(BASE_DIR, "jobs.db")

def manage_operation(jd):
    conn=sqlite3.connect(db_path)
   
    cur=conn.cursor()
    for i in jd:
        cur.execute(
                'INSERT OR IGNORE INTO jobs(j_title,location,salary,status,company,scraped_time) values(?,?,?,?,?,?)',
                (
                    i['job'],
                    i['Location'],
                    i['Salary'],
                    i['status'],
                    i['company'],
                    i['Scrape_time']
                )
                )
        job_id=cur.lastrowid
        cur.execute(
            '''UPDATE OR IGNORE Jobs set company=? WHERE j_id=?''',
            (i['company'],job_id)
)
    # Get the job id
        
        if i['TechStack']:
            for techstack in i['TechStack']:
                cur.execute(
                    'INSERT OR IGNORE INTO skills(name) VALUES(?)',
                    (techstack,))
                
                cur.execute(
                    'SELECT s_id FROM skills WHERE name=?',
                    (techstack,)
                )
                skill_id=cur.fetchone()[0] #this line fetches the skill id which helps to map the skils with the job in jo_skills table

                # Insert data into job_skills table
                cur.execute(
                    "INSERT OR IGNORE INTO job_skills(job_id,skill_id) VALUES (?,?)",
                    (job_id,skill_id)
                )
   
    
    conn.commit()  #commit the changes
    conn.close()    #close the connection


def clearTable():
    conn=sqlite3.connect(db_path)
    cur=conn.cursor()
    # cur.execute('DELETE FROM jobs')
    # cur.execute('DELETE FROM skills')
    cur.execute('DELETE FROM skills')
    conn.commit()
    conn.close()




