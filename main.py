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

GOOGLE_SHEETS_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeRlP-L8yrF2aEGMwUnin230wd8tf1ELpOW2UFogRCGQPwSFA/viewform?usp=pp_url"
ZILLOW_URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22usersSearchTerm%22%3A%22Portland%2C%20OR%22%2C%22mapBounds%22%3A%7B%22west%22%3A-123.00571444677735%2C%22east%22%3A-122.38567355322266%2C%22south%22%3A45.2777852256197%2C%22north%22%3A45.831669610234385%7D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A310199%2C%22max%22%3A387749%7D%2C%22mp%22%3A%7B%22min%22%3A1600%2C%22max%22%3A2000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22lau%22%3A%7B%22value%22%3Atrue%7D%2C%22parka%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22customRegionId%22%3A%226cdcc634edX1-CRsgdw3179mg72_13hj4h%22%2C%22pagination%22%3A%7B%7D%2C%22mapZoom%22%3A11%7D"


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