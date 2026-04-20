# from fetcher import get_soup
from datetime import datetime,timedelta
import re
import logging
import pandas as pd
def dateFromtext(i):
    match = re.search(r"(\d+)\s(\w+)\sago",i)
    value = int(match.group(1))
    measure = match.group(2)
    if measure == "day" or measure == "days":
        date = (datetime.now() - timedelta(days=value)).strftime("%Y-%m-%d")
    if measure == "week" or measure == "weeks":
        date = (datetime.now() - timedelta(weeks=value)).strftime("%Y-%m-%d")
    return date

def scrape_data(soup):
    try:
        import sqlite3
        #Connect to the Database file 
        conn=sqlite3.connect("jobs.db")
        # Extract all the fields from web
        import numpy as np
        timeMeasure = ["few hours ago","just now","today"]
        job_card=soup.find_all('div',class_="internship_meta experience_meta")
        job_data=[]
        jobcard_length = 0
        if job_card:
            for job in job_card:
                postedtime_tag = job.select_one("div.color-labels span")
                posted_time=postedtime_tag.text.strip() if postedtime_tag else None

                skills_tag = job.find_all('div',class_="skill_container")
                skills= skills_tag if skills_tag else None

                job_tag = job.find('a',id='job_title')
                jobb=job_tag.text.strip() if job_tag else None

                company_tag = job.find('p',class_="company-name")
                comp=company_tag.text.strip() if company_tag else None

                status_tag =job.find('div',class_="actively-hiring-badge")
                status=status_tag.text.strip() if status_tag else None

                sal_tag = job.find('span',class_="desktop")
                sal=sal_tag.text.strip() if sal_tag else None

                jobcard_length+=1
                #Extract the skills and store it on a list
                techstack=[skil.text.strip().lower() for skil in skills ] if skills else None
                #Extract the location of the job
                location_tag = job.select_one("p.locations a")
                location = location_tag.get_text(strip=True) if location_tag else None


                jobPostedDate=dateFromtext(posted_time.lower()) if posted_time.lower() not in timeMeasure else datetime.now().strftime("%Y-%m-%d")
                scrape_time = datetime.now().strftime("%Y-%m-%d")
            
                jd={"job":jobb,
                    "company":comp,
                    "status":status,
                    "Salary":sal,
                    "TechStack":techstack ,
                    "Location":location ,
                    "Scrape_time":scrape_time,
                    "posted_date":jobPostedDate
                    }
                
                job_data.append(jd)
        df = pd.DataFrame(job_data)
        df.to_csv("mycsv.csv",index= False)
            # print(jobPostedDate)
        
            
        
        return job_data 
    except Exception as e:
        logging.error(e)
'''
1.select_one : is a css selctor
2.we have to use np.nan instead of None if we want to actualy insert null into the csv
3.(skills) : it is not a tuple, (skills,) :touple with 1 element
4.cur.lastrowid : the id of the last row which it has inserted
'''
# from fetcher import get_soup

# scrape_data(get_soup("https://internshala.com/jobs/ai-agent-development,backend-development-jobs/"))