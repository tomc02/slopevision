import re
import traceback

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from django.utils import timezone  # To get the current timestamp
import pytz

def find_video_url(page_url):
    """
    Fetch the given page URL and find the first .mp4 video URL in the page source.

    :param page_url: URL of the webpage to scan
    :return: The first .mp4 video URL found or None if not found
    """
    if 'chatanagruni' in page_url:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors")
        driver = webdriver.Chrome(chrome_options)
        img_urls = {}
        try:
            driver.get(page_url)
            time.sleep(5)  # Wait for the page to load

            # Find <img> elements with the class 'fancybox-image' and get the 'src' attribute
            img_elements = driver.find_elements(By.CLASS_NAME, 'fancybox-image')
            if img_elements:
                img_url = img_elements[0].get_attribute('src')
                return img_url
            else:
                return None
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred: {e}")
            return None
        finally:
            driver.quit()

    else:
        try:
            # Fetch the page content
            response = requests.get(page_url, verify=False)
            response.raise_for_status()  # Raise an error for bad status codes

            # Search for the first .mp4 URL in the page source
            mp4_pattern = re.compile(r'https?://[^\s\'"]+\.mp4')

            # Use search() to find the first match, return immediately after finding it
            match = mp4_pattern.search(response.text)

            if match:
                return match.group(0)  # Return the matched URL (first found)
            else:
                print("No .mp4 URL found on the page.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the page: {e}")
            return None


def get_image_urls(image_ids):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    driver = webdriver.Chrome(chrome_options)
    img_urls = {}
    try:
        driver.get("https://meteo.hzs.sk/")
        time.sleep(15)  # Wait for the page to load
        camera_button = driver.find_elements(By.CLASS_NAME, "nav-buttons")[1]

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(camera_button)
        )

        camera_button.click()
        time.sleep(5)  # Wait for the images to load

        for image_id in image_ids:

            img_element = driver.find_element(By.ID, image_id)
            img_url = img_element.get_attribute('src')
            img_urls[image_id] = img_url

        return img_urls

    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred: {e}")
        return None

    finally:
        driver.quit()

def save_webcam_url(webcam, url):
    if url:
        webcam.source_url = url
        # Update description with the video URL and the current timestamp
        prague_tz = pytz.timezone('Europe/Prague')
        timestamp = timezone.now().astimezone(prague_tz).strftime('%B %d, %Y at %I:%M %p')
        webcam.description = f"Updated at: {timestamp}"
        webcam.save()
        print(f"Updated {webcam.name} with video URL: {url}")
    else:
        print(f"No video URL found for {webcam.name}")
