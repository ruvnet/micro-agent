import asyncio
from pyppeteer import launch
from pathlib import Path
import aiofiles
from .find_visual_file import find_visual_file

async def get_screenshot(options):
    current_code_path = Path(options['outputFile'])
    async with aiofiles.open(current_code_path, mode='r') as file:
        current_code = await file.read()
    
    cached = cache_by_code.get(current_code)
    if cached:
        return cached

    url = options['visual']
    image_file = await find_visual_file(options)
    if image_file is None:
        raise Exception("No image file found.")

    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)

    # Assuming the screenshot size is determined by the viewport of the page
    screenshot = await page.screenshot({'path': f'{current_code_path.stem}_screenshot.png', 'type': 'png'})
    await browser.close()

    cache_by_code[current_code] = screenshot
    return screenshot

cache_by_code = {}
