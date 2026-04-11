import sqlite3
# from scraper.extractor import scrape_data
# from scraper.fetcher import get_soup
# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent
import logging
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__)) 
db_path = os.path.join(BASE_DIR, "jobs.db")

def manage_operation(jd):
    try:
        conn=sqlite3.connect(db_path)
        cur=conn.cursor()
        for i in jd:
            cur.execute(
                    'INSERT OR IGNORE INTO jobs(j_title,location,salary,status,company,scraped_time,postedDate) values(?,?,?,?,?,?,?)',
                    (
                        i['job'],
                        i['Location'],
                        i['Salary'],
                        i['status'],
                        i['company'],
                        i['Scrape_time'],
                        i['posted_date']
                    )
                    )
            if cur.lastrowid:
                job_id = cur.lastrowid 
                if i['TechStack']:
                    for techstack in i['TechStack']:
                        cur.execute(
                            'INSERT OR IGNORE INTO skills(name) VALUES(?)',
                            (techstack,))
                        
                        cur.execute(
                            'SELECT s_id FROM skills WHERE name=?',
                            (techstack,)
                        )
                        word=cur.fetchone()
                        if word:
                            skill_id=word[0] #this line fetches the skill id which helps to map the skils with the job in job_skills table
                        else:
                            continue

                        # Insert data into job_skills table
                        cur.execute(
                            "INSERT OR IGNORE INTO job_skills(job_id,skill_id) VALUES (?,?)",
                            (job_id,skill_id)
                        )
            else:
                cur.execute(
                '''SELECT j_id from jobs
                where j_title=? and company=? and location=?''',
                (i['job'],i['company'],i['Location'])

                )
                job_id=cur.fetchone()[0]
            cur.execute(
                '''INSERT INTO jobSnapshot(job_id,scraped_date) values(?,?)''',(job_id,i["Scrape_time"])
            )
                # Get the job id

        
        conn.commit()  #commit the changes
        conn.close()    #close the connection
    except Exception as e:
        logging.error(e)







