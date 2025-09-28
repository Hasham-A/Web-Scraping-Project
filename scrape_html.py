from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scraper(name, password,role):

    driver = webdriver.Chrome()
    #--------give the website here-------
    driver.get("https://www.linkedin.com/login")
    wait = WebDriverWait(driver, 10)

    #------ put login detials in the following "send_keys('write here')" -----
    wait.until(EC.presence_of_element_located((By.ID,'username'))).send_keys(name)
    wait.until(EC.presence_of_element_located((By.ID,'password'))).send_keys(password,Keys.RETURN)

    # click on the job button
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Jobs'))).click()

    #----Search role-----
    search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='typeahead-input']")))
    search_box.clear()
    search_box.send_keys(role,Keys.RETURN)

                                #------click on the Dateposted filter-----
    date_filter_button = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "searchFilter_timePostedRange")))
    date_filter_button.click()

    #                               -----click on the past 24 hours-----
    past_week = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//label[contains(., "Past week")]')
    ))
    past_week.click()


    file = 0
    for i in range(0,600, 25):
        driver.get(f'https://www.linkedin.com/jobs/search/?keywords=full%20stack%20developer&origin=JOBS_HOME_KEYWORD_AUTOCOMPLETE&start={i}')
        time.sleep(5)
        
                        #----- find job_cards and then click to extract html------
        job_list = driver.find_elements(By.CSS_SELECTOR, 'li.ember-view')
        for j in range(len(job_list)):
            driver.implicitly_wait(8)
            job_list[j].click()
      
            job_details = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.jobs-search__job-details--container')))
            time.sleep(5)

            d =  job_details.get_attribute('outerHTML')

            with open(f'Selenium/newjobs/{file}_jobs.html', 'w', encoding='utf-8') as f:
                f.write(d)

            file +=1
    driver.quit()

#-----user login----
#  log in manually once here.
name = input('Enter your username of linkedin:').strip()
password = input('Enter password:')
role = input('Enter job title:')
scraper(name,password,role)