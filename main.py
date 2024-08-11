from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
import requests
from util import ask_for_url, wait_for_page_load_and_ajax
import time


def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 10)
    # wait.until(lambda driver: driver.execute_script(
    #     "return jQuery.active == 0"))
    wait.until(lambda driver: driver.execute_script(
        "return document.readyState == 'complete'"))


# Create a directory to save the downloaded files
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

# Initialize WebDriver (e.g., Chrome)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Enable headless mode
driver = webdriver.Chrome(options=options)

url = ask_for_url()
# Navigate to the webpage
driver.get(url)
wait_for_page_load_and_ajax(driver)
time.sleep(1)

# Find all elements with TAG_NAME as 'a'
all_links = driver.find_elements(By.TAG_NAME, "a")
final_links = []

# Extract href attributes
for link in all_links:
    href = link.get_attribute("href")
    if href.endswith("pdf"):
        final_links.append(href)

# Start processing downloading
for link in final_links:
    try:
        response = requests.get(link)
        if response.status_code == 200:
            # Extract the filename from the URL
            filename = os.path.join(download_dir, os.path.basename(link))
            with open(filename, "wb") as f:
                f.write(response.content)
                print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {link}")
    except Exception as e:
        print(f"Error downloading {link}: {e}")

# Close the WebDriver
driver.quit()
