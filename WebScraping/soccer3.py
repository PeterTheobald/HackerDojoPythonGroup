import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Note: If you don't have chromium installed,
# Need to apt install chromium-browser
# apt install -y \
#  chromium-browser chromium-chromedriver \
#  libnss3 libgconf-2-4 libxss1 libasound2 \
#  libatk1.0-0 libgtk-3-0 libx11-xcb1 \
#  libdbus-glib-1-2 libxtst6 fonts-liberation
# And need to run with a graphic UI (X server) running

url = "https://www.cnbc.com/2025/05/05/cnbcs-official-global-soccer-team-valuations-2025.html"
opts = webdriver.ChromeOptions()
# use new headless mode
opts.add_argument("--headless=new")
# required for Linux
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--disable-gpu")
opts.add_argument("--remote-debugging-port=0")
# point to your binary if needed:
#opts.binary_location = "/usr/bin/chromium-browser"
opts.add_argument("--user-data-dir=/tmp/selenium-profile")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts)
driver.get(url)
# wait for JS to finish (e.g. via WebDriverWait)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

table = soup.find("table")
rows = table.find_all("tr")

data = []
for tr in rows[1:]:
    cols = tr.find_all("td")
    if len(cols) >= 5:
        data.append({
            "team":    cols[0].get_text(strip=True),
            "country": cols[1].get_text(strip=True),
            "league":  cols[2].get_text(strip=True),
            "value":   cols[3].get_text(strip=True),
            "revenue": cols[4].get_text(strip=True)
        })

df = pd.DataFrame(data)
print(df)


driver.quit()


