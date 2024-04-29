import json
import re

from playwright.sync_api import sync_playwright

# Declare a global variable to hold the data
locale_stations_data = None


def fix_json(data):
    # Replace property names without double quotes
    data = data.replace('{ru:', '{"ru":')
    data = data.replace(',ru:', ',"ru":')
    data = data.replace('{uz:', '{"uz":')
    data = data.replace(',uz:', ',"uz":')
    data = data.replace('{en:', '{"en":')
    data = data.replace(',en:', ',"en":')
    data = data.replace('{code:', '{"code":')
    data = data.replace(',code:', ',"code":')

    return data


# data = '''
# [{ru:"\u0422\u0430\u0448\u043a\u0435\u043d\u0442",uz:"Toshkent",en:"Tashkent",code:"2900000"},{ru:"\u0421\u0430\u043c\u0430\u0440\u043a\u0430\u043d\u0434",uz:"Samarqand",en:"Samarkand",code:"2900700"},{ru:"\u0411\u0443\u0445\u0430\u0440\u0430",uz:"Buxoro",en:"Bukhara",code:"2900800"},{ru:"\u0425\u0438\u0432\u0430",uz:"Xiva",en:"Khiva",code:"2900172"},{ru:"\u0423\u0440\u0433\u0435\u043d\u0447",uz:"Urganch",en:"Urgench",code:"2900790"},{ru:"\u041d\u0443\u043a\u0443\u0441",uz:"Nukus",en:"Nukus",code:"2900970"},{ru:"\u041d\u0430\u0432\u043e\u0438",uz:"Navoiy",en:"Navoi",code:"2900930"},{ru:"\u0410\u043d\u0434\u0438\u0436\u0430\u043d",uz:"Andijon",en:"Andijan",code:"2900680"},{ru:"\u041a\u0430\u0440\u0448\u0438",uz:"Qarshi",en:"Karshi",code:"2900750"},{ru:"\u0414\u0436\u0438\u0437\u0430\u043a",uz:"Jizzax",en:"Jizzakh",code:"2900720"},{ru:"\u0422\u0435\u0440\u043c\u0435\u0437",uz:"Termiz",en:"Termez",code:"2900255"},{ru:"\u0413\u0443\u043b\u0438\u0441\u0442\u0430\u043d",uz:"Guliston",en:"Gulistan",code:"2900850"},{ru:"\u041a\u043e\u043a\u0430\u043d\u0434",en:"Qo'qon",uz:"Qo'qon",code:"2900880"},{ru:"\u041c\u0430\u0440\u0433\u0438\u043b\u0430\u043d",en:"Margilon",uz:"Margilon",code:"2900920"},{ru:"\u041f\u0430\u043f",en:"Pop",uz:"Pop",code:"2900693"},{ru:"\u041d\u0430\u043c\u0430\u043d\u0433\u0430\u043d",en:"Namangan",uz:"Namangan",code:"2900940"}]
# '''
# fixed = fix_json(data)
# decoded = json.loads(fixed)
# print(decoded)


def modify_requests(route, request):
    global locale_stations_data  # Reference the global variable
    # Check if the request URL includes the specific JavaScript file
    if 'main.259db808914687da4dfa.js' in request.url:
        print("FOUND")
        # First, you need to continue the route to get the response
        route.continue_()
        response = request.response()
        if response:
            print("Response OK")
            body = response.body()
            # Convert bytes to string
            js_content = body.decode('utf-8')
            # Find and extract the content of this.localeStations
            match = re.search(r'this\.localeStations\s*=\s*(.*?);', js_content)
            if match:
                locale_stations_data = match.group(1)
                cleaned_data = locale_stations_data.split(']')[0] + ']'
                fixed_data = fix_json(cleaned_data)
                decoded_data = json.loads(fixed_data)
                print(f"Locale stations data: {locale_stations_data}")
                print(f"Cleaned data{decoded_data}")
            else:
                print("this.localeStations not found in the JavaScript file.")
    else:
        # Continue the request for all other routes
        route.continue_()


def initialize_playwright(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    # Route needs to be established before navigating to the page
    context.route('**/*', modify_requests)
    return context.new_page()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        page = initialize_playwright(playwright)
        page.goto("https://eticket.railway.uz/en/home", timeout=90000)
        #
