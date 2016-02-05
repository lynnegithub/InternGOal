from selenium import webdriver
import bs4
import time
import math
import json
browser = webdriver.Firefox();
allJobIDS  = []
allJobInfo = []
term = "1165"
userID = "ja4green"
Password = ""
def login():
    #login using jeffs credentials
    browser.get('https://jobmine.ccol.uwaterloo.ca/psp/SS/EMPLOYEE/WORK/')
    time.sleep(3)
    browser.find_element_by_id("userid").send_keys(userID)
    browser.find_element_by_id("pwd").send_keys(Password)
    browser.find_element_by_id("login").find_element_by_xpath("//input[@type='submit'][@name='submit']").submit()
    time.sleep(3)


def preformSearch():
    # go to inquiry page
    browser.find_element_by_link_text('Job Inquiry').click()
    time.sleep(3)
    # get the proper frame
    frame = browser.find_element_by_id("ptifrmtgtframe")
    browser.switch_to_frame(frame)
    #make sure search is correct
    browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_WT_SESSION").clear()
    browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_WT_SESSION").send_keys(term)
    browser.find_element_by_id("UW_CO_JOBSRCH_UW_CO_WT_SESSION")
    browser.find_element_by_xpath("//select[@name='UW_CO_JOBSRCH_UW_CO_JS_JOBSTATUS']/option[text()='Apps Avail']").click()
    time.sleep(4)
    #search
    browser.find_element_by_id("UW_CO_JOBSRCHDW_UW_CO_DW_SRCHBTN").click()
    #get amount of jobs
    time.sleep(10)
    str = browser.find_element_by_class_name("PSGRIDCOUNTER").text
    jobAmount = [int(s) for s in str.split() if s.isdigit()][0]
    #cycle through each page getting all the jobs
    for x in range(0,int(jobAmount/25 - 1)):
        jobs = getJobs()
        for job in jobs:
            allJobIDS.append(job)
        browser.find_element_by_id("UW_CO_JOBRES_VW$hdown$0").click()
        time.sleep(5)

def getJobs():
    #get all the jobs on the page
    jobs = []
    soup = bs4.BeautifulSoup(browser.page_source)
    job_all = soup.findAll('span', id=lambda x: x and x.startswith('UW_CO_JOBRES_VW_UW_CO_JOB_ID'))
    # add them to the alljobs array
    for x in job_all:
        jobs.append(x.text)
    return jobs

def getJobInfo(jobID):
    browser.get("https://jobmine.ccol.uwaterloo.ca/psc/SS_2/EMPLOYEE/WORK/c/UW_CO_STUDENTS.UW_CO_JOBDTLS.GBL?UW_CO_JOB_ID=" + jobID)
    jobInfo= {}
    time.sleep(3)

    soup = bs4.BeautifulSoup(browser.page_source)

    jobInfo['job id'] = jobID
    jobInfo['employer'] = soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_EMPUNITDIV").text
    jobInfo['job title'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_JOB_TITLE").text
    jobInfo['work location'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_WORK_LOCATN").text
    try:
        # handle case where available openings doesnt exist
        jobInfo['available openings'] = int(soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_AVAIL_OPENGS").text)
    except ValueError:
        jobInfo['available openings'] = "Unknown"
    jobInfo['disciplines'] = soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_DESCR").text + ", " + soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_DESCR100").text
    jobInfo['job description'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_JOB_DESCR").text
    jobInfo['levels'] = soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_DESCR_100").text
    jobInfo['posting open date'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_CHAR_EDATE").text
    jobInfo['last day to apply'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_CHAR_DATE").text
    jobInfo['emp job #'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_EMPOWN_JOBNO").text
    jobInfo['grades'] = soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_MARKS_DRVD").text
    jobInfo['hiring process support'] = soup.find(id = "UW_CO_OD_DV2_UW_CO_NAME").text
    jobInfo['work term support'] = soup.find(id = "UW_CO_OD_DV2_UW_CO_NAME2").text
    jobInfo['comments'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_JOB_SUMMARY").text

    # get employer info
    browser.find_element_by_link_text("Employer Profile").click();
    soup = bs4.BeautifulSoup(browser.page_source)
    try:
        jobInfo['empUnit1'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_EMPLYR_NAME1").text
    except AttributeError:
        jobInfo['empUnit1'] = ""
    try: 
        jobInfo['empUnit2'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_EMPLYR_NAME1").text
    except AttributeError:
        jobInfo['empUnit2'] = ""
    try:
        jobInfo['empwebSite'] = soup.find(id = "UW_CO_JOBDTL_DW_UW_CO_URL").text
    except AttributeError:
        jobInfo['empwebSite'] = ""
    try:
        jobInfo['empDesc'] = soup.find(id = "UW_CO_JOBDTL_VW_UW_CO_PROFILE").text
    except AttributeError:
        jobInfo['empDesc'] = ""
    return jobInfo


def main():
    
    login()
    preformSearch()
    
    for ID in allJobIDS:
        info = getJobInfo(ID)
        allJobInfo.append(info)

    with open('job_data', 'w') as outfile:
        json.dump(allJobInfo, outfile, indent=4)
main()
