import asyncio
import json
import os
from playwright.async_api import async_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
COOKIES_FILE = "linkedin_cookies.json"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
        )

        context = await browser.new_context()
        page = await context.new_page()

        # 
        if os.path.exists(COOKIES_FILE):
            with open(COOKIES_FILE, "r", encoding="utf-8") as f:
                cookies = json.load(f)
            print(f"Loading {len(cookies)} cookies")
            await context.add_cookies(cookies)
            await page.goto("https://www.linkedin.com/feed/")
        else:
            await page.goto("https://www.linkedin.com/login")
            print(">>> Please log in manually within 60 seconds...")
            await asyncio.sleep(60)  # time to login

            cookies = await context.cookies()
            print(f"Saving {len(cookies)} cookies")
            with open(COOKIES_FILE, "w", encoding="utf-8") as f:
                json.dump(cookies, f)
            print(f"Cookies saved to {COOKIES_FILE}")

            await page.goto("https://www.linkedin.com/feed/")

        await asyncio.sleep(30)  # keep browser open to verify login
        await browser.close()

asyncio.run(main())
