import json
import re

from playwright.sync_api import sync_playwright

# Declare a global variable to hold the data
locale_stations_data = None

JAVASCRIPT_FILE_NAME = 'main.259db808914687da4dfa.js'


def fix_json(data):
    # Function to fix JSON data by adding double quotes to property names
    data = re.sub(r'({|,)(\w+):', r'\1"\2":', data)
    return data


def handle_js_route(route, request):
    global locale_stations_data

    if JAVASCRIPT_FILE_NAME in request.url:
        route.continue_()
        response = request.response()
        if response:
            body = response.body()
            js_content = body.decode('utf-8')
            match = re.search(r'this\.localeStations\s*=\s*(.*?);', js_content)
            if match:
                cleaned_data = match.group(1).split(']')[0] + ']'
                fixed_data = fix_json(cleaned_data)
                decoded_data = json.loads(fixed_data)
                print(f"Cleaned data: {decoded_data}")
            else:
                print("this.localeStations not found in the JavaScript file.")
    else:
        route.continue_()


def initialize_playwright(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    context.route('**/*', handle_js_route)
    return context.new_page()


def main():
    global playwright
    with sync_playwright() as playwright:
        page = initialize_playwright(playwright)
        page.goto("https://eticket.railway.uz/en/home", timeout=90000)
        #


if __name__ == "__main__":
    main()
