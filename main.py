import json
import re
import time

import redis
from playwright.sync_api import sync_playwright

# Declare a global variable to hold the data
locale_stations_data = None
main_page_content = None

JAVASCRIPT_FILE_NAME = 'main.'
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


def fix_json(data):
    # Function to fix JSON data by adding double quotes to property names
    data = re.sub(r'({|,)(\w+):', r'\1"\2":', data)
    return data


def handle_js_route(route, request):
    if JAVASCRIPT_FILE_NAME in request.url:
        route.continue_()
        response = request.response()
        if response:
            global main_page_content
            main_page_content = response.body()
    else:
        route.continue_()


def extract_stations_info(body):
    js_content = body.decode('utf-8')
    match = re.search(r'this\.localeStations\s*=\s*(.*?);', js_content)
    if match:
        return clean_data(match)
    # print(f"Cleaned data: {user_data}")
    else:
        print("this.localeStations not found in the JavaScript file.")


def clean_data(match):
    cleaned_data = match.group(1).split(']')[0] + ']'
    fixed_data = fix_json(cleaned_data)
    decoded_data = json.loads(fixed_data)
    return decoded_data


def save_to_redis(decoded_data):
    for station in decoded_data:
        key = f"city:{station['code']}"
        r.set(key, json.dumps(station))

    keys = r.keys('city:*')
    cities = [json.loads(r.get(key)) for key in
              keys]  # Using r.get and json.loads to correctly retrieve and deserialize the data
    print(f"Data from redis:{cities}")


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
        stations = extract_stations_info(main_page_content)
        save_to_redis(stations)


if __name__ == "__main__":
    main()
