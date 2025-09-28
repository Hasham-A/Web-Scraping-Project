import pandas as pd
from bs4 import BeautifulSoup
import os

d = {'Job Title': [], 'Link': [], 'WorkType': [], 'JobType':[], 'Company': [], 'Company Location': []}

#-----function to extract work and job types-----
def extract_work_and_job_type(valid_work_locations, valid_job_types, work_type, job_type, strongs):
    for s in strongs:
        text = s.get_text(strip=True)
        if not work_type and text in valid_work_locations:
            work_type = text
        if not job_type and text in valid_job_types:
            job_type = text
    return work_type,job_type


#-----function to extract company name-----
def find_company(soup):
    c = soup.find('div', class_='job-details-jobs-unified-top-card__company-name')
    if c is not None:
        a_tag = c.find('a')
        if a_tag is not None:
            company = a_tag.get_text()
            return company
    return ""
#-----function to extract company location-----
def location(soup):
    company_location = ""
    div = soup.find('div', class_='job-details-jobs-unified-top-card__primary-description-container')
    if div:
        span = div.find('span', class_='tvm__text tvm__text--low-emphasis')
        if span:
            location = span.get_text()
            company_location = ' '.join(location.split())
    return company_location

#-----function to extract title and link-----
def find_title_and_link(soup):
    t = soup.select('div.job-details-jobs-unified-top-card__title-container')
    #Title
    for elems in t:
        h2_elem = elems.find('h2')
        if h2_elem is not None:
            title = h2_elem.get_text().strip().lstrip()
        else:
            title = ""
    
        #link
        l = elems.find('a')
        if l is not None and l.has_attr('href'):
            link = 'https://www.linkedin.com' + l['href']
        else:
            link = ""
        return title, link  # Return immediately after first found
    return "", ""  # Return empty if nothing found


#-----main function to collect data from html files-----
def job_collection(d, extract_work_and_job_type, find_company, location, find_title_and_link):
    for file in (os.listdir('Selenium/newjobs')): 
        try:
            with open(f'Selenium/newjobs/{file}', 'r', encoding='utf-8') as f:
                html_doc = f.read()

            soup = BeautifulSoup(html_doc, 'lxml')

        #find Title, link, work_type
            title, link = find_title_and_link(soup)
          

        #find work_type & job_type
            valid_work_locations = {"Remote", "On-site", "Hybrid"}
            valid_job_types = {"Full-time", "Part-time", "Contract", "Temporary", "Internship", "Volunteer"}
            prefs = soup.find('div', class_='job-details-fit-level-preferences')
            work_type = ""
            job_type = ""
            if prefs:
                strongs = prefs.find_all('strong')
                work_type, job_type = extract_work_and_job_type(valid_work_locations, valid_job_types, work_type, job_type, strongs)

        #find company
            company = find_company(soup)
        
        #company Location
            company_location = location(soup)
    

            d['Job Title'].append(title)
            d['Link'].append(link)
            d['WorkType'].append(work_type)
            d['JobType'].append(job_type)
            d['Company'].append(company)
            d['Company Location'].append(company_location)
           
        except Exception as e:
                print(e)


    df = pd.DataFrame.from_dict(d)
    df = df.dropna(how='any')
    df.to_csv('New Jobs Data.csv')


job_collection(d, extract_work_and_job_type, find_company, location, find_title_and_link)