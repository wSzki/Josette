import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
import shutil



async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()

        await page.goto('https://dap.ema.europa.eu/analytics/saw.dll?PortalPages&PortalPath=%2Fshared%2FPHV%20DAP%2F_portal%2FDAP&Action=Navigate&P0=1&P1=eq&P2=%22Line%20Listing%20Objects%22.%22Substance%20High%20Level%20Code%22&P3=1+18853')  # Replace with your actual URL
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

asyncio.run(main())
