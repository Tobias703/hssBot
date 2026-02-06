from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from config import *

def enroll(course_id: int, headless=True):
    url = ENROLlMENT_URL.format(course_id=course_id)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(storage_state=AUTH_STATE)
        page = context.new_page()

        # Go directly to booking page
        page.goto(url, wait_until="domcontentloaded")

        # Wait for the submit button to exist
        try:
            page.wait_for_selector("#subbtn1", timeout=5000)
        except PlaywrightTimeoutError:
            exists = page.evaluate("""
                () => !!document.querySelector("input[type=submit]")
                """)
            print("Submit button exists:", exists)
            page.screenshot(path="debug_no_button.png", full_page=True)
            raise RuntimeError("Booking button not found (not logged in or course not bookable)")

        with page.expect_navigation(wait_until="domcontentloaded"):
            page.click("#subbtn1")

        page.wait_for_timeout(2000)

        html = page.content()

        browser.close()
        
        print("Enrolled to course: ", course_id)

        return html
