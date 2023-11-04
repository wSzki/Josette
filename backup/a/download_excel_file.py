import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
import shutil
import sys



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
