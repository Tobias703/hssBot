from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from config import *
import random
import time
from datetime import datetime
from zoneinfo import ZoneInfo

def enroll(course_id: int, headless=True):
    url = ENROLLMENT_URL.format(course_id=course_id)

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

def now():
    return datetime.now(ZoneInfo("Europe/Berlin"))

def sleep_with_jitter(base):
    jitter = random.uniform(-0.15, 0.15) * base
    time.sleep(max(0.01, base + jitter))
    
def compute_interval(seconds_to_open):
    """
    Smooth ramp:
    - >30 min: very slow
    - 30-1 min: medium
    - <1 min: aggressive
    """
    if seconds_to_open > 1800:
        return MIN_RATE
    if seconds_to_open > 60:
        return MED_RATE
    return MAX_RATE