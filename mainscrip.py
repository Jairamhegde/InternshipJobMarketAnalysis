

from scraper.cleanData import clean_data
from insights.insight import generate_insights
# from app import DashBoard
from pathlib import Path
import subprocess
import sys
import logging
import sqlite3
from scraper.fetcher import get_soup
from scraper.extractor import scrape_data
from db.db_manager import manage_operation

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s",
    handlers=[
        logging.FileHandler("logfile.log"),
        logging.StreamHandler()
    ]
)
logging.info("Execution started..")
def internshala(url):   
    
        for i in range(1,21):
            if i==1:
                link=url
            else:
                link=url+f'page-{i}'
            try:
                g=get_soup(link)
                x=scrape_data(g)     
                logging.info(f"Scraped data from page {i}")
                manage_operation(x)
                logging.info("inserted the data into the tables..")
            except Exception as e:
                logging.error(e)

def run_streamlit():
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py"
    ])
     
if __name__=='__main__':
    internshala("https://internshala.com/jobs/net-development,ai-agent-development,asp-net,android-app-development,angular-js-development,backend-development,cloud-computing,cyber-security,front-end-development,full-stack-development,game-development,java,javascript-development,machine-learning,node-js-development,python-django,web-development-jobs/")   
    run_streamlit()
