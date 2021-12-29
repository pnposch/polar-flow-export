from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
import time
import sys
import os
import json
import chromedriver_binary  # Adds chromedriver binary to path

FLOW_URL = "https://flow.polar.com"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")

regex = r"filename=\"([\w._-]+)\""

with open("config.json") as json_data_file:
    cfg = json.load(json_data_file)



def login(driver, username, password):
    driver.get("%s/login" % FLOW_URL)
    driver.find_element_by_name("email").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_id("login").click()

def get_exercise_ids(driver, year, month):
    driver.get("%s/diary/%s/month/%s" % (FLOW_URL, year, month))
    time.sleep(2)
    ids = map(
        # The subscript removes the prefix
        lambda e: e.get_attribute("href")[len("https://flow.polar.com/training/analysis/"):],
        driver.find_elements_by_xpath("//div[@class='event event-month exercise']/a")
    )
    return ids

def export_exercise(driver, exercise_id, output_dir):
    def _load_cookies(session, cookies):
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

    s = requests.Session()
    _load_cookies(s, driver.get_cookies())

    r = s.get("%s/api/export/training/tcx/%s" % (FLOW_URL, exercise_id))
    filename = re.search(regex, r.headers['Content-Disposition']).group(1)
    if os.path.exists(os.path.join(output_dir, filename)):
        print("File existed. redownloading %s" % filename)
        
    with open(os.path.join(output_dir, filename), 'w') as outfile:
     outfile.write(r.text)
    print("Wrote file %s" % filename)


if __name__ == "__main__":
    username = cfg["username"]
    password = cfg["password"]
    month = 12
    year = cfg["year"]
    output_dir = cfg["output_dir"]
    driver = webdriver.Chrome(options=chrome_options)
    print("Chrome initialized")
    try:
        login(driver, username, password)
        time.sleep(5)
        exercise_ids = get_exercise_ids(driver, year, month)
        for ex_id in exercise_ids:
            export_exercise(driver, ex_id, output_dir)
    finally:
        driver.quit()
        print("Finished with %s / %s" % (month, year) )
