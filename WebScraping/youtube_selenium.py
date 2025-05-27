from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def scrape_comments(video_url, num_comments=10):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get(video_url)
    time.sleep(5)  # wait for page to load
    
    # scroll to load comments
    driver.execute_script("window.scrollTo(0, 600);")
    time.sleep(3)
    
    # keep scrolling until enough comments are loaded
    comments = []
    while len(comments) < num_comments:
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)
        comments = driver.find_elements(By.CSS_SELECTOR, 'ytd-comment-thread-renderer')
    
    results = []
    for c in comments[:num_comments]:
        author = c.find_element(By.CSS_SELECTOR, '#author-text span').text.strip()
        text = c.find_element(By.CSS_SELECTOR, '#content-text').text.strip()
        results.append((author, text))
    
    driver.quit()
    return results

if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=_bwyY5XwmEU'
    for author, text in scrape_comments(video_url):
        print(f"{author}: {text}")

