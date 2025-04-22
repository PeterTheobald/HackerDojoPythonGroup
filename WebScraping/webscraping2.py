import requests
from bs4 import BeautifulSoup

# URL of the webpage you want to scrape
url = 'https://www.qrmobileorder.com/'

# Send an HTTP request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Print the entire HTML content of the page
    print(soup.prettify())
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
