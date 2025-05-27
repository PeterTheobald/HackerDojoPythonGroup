import os
import sys
from googleapiclient.discovery import build

VIDEO_ID = '_bwyY5XwmEU'

API_KEY = os.environ['YOUTUBE_API_KEY']
if not API_KEY:
    print('Error: YOUTUBE_API_KEY environment variable not set.')
    sys.exit(1)

youtube = build('youtube', 'v3', developerKey=API_KEY)

# fetch top‐level comments
threads = youtube.commentThreads().list(
    part='snippet',
    videoId=VIDEO_ID,
    maxResults=10,
    textFormat='plainText'
).execute()

for thread in threads.get('items', []):
    top = thread['snippet']['topLevelComment']
    tid = top['id']
    author = top['snippet']['authorDisplayName']
    text = top['snippet']['textDisplay']
    print(f"{author}: {text}")

    # fetch all replies for this top‐level comment
    next_token = None
    while True:
        replies = youtube.comments().list(
            part='snippet',
            parentId=tid,
            maxResults=100,
            pageToken=next_token
        ).execute()
        for reply in replies.get('items', []):
            r = reply['snippet']
            print(f"\t{r['authorDisplayName']}: {r['textDisplay']}")
        next_token = replies.get('nextPageToken')
        if not next_token:
            break

