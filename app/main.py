from app.crawler import importer
from playwright.sync_api import sync_playwright


def main():
    global playwright
    with sync_playwright() as playwright:
        page = importer.initialize_playwright(playwright)
        page.goto("https://eticket.railway.uz/en/home", timeout=90000)
        stations = importer.extract_stations_info(importer.main_page_content)
        importer.save_to_redis(stations)


if __name__ == "__main__":
    main()
