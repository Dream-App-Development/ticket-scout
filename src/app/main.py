import requests
from requests import session
from urllib3 import request

from crawler import importer
from playwright.sync_api import sync_playwright


headers = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "160",
    "Cookie": "__stripe_mid=48ec407d-cbfe-45ed-badb-a845484aea6ea99ba3; _ga=GA1.1.1990290039.1726498760; G_ENABLED_IDPS=google; XSRF-TOKEN=b4bd663b-9980-4544-9cb8-60dcd7502e56; _ga_K4H2SZ7MWK=GS1.1.1729408038.4.1.1729408762.0.0.0",
    "Device-Type": "BROWSER",
    "Host": "eticket.railway.uz",
    "Origin": "https://eticket.railway.uz",
    "Pragma": "no-cache",
    "Referer": "https://eticket.railway.uz/en/pages/trains-page",
    "Sec-CH-UA": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "X-XSRF-TOKEN": "b4bd663b-9980-4544-9cb8-60dcd7502e56"
}


def get_ticket_info_test(requests_session: requests.Session) -> requests.Response:
    return requests_session.post(
        url="https://eticket.railway.uz/api/v3/trains/availability/space/between/stations",
        json={
            "detailNumPlaces": 1,
            "direction": [
                {
                    "depDate": "25.10.2024",
                    "fullday": True,
                    "type": "Forward"
                }
            ],
            "showWithoutPlaces": 0,
            "stationFrom": "2900800",
            "stationTo": "2900000"
        },
        headers=headers,
        timeout=20
    )


def main():
    # global playwright
    # with sync_playwright() as playwright:
    #     page = importer.initialize_playwright(playwright)
    #     page.goto("https://eticket.railway.uz/en/home", timeout=90000)
    requests_session = requests.Session()
    response = requests.get("https://eticket.railway.uz/en/main.a6b751958f1637237fc1.js")
    print(response.status_code)
    print(response.text)
    stations = importer.extract_stations_info(response.text)
    importer.save_to_redis(stations)
    tickets_response = get_ticket_info_test(requests_session)
    print(tickets_response.status_code)
    print(tickets_response.json())


if __name__ == "__main__":
    main()
