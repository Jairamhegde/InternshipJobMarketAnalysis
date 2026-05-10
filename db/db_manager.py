import sqlite3

import logging
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__)) 
db_path = os.path.join(BASE_DIR, "jobs.db")
from datetime import datetime
def manage_operation(jd):
    try:
        conn=sqlite3.connect(db_path)
        cur=conn.cursor()
        for i in jd:
             if i['TechStack'] and i['company'] and i['job']:
                cur.execute(
                        'INSERT OR IGNORE INTO jobs(j_title,location,status,company,scraped_time,postedDate,minsal,maxsal) values(?,?,?,?,?,?,?,?)',
                        (
                            i['job'],
                            i['Location'],
                            i['status'],
                            i['company'],
                            i['Scrape_time'],
                            i['posted_date'],
                            i['min_sal'],
                            i['max_sal']
                        )
                        )
                if cur.rowcount == 1:
                    job_id = cur.lastrowid
                    if i["TechStack"]:
                        for techstack in i['TechStack'] :
                            cur.execute(
                                '''INSERT OR IGNORE INTO skills(name) values (?)''',
                                (techstack,)
                            )
                            cur.execute("SELECT s_id FROM skills WHERE name=?",(techstack,))
                            skid = cur.fetchone()
                            skillID = skid[0] if skid else None
                            if skillID:
                                cur.execute(
                                    '''INSERT OR IGNORE INTO job_skills(job_id,skill_id) VALUES(?,?)''',
                                    (job_id,skillID)
                                )
                cur.execute ('SELECT j_id from jobs WHERE j_title = ? AND location = ? AND company = ?',
                            (i['job'],i['Location'],i['company']))
                result = cur.fetchone()
                jbID = result[0] if result else None
                if jbID:
                    cur.execute(
                        '''INSERT OR IGNORE INTO jobSnapshot(job_id,scraped_date)values(?,?)''',
                        (jbID,datetime.now().strftime("%Y-%m-%d"))
                    )     
        conn.commit()  #commit the changes
        conn.close()    #close the connection
    except Exception as e:
        logging.error(e)







