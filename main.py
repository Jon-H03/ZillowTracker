from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
import lxml
import json
import time

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"

}

GOOGLE_SHEETS_URL = my_google_sheets_url
ZILLOW_URL = my_zillow_preferences_url


response = requests.get(ZILLOW_URL, headers=header)
soup = BeautifulSoup(response.text, "lxml")
housing = soup.find_all("script", attrs={"type": "application/json"})
rent_data = housing[1].text
rent_data = rent_data.replace("<!--", "")
rent_data = rent_data.replace("-->", "")
rent_data = json.loads(rent_data)


links = []
addresses = []
prices = []

for i in rent_data["cat1"]["searchResults"]["listResults"]:
    addresses.append(i["address"])
    links.append(f"https://www.zillow.com{i['detailUrl']}")
    try:
        prices.append(i["units"][0]["price"][:6])
    except KeyError:
        prices.append("Price Unavailable")
        continue

print(links)
print(addresses)
print(prices)

chrome_driver_path = Service("E:\Development\chromedriver.exe")
driver = webdriver.Chrome(service=chrome_driver_path)

driver.get(GOOGLE_SHEETS_URL)


for i in range(len(prices)):
    enter = driver.find_element(By.CSS_SELECTOR, "input.whsOnd.zHQkBf")
    time.sleep(1)
    enter.click()

    enter.send_keys(addresses[i]+Keys.TAB+prices[i]+Keys.TAB+links[i])

    submit = driver.find_element(By.CSS_SELECTOR, "span.NPEfkd.RveJvd.snByac")
    submit.click()
    time.sleep(1)

    restart = driver.find_element(By.TAG_NAME, "a")
    restart.click()
    time.sleep(1)
