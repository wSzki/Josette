# ==============================================================================
# ---------------------------------- IMPORTS -----------------------------------
# ==============================================================================

import os
import telebot
import sys
import subprocess
from datetime import datetime


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Playwright
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
import shutil

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Db update
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
import requests
from bs4 import BeautifulSoup
import string

# ==============================================================================
# ------------------------------------ CORE ------------------------------------
# ==============================================================================

BOT_TOKEN = "6828287802:AAEMo3QZsWPTwQ8FcfUlCGtaPXQD3x5tOdA"
bot = telebot.TeleBot(BOT_TOKEN)

# ==============================================================================
# ----------------------------------- UPDATE -----------------------------------
# ==============================================================================

# Function to fetch and store <a> elements in a file
def fetch_and_store_links():
    filename = "database.txt"
    # Start a session to keep cookies
    session = requests.Session()

    # The cookie name and value you want to set
    cookie_name = 'disclaimer_accepted'
    cookie_value = 'true'

    # Set the cookie in the session
    session.cookies.set(cookie_name, cookie_value)

    # Get the current date in the format you prefer (e.g., YYYY-MM-DD)
    current_date = datetime.now().strftime("%Y-%m-%d")
    new_filename = "{0}_{1}.txt".format(filename, current_date)

    # Backup existing database
    os.rename(filename, new_filename)

    # Open the file to write
    with open(filename, 'w', encoding='utf-8') as file:
        # Loop over every letter in the alphabet
        for letter in string.ascii_lowercase:
            # Format the URL for the current letter
            url = f'https://www.adrreports.eu/tables/substance/{letter}.html'

            # Make a GET request to the page
            response = session.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Initialize BeautifulSoup to parse the page content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all <tr> elements
                table_rows = soup.find_all('tr')

                # Iterate over each <tr> element and find all <a> tags within it
                for tr in table_rows:
                    # Find all <a> tags within this <tr> tag
                    a_tags = tr.find_all('a')
                    for a in a_tags:
                        # Write the text and the href attribute of each <a> tag to the file
                        file.write(f"{a.text}, {a.get('href')}\n")
            else:
                return letter
    return None

@bot.message_handler(commands=['update'])
def upload(message):
    chat_id   = message.chat.id
    letter = fetch_and_store_links()
    if (letter):
        bot.send_message(chat_id, "❌ Error updating database at letter " + letter)
        return
    bot.send_message(chat_id, "✅ Database updated")



# ==============================================================================
# --------------------------------- FUNCTIONS ----------------------------------
# ==============================================================================

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Find url from local file
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def find_url_with_substring(drug):
    filename = 'database.txt'
    with open(filename, 'r') as file:
        for line in file:
            if drug.upper() in line.upper():
                url = line.strip().split(',')[-1].strip()
                return url
    return None

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Find all matches                                          
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def find_lines_with_substring(drug):
    filename = 'database.txt'
    matching_lines = []
    with open(filename, 'r') as file:
        for line in file:
            if drug.upper() in line.upper():
                # Find the start of the URL (assuming it starts with "http")
                url_index = line.find('http')
                if url_index != -1:
                    # Keep only the part of the line before the URL
                    drug_info = line[:url_index].strip()
                    matching_lines.append(drug_info)
    return matching_lines


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Send file to user
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def send_xslx(chat_id, drug):
    try:
        os.rename(drug, drug+'.xlsx')
        file_path = '/script/'+drug+'.xlsx'
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id, file)
        return 0
    except Exception as e:
        return 1

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Download file from dap.ema.europa.eu
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

async def sub_download_excel_file(drug, url):
    async with async_playwright() as p:
        try :
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(accept_downloads=True)
            page = await context.new_page()

            await page.goto(url)  # Replace with your actual URL
            await page.click('img#uberBar_dashboardpageoptions_image')

            # Listen for the download event
            download = page.wait_for_event('download')

            # Click on the 'Export to Excel' button
            await page.click('text="Export to Excel"')

            # Click on the 'Export Current Page' button
            await page.click('text="Export Current Page"')

            # Wait for the download event to fire and save the file
            download = await download
            path = await download.path()
            print(f'Download started: {download.url}')
            print(f'Suggested filename: {download.suggested_filename}')
            print(f'Download path: {path}')


            destination = Path.cwd() / drug
            shutil.copy(path, destination)
            print(f'File copied to: {destination}')
            # Additional code may be needed here to wait for the download to finish if necessary

            # When finished, close the browser
            await browser.close()
            return 0

        except Exception as e:
            return 1

def download_excel_file(drug, url):
    return asyncio.run(sub_download_excel_file(drug, url))

def get_random_cat_url():
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    if response.status_code == 200:
        data = response.json()
        return data[0]['url']
    else:
        return "Failed to get a cat picture."

# ==============================================================================
# ------------------------------------ MAIN ------------------------------------
# ==============================================================================

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Variables
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::
    drug      = message.text.upper().lstrip('/')
    chat_id   = message.chat.id
    url       = ''


    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Searching for file in local database
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::
    bot.send_message(chat_id, "🔎 Searching for " + drug.upper() + "\nType /update to refresh the local database from \nhttps://www.adrreports.eu/tables/substance/a.html")

    matched_drug_lines = find_lines_with_substring(drug)
    if (len(matched_drug_lines) == 0):
        bot.send_message(chat_id, "❌ Error - No match found for " + drug.upper())
        bot.send_message(chat_id, "🐱 Here's a cat picture instead - bisou")
        bot.send_message(chat_id, get_random_cat_url())
        return

    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # If multiple matches, send them all to the user and stop
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::
    if (len(matched_drug_lines) != 1):
        if len(matched_drug_lines) > 50:
            bot.send_message(chat_id, "⚠️  Only the first 50 matches are shown below")
            matched_drug_lines = matched_drug_lines[:50]
        message_string = '\n'.join(matched_drug_lines)
        bot.send_message(chat_id, message_string)
        bot.send_message(chat_id, "⚠️  Multiple matches for " + drug.upper() + "\nPlease be more specific")
        return

    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # If only one match found, continue
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::
    bot.send_message(chat_id, "✅ URL found in local database")

    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Scraping xlsx file from dap.ema.europa.eu
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::
    bot.send_message(chat_id, "⏬ Downloading Excel file from " + url)
    if (download_excel_file(drug, url)):
        bot.send_message(chat_id, "❌ Error downloading file from dap.ema.europa.eu")
        return
    bot.send_message(chat_id, "✅ Excel file downloaded")

    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Sending the file back to the user
    # ::::::::::::::::::::::::::::::::::::::::::::::::::::::
    if (send_xslx(chat_id, drug)):
        bot.send_message(chat_id, "❌ Error sending file to user")
        return

    bot.send_message(chat_id, "✅ Done for " + drug.upper())


# ==============================================================================
# ------------------------------------ CORE ------------------------------------
# ==============================================================================
bot.infinity_polling()

