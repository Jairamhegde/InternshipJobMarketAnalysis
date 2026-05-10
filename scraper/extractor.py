# from fetcher import get_soup
from datetime import datetime,timedelta
import re
import logging
import pandas as pd
def dateFromtext(i):
    match = re.search(r"(\d+)\s(\w+)\sago",i)
    if not match:
        return None
    value = int(match.group(1))
    measure = match.group(2)
    if measure == "day" or measure == "days":
        date = (datetime.now() - timedelta(days=value)).strftime("%Y-%m-%d")
        return date
    if measure == "week" or measure == "weeks":
        date = (datetime.now() - timedelta(weeks=value)).strftime("%Y-%m-%d")
        return date
    return None

def scrape_data(soup):
    job_data=[]
    job_dataCleaned = []
    try:
        # Extract all the fields from web
        import numpy as np
        timeMeasure = ["few hours ago","just now","today"]
        job_card=soup.find_all('div',class_="internship_meta experience_meta")
        
        jobcard_length = 0
        if job_card:
            for job in job_card:
                postedtime_tag = job.select_one("div.color-labels span")
                posted_time=postedtime_tag.text if postedtime_tag else None

                skills_tag = job.find_all('div',class_="skill_container")
                skills= skills_tag if skills_tag else None

                job_tag = job.find('a',id='job_title')
                jobb=job_tag.text if job_tag else None

                company_tag = job.find('p',class_="company-name")
                comp=company_tag.text if company_tag else None

                status_tag =job.find('div',class_="actively-hiring-badge")
                status=status_tag.text if status_tag else None

                sal_tag = job.find('span',class_="desktop")
                sal=sal_tag.get_text(strip = True) if sal_tag else None
                minsal = None
                maxsal = None
                if sal:
                    try:
                        if "-" in sal:
                            minsal,maxsal = sal.split('-')
                            minsal = int(minsal.replace(",","").replace("₹","").strip())
                            maxsal = int(maxsal.replace(",","").strip())
                        else:
                            minsal=maxsal = int(sal.replace(",","").replace("₹","").strip())
                    except ValueError:
                        minsal = None
                        maxsal = None

                else:
                        minsal,maxsal=None,None

                jobcard_length+=1
                #Extract the skills and store it on a list
                techstack=[skil.text for skil in skills ] if skills else None
                #Extract the location of the job
                location_tag = job.select_one("p.locations a")
                location = location_tag.get_text(strip=True) if location_tag else None
                
                jobPostedDate=dateFromtext(posted_time.lower()) if posted_time else None
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
                jdCleaned={"job":jobb.strip() if jobb else None,
                    "company":comp.strip() if comp else None,
                    "status":status.strip() if status else None,
                    "min_sal":minsal,
                    "max_sal":maxsal,
                    "TechStack":techstack ,
                    "Location":location.strip() if location else None,
                    "Scrape_time":scrape_time,
                    "posted_date":jobPostedDate
                    }
                job_dataCleaned.append(jdCleaned)
                job_data.append(jd)
        df = pd.DataFrame(job_data)
        df.to_csv("mycsv.csv",index= False)
            # print(jobPostedDate)
         
        return job_dataCleaned,job_data 
    
    except Exception as e:
        return job_dataCleaned,job_data 
        logging.error(e)
'''
1.select_one : is a css selctor
2.we have to use np.nan instead of None if we want to actualy insert null into the csv
3.(skills) : it is not a tuple, (skills,) :touple with 1 element
4.cur.lastrowid : the id of the last row which it has inserted
'''
# from fetcher import get_soup

# clened,raw = scrape_data(get_soup("https://internshala.com/jobs/ai-agent-development,backend-development-jobs/"))


# print(clened)
# print(raw)