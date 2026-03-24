import sqlite3
import logging
import os
BASE_DIR=os.path.commonpath(__file__)
db_path=os.path.join(BASE_DIR,"jobs.db")
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
cur.execute(

    "ALTER TABLE jobs RENAME COLUMN acraped_time TO scraped_time"
)
# logging.info("Added scraped_time column to jobs table")
conn.commit()
conn.close()