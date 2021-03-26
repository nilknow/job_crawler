import csv
import json
import time
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.webdriver.support.wait import WebDriverWait


def open_chrome():
    driver = webdriver.Chrome("./driver/chromedriver")
    return driver


def get_job_detail(driver: WebDriver, url: str):
    post_date_xpath = "//ppc-content[normalize-space()='Date posted']/../following-sibling::span[1]"

    # the chrome driver will wait for a page to load by default via .get() method.
    driver.get(url)
    WebDriverWait(driver, 10).until(presence_of_all_elements_located((By.XPATH, post_date_xpath)))
    post_date = driver.find_element_by_xpath(post_date_xpath)
    employment_type = driver.find_element_by_xpath(
        "//ppc-content[normalize-space()='Employment type']/../following-sibling::span[1]")
    job_info_list = driver.find_elements_by_class_name("jd-info")
    return (url.split("/")[-1],  # job title
            url,  # job link
            post_date.text,
            employment_type.text,
            job_info_list[0].text,  # job description
            job_info_list[1].find_element_by_tag_name("p").text,  # job responsibilities
            job_info_list[2].find_element_by_tag_name("p").text)  # qualifications


def safe_close(driver: WebDriver):
    try:
        driver.close()
    except Exception:
        print('Chrome is already closed')


if __name__ == '__main__':
    chrome = open_chrome()
    with open('./job_links.json', 'r') as f:
        links: List = json.load(f)
    with open('./job_detail.csv', 'a') as csvF:
        writer = csv.writer(csvF)
        writer.writerow(
            ("job", "link", "post date", "employment type", "description", "responsibilities", "qualifications"))
        # links = ["https://careers.microsoft.com/us/en/job/916402/Software-Engineer-SharePoint-Service-Fabric"]
        for index, link in enumerate(links):
            if index < 210:
                continue
            print(f"start download index: {index}")
            print(f"start download from : {link}")
            try:
                detail_tuple = get_job_detail(chrome, link)
            except:
                print(f"index {index} wasn't downloaded")
                with open('./failedurl.txt', 'a+') as ff:
                    ff.write(f"{index}\t{link}")
                continue
            writer.writerow(detail_tuple)
            print(f"index {index} was downloaded")
