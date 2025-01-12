import json
import os
from typing import List
from abc import ABC, abstractmethod

from app.logger import logger
from app.models import Product


class AbstractProductStorage(ABC):
    """
    Abstract base class defining methods for product storage management.
    """

    @abstractmethod
    def load_products(self) -> List[Product]:
        """
        Loads the list of products from the storage.
        """
        pass

    @abstractmethod
    def store_products(self, products: List[Product]):
        """
        Saves a list of products to the storage.
        """
        pass


class JSONProductStorage(AbstractProductStorage):
    """
    Concrete implementation of AbstractProductStorage using JSON files.
    """

    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        # Ensure the directory exists
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)

    def load_products(self) -> List[Product]:
        """
        Load products from the JSON file if it exists. Returns an empty list otherwise.
        """
        if not os.path.exists(self.storage_path) or os.stat(self.storage_path).st_size == 0:
            logger.info("Storage file not found or empty. Returning an empty list.")
            return []

        with open(self.storage_path, "r") as file:
            try:
                products_data = json.load(file)
                return [Product(**product) for product in products_data]
            except json.JSONDecodeError:
                logger.warning("Invalid JSON format in storage file.")
                return []

    def store_products(self, products: List[Product]):
        """
        Save or update products in the JSON storage file.
        """
        current_products = self.load_products()
        product_map = {product.product_id: product for product in current_products}

        new_count = 0
        updated_count = 0

        for product in products:
            if product.product_id not in product_map:
                product_map[product.product_id] = product
                new_count += 1
            else:
                product_map[product.product_id] = product
                updated_count += 1

        # Save updated product list back to file
        with open(self.storage_path, "w") as file:
            json.dump([p.model_dump() for p in product_map.values()], file, indent=4)

        logger.info(f"Products saved: {new_count} new, {updated_count} updated.")
        return new_count, updated_count
