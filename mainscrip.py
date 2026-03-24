

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
     filename="logfile.log",
     level=logging.INFO,
     format='%(asctime)s-%(levelname)s-%(name)s-%(message)s'
)
logging.info("Execution started..")
def internshala(url):   
    
        for i in range(1,11):
            if i==1:
                link=url
            else:
                link=url+f'page-{i}'
        try:
            g=get_soup(link)
            x=scrape_data(g)
                
            logging.info(f"Scraped data from page {i}")
            manage_operation(x)
              
        except Exception as e:
             logging.error("error while scraping..")

        
         

def run_streamlit():
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py"
    ])
     
# if __name__=='__main__':
#     internshala("https://internshala.com/jobs/ai-agent-development,backend-development-jobs/",takeuserInput())   
#     run_streamlit()
