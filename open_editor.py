"""Launch a persistent local Chromium browser for manual Naver login.

This does NOT save drafts. Requires `playwright install chromium`.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright


def main() -> None:
    profile = Path.home() / ".naver_blog_automation_profile"
    print("Naver login must be performed manually in the opened browser.")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            str(profile), headless=False, locale="ko-KR"
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://blog.naver.com/lstldh", wait_until="domcontentloaded")
        input("After checking the browser, press Enter to close it...")
        browser.close()


if __name__ == "__main__":
    main()
