import chromedriver_binary  # Adds chromedriver binary to path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import re
import time
import sys
import os
import json

FLOW_URL = "https://flow.polar.com"

chrome_options = Options()
chrome_options.add_argument("--headless") # disable to show whats happening
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--remote-debugging-port=9222")  # this
chrome_options.add_argument("--no-sandbox") # needed in docker


with open("config.json") as json_data_file:
    cfg = json.load(json_data_file)

username = cfg["username"]
password = cfg["password"]
month = cfg["month"]
year = cfg["year"]
output_dir = cfg["output_dir"]


def login(driver, username, password):
    driver.get("%s/login" % FLOW_URL)
    driver.find_element(By.NAME,"email").send_keys(username)
    driver.find_element(By.NAME,"password").send_keys(password)
    driver.find_element(By.ID,"login").click()
    print("Logged in")

def get_exercise_ids(driver, year, month):
    driver.get("%s/diary/%s/month/%s" % (FLOW_URL, year, month))
    time.sleep(2)
    ids = map(
        # The subscript removes the prefix
        lambda e: e.get_attribute("href")[len("https://flow.polar.com/training/analysis/"):],
        driver.find_elements(By.XPATH, "//div[@class='event event-month exercise']/a")
    )
    print("Exercise List downloaded")
    return ids


def _load_cookies(session, cookies):
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])


if __name__ == "__main__":
    try:
        (month, year) = sys.argv[1:]
    except ValueError:
        sys.stderr.write(("You can provide: %s <month> <year> here or in config.json \n") % sys.argv[0])
    print("Fetching %s / %s" % (month, year))
    driver = webdriver.Chrome(options=chrome_options)
    print("Chrome initialized")
    try:
        login(driver, username, password)
        time.sleep(5)
        exercise_ids = list(get_exercise_ids(driver, year, month))
        s = requests.Session()
        _load_cookies(s, driver.get_cookies())

        for ex_id in exercise_ids:
            r = s.get("%s/api/export/training/tcx/%s" % (FLOW_URL, ex_id))
            filename = re.search(r"filename=\"([\w._-]+)\"", r.headers['Content-Disposition']).group(1)
            with open(os.path.join(output_dir, filename), 'w') as outfile:
                outfile.write(r.text)
            print("Wrote file %s" % filename)

    finally:
        driver.quit()
        print("Finished with %s / %s" % (month, year) )
