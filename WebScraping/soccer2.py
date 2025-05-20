# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "bs4",
#     "pandas",
#     "requests",
# ]
# ///
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.cnbc.com/2025/05/05/cnbcs-official-global-soccer-team-valuations-2025.html"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.content, "html.parser")

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


