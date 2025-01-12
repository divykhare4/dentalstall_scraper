import os
import requests
import time
from typing import List
from bs4 import BeautifulSoup

from cache import RedisCache
from app.models import Product
from settings import fetch_settings
from app.logger import logger
from app.utils import generate_random_alphanumeric


class ScraperBase:
    """Base class for implementing web scrapers."""

    def __init__(self, base_url: str, headers: dict = None, proxy: dict = None):
        self.base_url = base_url
        self.headers = headers or {}
        self.proxy = proxy

    def save_image(self, image_url: str, title: str) -> str:
        """Fetches and saves an image locally."""
        logger.info(f"Downloading image for: {title}")
        filename = self._create_filename(title)

        image_dir = fetch_settings().images_folder
        os.makedirs(image_dir, exist_ok=True)

        response = requests.get(image_url)
        filepath = os.path.join(image_dir, f"{filename}.jpg")

        with open(filepath, "wb") as file:
            file.write(response.content)

        return filepath

    def _create_filename(self, title: str) -> str:
        """Generates a safe and unique filename."""
        sanitized_title = "".join(
            char for char in title if char.isalnum()
        ).rstrip()
        unique_suffix = generate_random_alphanumeric(6)
        return f"{sanitized_title}_{unique_suffix}"

    def scrape_page(self, page_number: int) -> List[Product]:
        """Stub for scraping a single page. Must be implemented in subclasses."""
        raise NotImplementedError(
            "Method 'scrape_page' must be overridden in subclasses."
        )

    def scrape_all(self) -> List[Product]:
        """Stub for scraping across multiple pages. Must be implemented in subclasses."""
        raise NotImplementedError(
            "Method 'scrape_all' must be overridden in subclasses."
        )


class DentalStallProductScraper(ScraperBase):
    """Scraper implementation for DentalStall product catalog."""

    def __init__(self):
        settings = fetch_settings()
        base_url = settings.dentalstall_base_url
        proxy = {"http": settings.proxy} if settings.proxy else None

        super().__init__(base_url=base_url, proxy=proxy)

        self.max_pages = settings.max_page_limit
        self.cache = RedisCache()
        self.retry_limit = settings.dentalstall_max_retries

    def _scrape_single_page(self, page_number: int) -> List[Product]:
        """Handles scraping logic for one page."""
        logger.info(f"Scraping page {page_number}...")
        retries = 0
        while retries < self.retry_limit:
            try:
                page_url = (
                    f"{self.base_url}/page/{page_number}"
                    if page_number > 1
                    else self.base_url
                )
                response = requests.get(
                    page_url, headers=self.headers, proxies=self.proxy
                )
                response.raise_for_status()
                break
            except requests.RequestException as error:
                retries += 1
                delay = retries * 2
                logger.error(
                    f"Error on page {page_number}: {error}. Retrying in {delay} seconds."
                )
                time.sleep(delay)

                if retries == self.retry_limit:
                    logger.warning(
                        f"Page {page_number} skipped after {self.retry_limit} attempts."
                    )
                    return []

        soup = BeautifulSoup(response.text, "html.parser")
        product_data = []

        for product_card in soup.find_all("div", class_="product-inner"):
            title = product_card.find(
                "h2", class_="woo-loop-product__title"
            ).text.strip()
            product_id = product_card.find("div", class_="addtocart-buynow-btn").find(
                "a"
            )["data-product_id"]

            price_tag = product_card.find("span", class_="price")
            if not price_tag:
                logger.warning(f"Price missing for product: {title}")
                continue

            discounted_price = price_tag.find("ins")
            price = (
                float(discounted_price.text.replace("₹", "").strip())
                if discounted_price
                else float(
                    price_tag.find("span", class_="amount")
                    .text.replace("₹", "")
                    .strip()
                )
            )

            if self.cache.is_product_cached(
                Product(product_id=product_id, product_title=title, product_price=price, path_to_image="")
            ):
                continue

            image_url = product_card.find("img").get("data-lazy-src", "")
            if not image_url:
                logger.info(f"Image missing for product: {title}")
                continue

            image_path = self.save_image(image_url, title)
            product = Product(
                product_id=product_id,
                product_title=title,
                product_price=price,
                path_to_image=image_path,
            )
            product_data.append(product)
            logger.info(f"Scraped product: {title} at ₹{price}")

        return product_data

    def scrape_all(self, total_pages: int) -> List[Product]:
        """Handles scraping for multiple pages."""
        logger.info(
            f"Starting scraping up to {min(self.max_pages, total_pages)} pages..."
        )
        all_products = []

        for page in range(1, min(self.max_pages, total_pages) + 1):
            products = self._scrape_single_page(page)
            all_products.extend(products)

        logger.info(f"Scraping complete. Total products scraped: {len(all_products)}")
        return all_products
