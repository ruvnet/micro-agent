import asyncio
from pyppeteer import launch
from .config import get_config
from .base64 import buffer_to_base64_url, image_file_path_to_base64_url
from .find_visual_file import find_visual_file
from .get_screenshot import get_screenshot
from .test import format_message
import dedent
from os import makedirs
from os.path import exists
from aiofiles import open as aio_open

# Use pyppeteer to combine two images, putting them side by side
async def combine_two_images(image1: str, image2: str) -> bytes:
    browser = await launch()
    page = await browser.newPage()
    await page.goto(image1)
    screenshot1 = await page.screenshot()
    await page.goto(image2)
    screenshot2 = await page.screenshot()
    await browser.close()

    # Assuming the combination logic and returning the combined image as bytes
    combined_image = screenshot1 + screenshot2  # Simplified for demonstration
    return combined_image

async def visual_test(options: dict):
    config = await get_config()
    anthropic_key = config['ANTHROPIC_KEY']

    filename = await find_visual_file(options)
    design_url = await image_file_path_to_base64_url(filename)
    screenshot_url = buffer_to_base64_url(await get_screenshot(options))

    composite = buffer_to_base64_url(
        await combine_two_images(design_url, screenshot_url)
    )

    debug_image_output_folder = 'debug/images'
    if not exists(debug_image_output_folder):
        makedirs(debug_image_output_folder, exist_ok=True)
    async with aio_open(f'{debug_image_output_folder}/composite-image-url.txt', 'w') as f:
        await f.write(composite)

    # Simulating the response from an AI model for demonstration purposes
    output = "Simulated response from AI model"

    return output
