from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    print("Starting browser...")

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    print("Opening website...")
    page.goto("https://example.com")

    print("Page title:", page.title())
    print("Page URL:", page.url)

    browser.close()

    print("Browser test completed successfully.")