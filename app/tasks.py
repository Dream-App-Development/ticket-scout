from app.celery import app
from playwright.sync_api import sync_playwright
from app.crawler.importer import initialize_playwright


@app.task
def run_playwright_task():
    print("Starting playwright task")
    with sync_playwright() as playwright:
        page = initialize_playwright(playwright)
        page.close()
