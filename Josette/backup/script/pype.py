# import asyncio
# from pyppeteer import launch

# async def main():
    # browser = await launch(headless=True)
    # page = await browser.newPage()
    # await page.goto('https://dap.ema.europa.eu/analyticsSOAP/saw.dll?PortalPages&PortalPath=%2Fshared%2FPHV%20DAP%2F_portal%2FDAP&Action=Navigate&P0=1&P1=eq&P2=%22Line%20Listing%20Objects%22.%22Substance%20High%20Level%20Code%22&P3=1+17884')

    # # Wait for the selector to load
    # await page.waitForSelector('.MenuItemTextCell')

    # # Click on the element containing the text 'Export Current Page'
    # await page.evaluate('''() => {
        # Array.from(document.querySelectorAll('.MenuItemTextCell'))
            # .find(el => el.innerText.includes('Export Current Page'))
            # ?.click();
    # }''')

    # # Do something post click, like wait for a download to start
    # # ... Your code here ...

    # await browser.close()

# asyncio.get_event_loop().run_until_complete(main())

import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to your desired URL
        await page.goto('https://dap.ema.europa.eu/analyticsSOAP/saw.dll?PortalPages&PortalPath=%2Fshared%2FPHV%20DAP%2F_portal%2FDAP&Action=Navigate&P0=1&P1=eq&P2=%22Line%20Listing%20Objects%22.%22Substance%20High%20Level%20Code%22&P3=1+17884')

        # Wait for the '.MenuItemTextCell' elements to be loaded
        await page.wait_for_selector('.MenuItemTextCell')

        # Perform the click on the 'Export Current Page' button
        await page.evaluate('''() => {
            Array.from(document.querySelectorAll('.MenuItemTextCell'))
                .find(el => el.innerText.includes('Export Current Page'))
                ?.click();
        }''')

        # Wait for the file to be downloaded
        # You need to know the download path or some part of the filename to wait for it
        download = await page.wait_for_event('download')  # <-- waits for the download to start
        await download.save_as("./file.xlsx")

        # Close the browser
        await browser.close()

asyncio.run(main())

