# from fetcher import get_soup
from datetime import datetime,timedelta
import re
import logging
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
        for job in job_card:
            posted_time=job.select_one("div.color-labels span").text.strip()
            skills=job.find_all('div',class_="skill_container") if job.find_all('div',class_="skill_container") else None
            jobb=job.find('a',id='job_title').text.strip() if job.find('a',id='job_title') else None
            comp=job.find('p',class_="company-name").text.strip() if job.find('p',class_="company-name") else None
            status=job.find('div',class_="actively-hiring-badge").text.strip() if job.find('div',class_="actively-hiring-badge") else None
            sal=job.find('span',class_="desktop" ).text.strip() if job.find('span',class_="desktop") else None
            jobcard_length+=1
            #Extract the skills and store it on a list
            techstack=[skil.text.strip() for skil in skills ] if skills else None
            #Extract the location of the job
            location = job.select_one("p.locations a").get_text(strip=True) if job.select_one("p.locations a") else None
            jobPostedDate=dateFromtext(posted_time.lower()) if posted_time.lower() not in timeMeasure else datetime.now().strftime("%Y-%m-%d %H:%M")
            scrape_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
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
            # print(jobPostedDate)
        
            
        
        return job_data 
    except Exception as e:
        logging.ERROR(e)
'''
1.select_one : is a css selctor
2.we have to use np.nan instead of None if we want to actualy insert null into the csv
3.(skills) : it is not a tuple, (skills,) :touple with 1 element
4.cur.lastrowid : the id of the last row which it has inserted
'''

# scrape_data(get_soup("https://internshala.com/jobs/ai-agent-development,backend-development-jobs/"))