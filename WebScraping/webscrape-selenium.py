from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def main():
    # Set up the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Navigate to Airbnb
        driver.get("https://www.airbnb.com")

        # Wait for the page to load
        time.sleep(2)

        # Locate the search box (Inspect the page to find the correct input name or ID)
        search_box = driver.find_element(By.NAME, "query")
        search_box.send_keys("Mountain View, CA")

        # Submit the search box form
        search_box.send_keys(Keys.ENTER)
        time.sleep(5)  # Wait for the search results to load

        # Collect listing titles (inspect the page to find the correct class names or element tags)
        listings = driver.find_elements(By.CLASS_NAME, "_bzh5lkq")
        locations = [listing.text for listing in listings]

        # Print all the locations found
        print("Available Locations in Mountain View, CA:")
        for location in locations:
            print(location)

    finally:
        # Close the driver
        driver.quit()

if __name__ == "__main__":
    main()
