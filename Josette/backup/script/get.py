import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
import shutil
import sys

async def main(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        await page.goto(url)  # Use the URL provided as a command-line argument

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

        destination = Path.cwd() / download.suggested_filename
        shutil.copy(path, destination)
        print(f'File copied to: {destination}')
        # Additional code may be needed here to wait for the download to finish if necessary

        # When finished, close the browser
        await browser.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ./download_excel_file.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    asyncio.run(main(url))

