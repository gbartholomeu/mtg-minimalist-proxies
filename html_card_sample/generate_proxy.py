#!/usr/bin/python3
import asyncio
from pyppeteer import launch
import os

async def main():
    browser = await launch()
    page = await browser.newPage()
    # await page.goto(f'file://{os.getcwd()}/planeswalker.html')
    await page.goto(f'file:///tmp/scryfall_cache/html_temp_Tezzeret,_Master_of_the_Bridge-war/html_template.html')
    await page.screenshot({'path': '/tmp/scryfall_cache/minimalist_Tezzeret,_Master_of_the_Bridge-war.png', 'clip':{'x':0,'y':0, 'width': 1540, 'height': 2140} })
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
