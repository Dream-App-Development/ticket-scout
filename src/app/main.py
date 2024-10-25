from uuid import uuid4

import requests
import re
from requests import session
from urllib3 import request

from crawler import importer

XSRF_TOKEN = str(uuid4())
# values of the cookie 'XSRF-TOKEN' and header 'X-XSRF-TOKEN' must be the same
headers = {
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en",  # essential header
    "Cache-Control": "no-cache",
    "Cookie": f"XSRF-TOKEN={XSRF_TOKEN}",  # essential header
    "Device-Type": "BROWSER",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "X-XSRF-TOKEN": XSRF_TOKEN  # essential header
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


def get_js_file_title(html_content: str):
    match = re.search(r'main\.[a-zA-Z0-9]+\.js', html_content)

    if match:
        return match.group(0)
    else:
        print("No matching JS file found.")


def main():
    requests_session = requests.Session()
    response = requests.get("https://eticket.railway.uz/en/pages/trains-page")
    js_file_title = get_js_file_title(response.text)
    print(js_file_title)
    main_response = requests.get(f"https://eticket.railway.uz/en/{js_file_title}")
    stations = importer.extract_stations_info(main_response.text)
    # importer.save_to_redis(stations)
    tickets_response = get_ticket_info_test(requests_session)
    print(tickets_response.status_code)
    print(tickets_response.json())


if __name__ == "__main__":
    main()
