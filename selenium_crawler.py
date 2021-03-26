import json
import os
from typing import List

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# use chrome driver to crawler
# URL for job descriptions links
START_URL = "https://careers.microsoft.com/us/en/search-results?qcity=Suzhou&qstate=Jiangsu&qcountry=China"
DRIVER_PATH = "./driver/chromedriver"

# method to wait for elements to be loaded on webpage


class wait_for_all(object):
    def __init__(self, methods: List):
        self.methods = methods

    def __call__(self, driver):
        try:
            for method in self.methods:
                if not method(driver):
                    return False
            return True
        except StaleElementReferenceException:
            return False


# get all job descriptions links on every page
def add_job_link_and_click_next(jobLinkQueue: List[str]):
    NEXT_BUTTON_XPATH = "//ppc-content[normalize-space()='Next']/.."
    # wait for the loading of this page
    methods = []
    methods.append(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, "job-title")))
    try:
        WebDriverWait(driver, 5).until(wait_for_all(methods))
    except Exception:
        driver.quit()

    # save job detail links in this page
    jobTitles = driver.find_elements_by_class_name("job-title")
    [print(f"job <<{elem.text}>> was added") for elem in jobTitles]
    jobDetailLinks: List[WebElement] = driver.find_elements_by_xpath(
        '//span[@class="job-title"]/..')
    [jobLinkQueue.append(elem.get_attribute('href'))
     for elem in jobDetailLinks]

    # print jobs already saved
    job_count_span: WebElement = driver.find_elements_by_class_name(
        "job-number")[2]
    print(f"there are already {job_count_span.text} jobs")

    # check if there is one more page
    methods.append(EC.presence_of_all_elements_located(
        (By.XPATH, NEXT_BUTTON_XPATH)))
    try:
        WebDriverWait(driver, 5).until(wait_for_all(methods))
    except Exception:
        driver.close()
        return False
    driver.find_element_by_xpath(
        NEXT_BUTTON_XPATH).click()
    return True


def safe_close_driver(driver: WebDriver):
    try:
        driver.close()
        print("driver successfully closed.")
    except Exception:
        print("driver already closed.")


def dump_to_json_file(data: List, path: str):
    with open(path, "w") as f:
        json.dump(data, f)


def say_to_me(text: str):
    os.system(f"spd-say {text}")


def download_job_links():
    jobLinkQueue = []
    driver.get(START_URL)
    page: int = 0
    while(add_job_link_and_click_next(jobLinkQueue)):
        page = page+1
        print(f"this is page {page}")
        pass
    print(f"the numbers of job is now {len(jobLinkQueue)}")
    safe_close_driver(driver)
    dump_to_json_file(jobLinkQueue, "./job_links.json")
    say_to_me('"your web crawler has finished"')


if __name__ == '__main__':
    driver = webdriver.Chrome(DRIVER_PATH)
    download_job_links()
