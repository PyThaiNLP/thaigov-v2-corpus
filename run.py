# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import codecs
import uuid
import re
import time
import datetime, pytz
import os

# --- Setup Selenium WebDriver for Firefox ---
# This configures Firefox to run in headless mode (without a visible browser window)
# firefox_options = Options()
# firefox_options.add_argument("--headless")
# # Initialize the Firefox driver
# Make sure geckodriver is in your PATH or specify its location
# Example: driver = webdriver.Firefox(executable_path='/path/to/geckodriver', options=firefox_options)
# driver = webdriver.Firefox(options=firefox_options)
from selenium import webdriver
# Initialize ChromeOptions
options = webdriver.ChromeOptions()

# Set preferences to block images and JavaScript
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.default_content_setting_values.javascript": 2
}
options.add_experimental_option("prefs", prefs)


driver = webdriver.Chrome(options=options)

# --- Directory and File Setup ---
tz = pytz.timezone('Asia/Bangkok')
now1 = datetime.datetime.now(tz)

# Create nested directories for the current year, month, and day
f = os.path.join("data", str(now1.strftime('%Y')))
if not os.path.exists(f):
    os.makedirs(f)
f = os.path.join(f, str(now1.strftime('%m')))
if not os.path.exists(f):
    os.makedirs(f)
f = os.path.join(f, str(now1.strftime('%d')))
if not os.path.exists(f):
    os.makedirs(f)

# --- Read the last scraped number ---
try:
    with open("last_num.txt", "r", encoding="utf-8-sig") as file:
        i = int(file.read().strip())
except FileNotFoundError:
    print("last_num.txt not found. Starting from 1.")
    i = 1 # Start from 1 if the file doesn't exist
except ValueError:
    print("Invalid content in last_num.txt. Starting from 1.")
    i = 1 # Start from 1 if the content is not a valid number

# --- Main Scraping Loop ---
i2 = 1
i_backup = i
e = 0 # Error counter to stop the loop after too many consecutive failures
data = {}

print("Starting scraper...")
try:
    while e < 50:
        url = "https://www.thaigov.go.th/news/contents/details/" + str(i)
        try:
            # Use Selenium to get the page
            driver.get(url)
            # A short delay can help ensure the page loads fully
            time.sleep(1)
            text = driver.page_source

            # Check if the page is a valid news page
            if "<title>รัฐบาลไทย-ข่าวทำเนียบรัฐบาล-</title>" not in text:
                soup = BeautifulSoup(text, "lxml")
                title = soup.title.text
                
                # Double-check the title to ensure it's a real article
                if title != "รัฐบาลไทย-ข่าวทำเนียบรัฐบาล-":
                    article_div = soup.find('div', {'class': 'border-normal clearfix'})
                    collection_span = soup.find('span', {'class': 'Circular headtitle-2 font_level6 color2 col-xs-9 remove-xs'})

                    # Proceed only if the main content elements are found
                    if article_div and collection_span:
                        article = article_div.text
                        collection = collection_span.text
                        collection = re.sub(r'[\?\.!/\;:]', '', collection) # Clean collection name

                        # Clean up article text
                        _text = ''
                        for line in article.split('\n'):
                            line = line.strip()
                            if line:
                                _text = _text + '\n' + line
                        article = _text.strip()
                        
                        all_data = title + "\n\n" + article + "\n\nที่มา : " + url
                        
                        # Handle file naming and saving
                        if collection not in data:
                            data[collection] = 1
                        
                        filename = f"{collection}_{data[collection]}_{uuid.uuid4()}.txt"
                        filepath = os.path.join(f, filename)
                        
                        with codecs.open(filepath, "w", "utf-8") as temp:
                            temp.write(all_data)
                        
                        data[collection] += 1
                        print(f"Saved: {title}\tURL: {url}")
                        
                        i2 += 1
                        e = 0 # Reset error counter on success
                        i += 1
                        i_backup = i
                    else:
                        print(f"Skipping {url} - Missing article content or collection info.")
                        e += 1
                        i += 1
                else:
                    e += 1
                    i += 1
            else:
                print(f"Page {i} is not a valid news article.")
                e += 1
                i += 1
        except Exception as ex:
            print(f"An error occurred while processing {url}: {ex}")
            e += 1
            i += 1
finally:
    # --- Cleanup and Finalize ---
    print("\nScraping finished. Closing browser.")
    # Make sure to quit the driver to close the browser instance
    driver.quit()

    # Save the last successful number
    with open("last_num.txt", "w", encoding="utf-8") as f_out:
        f_out.write(str(i_backup))
    print(f"Last successful article number saved: {i_backup}")