# login_and_save_state.py
from playwright.sync_api import sync_playwright
from config import *
import json
import sys

def login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(LOGIN_URL)

        print("Log in manually via Uni Ulm SSO.")
        input("Press ENTER after you see the KursListe page...")

        context.storage_state(path=AUTH_STATE)
        print("Saved auth state to ", AUTH_STATE)

        browser.close()

def check_logged_in():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=AUTH_STATE)
        response = context.request.get(IS_LOGGED_IN_URL)

        try:
            print(response.text())
        except Exception as e:
            print("Failed to read response body:", e)
            
        response_data = json.loads(response.text())
        if response_data["isLoggedIn"] == False:
            return 0
            
        browser.close()
        return 1