import os

from settings import fetch_settings
from app.scraper import DentalStallProductScraper
from db import JSONProductStorage
from cache import RedisCache
from app.notification import LogBasedNotification
from app.logger import logger
from app.models import ScrapeRequest
from middlewares.auth import authenticate

from fastapi import FastAPI, Depends, HTTPException, Header

app = FastAPI()


@app.post("/scrape")
def scrape(request: ScrapeRequest, token: str = Depends(authenticate)):
    logger.info("Scraping initiated via API")
    scraper = DentalStallProductScraper()
    cache = RedisCache()
    notifier = LogBasedNotification()

    db = JSONProductStorage(
        os.path.abspath(os.path.join("output", fetch_settings().output_json_filename))
    )

    scraped_products = scraper.scrape_all(request.total_pages)
    new_count = 0
    updated_count = 0

    for product in scraped_products:
        if not cache.is_product_cached(product):
            new, updated = db.store_products([product])
            cache.store_product(product)

            new_count += new
            updated_count += updated

    notifier.notify(new_count, updated_count)
    logger.info(
        f"""Scraping session completed. {
                new_count} new products saved and {updated_count} products updated."""
    )

    return {"new": new_count, "updated": updated_count}
