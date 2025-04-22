import requests

# URL of the webpage you want to scrape
url = 'https://www.qrmobileorder.com/'

# Send an HTTP request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print(response.content)
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
