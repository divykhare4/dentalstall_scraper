# Dental Stall Scraper

The Dentalstall Scraper Tool is a web scraping project to scrapte data from dentalstall.com. It collects details such as id, title, price and product image and stores this data in a json file. It also caches the product details in redis and sends relevant notifications via logging, email, and SMS.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Logging](#logging)
- [Improvements](#improvements)

## Features

- **Data Extraction**: Collect product information such as product ID, title, price, and images from the source.
- **Alerting System**: Provide a flexible notification system that supports logging, email, and SMS to report on the scraping process and outcomes.
- **Retry Mechanism**: The scraper will attempt to re-fetch a failed page a configurable number of times.
- **Event Logging**: Record key activities like scraping operations and notification events both in a log file and the console for monitoring purposes.
- **Data Caching**: Utilize Redis to store product data with an adjustable expiration time to avoid redundant scraping of the same content.
- **Data Storage**: Store the collected product information in a local JSON file, with an option to extend the implementation to integrate with different databases.

## Installation

1. **Clone the repository**:

   ```bash
   git clone git@github.com:Divy123/dental-stall-scraper.git
   cd dental-stall-scraper
   ```

2. **Install dependencies using Pipenv**:

   ```bash
   pipenv install
   ```

3. **Activate the virtual environment**:

   ```bash
   pipenv shell
   ```

## Usage

1. **Set up environment variables**:

   Update `.env.dev` file in the root directory:
   
   ```bash
   APP_NAME="dentalstall.com scraper"
   ENVIRONMENT="dev"
   PROXY="" # Optional
   AUTH_TOKEN="your_auth_token"
   MAX_PAGE_LIMIT=10
   REDIS_HOST="localhost"
   REDIS_PORT=6379
   REDIS_DB=0
   ```

2. **Run the application**:

    Make sure that the redis is up and running. To check if redis is running, run the following in a different terminal:
    ```bash
    ❯ redis-cli ping
    ```
    Start the server

   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access the API**:

   Start scraping by sending below curl request. The request accepts `total_pages` in the POST body but the number of pages to be scraped is limited by the config provided at the startup in `.env.dev` file.

   Example using `curl`:

   ```bash
   curl --location --request POST 'http://127.0.0.1:8000/scrape' --header 'Authorization: Bearer !mN8b663>H>y' --header 'Content-Type: application/json' --data-raw '{"total_pages": 2}'
   ```

4. **Output**:
   Images are stored in `assets` folder and output json is stored in `output/outputs.json`.

## Configuration


Configuration is stored in `.env.dev` file and `settings/settings.py` file. Edit them as per the requirement.

## Logging

The project use the python `logging` module for the logging purposes. The logs are printed on the console and are stored in the `logs` folder.

## Improvements

While the current implementation of the dentalstall.com scraper serves its purpose, there are various opportunities to enhance its performance, scalability, and overall usability:

### Asynchronous Scraping:

The current implementation of the scraper operates synchronously, which may hinder performance, especially when scraping large volumes of data across multiple pages. Transitioning to an asynchronous model with frameworks like `aiohttp` and `asyncio` can significantly boost speed and efficiency.

### Distributed Scraping:

For handling more extensive scraping operations, distributing the scraping workload across multiple servers or containers using tools like `Celery` or `Redis Queue` would enhance the system's scalability and ability to handle large-scale data extraction tasks.

### Enhanced Monitoring and Error Reporting:

To improve production reliability, integrating error reporting tools such as prometheus, alert manager and grafana would provide insight into issues as they arise. Coupled with system performance tracking and health monitoring, it would be easier to diagnose problems and optimize performance.

### Comprehensive Testing Strategy:

Introducing a thorough suite of unit and integration tests would provide assurance that each component of the system—whether the scraper, cache, or notification service—functions correctly. This would also facilitate quicker identification of regressions or bugs when new features are introduced.
