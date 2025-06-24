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
import asyncio
from playwright.async_api import async_playwright


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


async def get_image_urls(image_ids):
    img_urls = {}

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://meteo.hzs.sk/", wait_until='load')
            

            await page.wait_for_timeout(5000)  # Wait 5 seconds for images to load
            
            for image_id in image_ids:
                img_element = await page.query_selector(f"#{image_id}")
                if img_element:
                    img_url = await img_element.get_attribute('src')
                    img_url = "https://meteo.hzs.sk" + img_url if img_url and not img_url.startswith('http') else img_url
                    img_urls[image_id] = img_url
                else:
                    img_urls[image_id] = None  # or handle missing element differently

            await browser.close()
            return img_urls

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def get_image_urls_sync(image_ids):
    return asyncio.run(get_image_urls(image_ids))

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
