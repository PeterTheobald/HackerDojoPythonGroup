import requests

def get_jokes():
    url = "https://www.reddit.com/r/jokes/new.json?limit=100"
    headers = {'User-agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print('Failed to fetch jokes:', response.status_code)
        return

    jokes = []
    for post in response.json()['data']['children']:
        joke = {
            'title': post['data']['title'],
            'body': post['data']['selftext']
        }
        jokes.append(joke)

    return jokes

# Example usage
jokes = get_jokes()
if jokes:
    for joke in jokes:
        print('Title:', joke['title'])
        print('Body:', joke['body'])
        print()
