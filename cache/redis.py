import json
import redis

from settings import fetch_settings
from app.models import Product

CACHE_EXPIRATION_SECONDS = 3600  # Cache expiration time in seconds


class RedisCache:
    """Manages caching of products in Redis."""

    def __init__(self):
        settings = fetch_settings()
        self.redis_client = redis.StrictRedis(
            host=settings.redis_host, port=settings.redis_port, db=settings.redis_db
        )

    def store_product(self, product: Product):
        """
        Caches a product in Redis with an expiration time.

        Args:
            product (Product): The product object to cache.
        """
        cache_key = self._generate_cache_key(product)
        product_data = json.dumps(product.model_dump())
        self.redis_client.setex(cache_key, CACHE_EXPIRATION_SECONDS, product_data)

    def is_product_cached(self, product: Product) -> bool:
        """
        Checks if a product is already cached and if the cached price matches the current price.

        Args:
            product (Product): The product object to check.

        Returns:
            bool: True if the product is cached and its price matches, otherwise False.
        """
        cache_key = self._generate_cache_key(product)
        cached_data = self.redis_client.get(cache_key)

        if cached_data:
            cached_product = json.loads(cached_data)
            return cached_product.get("product_price") == product.product_price

        return False

    def _generate_cache_key(self, product: Product) -> str:
        """
        Creates a unique cache key for the given product.

        Args:
            product (Product): The product object for which the cache key is generated.

        Returns:
            str: The cache key for the product.
        """
        return f"product_cache::{product.product_id}"
