# Web Scraping

## Why? 
- Competitive analysis
- market research
- price monitoring

## Should we use web scraping?
- First check if the website has a clean download of the data you want in JSON, YAML, CSV etc.
eg: https://dumps.wikimedia.org/
https://www.reddit.com/dev/api/
- Check if it is legal and/or approved to web scrape the site. "/robots.txt" ( http://www.ebay.com/robots.txt )

## Challenges
- Websites can change their layout and break brittle scrapers
- Websites use HTML. Tag based hierarchical format like XML. Hard to parse w text functions and even regex.
- Some "Single-Page-Apps" (SPAs) like gmail load empty pages and then fill them in with data ("hydration") with Javascript calls to a backend database or API.

## How?
Understanding HTML and the DOM
Example, restaurant near us:
https://www.qrmobileorder.com/

1. Requests + regex (raw HTML)
2. Beautiful Soup (parses HTML, selectors)
3. Mechanical Soup (interacts w HTML, no javascript)
4. Selenium (remote controls browser, full javascript)

first_div = soup.find('div')
link = soup.find('a', class_='myClass')

sandwiches = soup.find( 'div', class_ = 'bold f18')

all_links = soup.find_all('a')
all_divs = soup.find_all('div', id='myId')

items = soup.select('.myClass') # by class
content = soup.select('#content') # by id
nested_items = soup.select('div #someId ul.items li') # by nested combo

parent_div = link.parent
child_elements = soup.find('div').contents
for child in soup.find('div').children:
   print(child)
next_sibling = soup.find('h1').next_sibling
previous_sibling = soup.find('h1').previous_sibling



