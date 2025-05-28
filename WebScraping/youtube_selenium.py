from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

VIDEO_ID='_bwyY5XwmEU'

def scrape_comments(video_url, num_comments=10, max_scrolls=10):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(video_url)

    # wait until at least one comment thread appears
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-comment-thread-renderer"))
    )

    scrolls = 0
    comments = []
    while len(comments) < num_comments and scrolls < max_scrolls:
        driver.execute_script("window.scrollBy(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        comments = driver.find_elements(By.CSS_SELECTOR, "ytd-comment-thread-renderer")
        scrolls += 1

    results = []
    for c in comments[:num_comments]:
        author = c.find_element(By.CSS_SELECTOR, "#author-text span").text.strip()
        text = c.find_element(By.CSS_SELECTOR, "#content-text").text.strip()
        results.append((author, text))

    driver.quit()
    return results

if __name__ == "__main__":
    for author, text in scrape_comments(f"https://www.youtube.com/watch?v={VIDEO_ID}"):
        print(f"{author}: {text}")

