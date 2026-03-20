
def scrape_data(soup):
    from datetime import datetime
    import sqlite3
    #Connect to the Database file 
    conn=sqlite3.connect("jobs.db")
    cur=conn.cursor()
    # Extract all the fields from web
    import numpy as np
    job_card=soup.find_all('div',class_="internship_meta experience_meta")
    job_data=[]
    jobcard_length = 0
    for job in job_card:
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

        scrape_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      
        jd={"job":jobb,
            "company":comp,
            "status":status,
            "Salary":sal,
            "TechStack":techstack ,
            "Location":location ,
            "Scrape_time":scrape_time
            }
        job_data.append(jd)
       
    
        
       
    return job_data
'''
1.select_one : is a css selctor
2.we have to use np.nan instead of None if we want to actualy insert null into the csv
3.(skills) : it is not a tuple, (skills,) :touple with 1 element
4.cur.lastrowid : the id of the last row which it has inserted
'''