import requests

url = "https://www.cnbc.com/2025/05/05/cnbcs-official-global-soccer-team-valuations-2025.html"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers)
print(resp.content)



