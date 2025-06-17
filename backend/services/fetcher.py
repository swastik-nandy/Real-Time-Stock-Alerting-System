import time
import requests
import logging
import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
from datetime import time as dtime
from django.utils.timezone import now
from datetime import datetime


# Initialize logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# Load .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env')

import sys
sys.path.append(str(BASE_DIR))

# ----------------- Django Setup -----------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
import django
django.setup()

from stocks.models import Stock, StockPriceHistory

# ----------------- API Keys and DB -----------------

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# ----------------- History Writer -----------------

def store_price_history_if_market_open(symbol, price):
    current_time = datetime.now().time()
    if dtime(9, 32, 0) <= current_time <= dtime(9, 32, 40):  # TESTING window
        try:
            stock = Stock.objects.get(symbol=symbol)
            StockPriceHistory.objects.create(stock=stock, price=price)
            logging.info(f"✔️ Stored price history for {symbol} at {price}")
            return 1
        except Exception as e:
            logging.error(f"❌ Failed to store price history for {symbol}: {e}")
    return 0

# ----------------- Database Functions -----------------

def get_all_stocks():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()
        cursor.execute("SELECT symbol FROM stocks_stock")
        stocks = cursor.fetchall()
        cursor.close()
        conn.close()
        return [stock[0] for stock in stocks]
    except Exception as e:
        logging.error(f"❌ Database error while fetching stocks: {e}")
        return []

def update_latest_price(stock_symbol, new_price):
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE stocks_stock
            SET latest_price = %s
            WHERE symbol = %s
        """, (new_price, stock_symbol))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error(f"❌ Database error while updating price: {e}")

# ----------------- API Fetching -----------------

def fetch_stock_price(symbol, max_retries=3, wait_seconds=2):
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}'

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get('c')
        except Exception as e:
            logging.error(f"Attempt {attempt} failed fetching {symbol}: {e}")
            if attempt < max_retries:
                time.sleep(wait_seconds)
            else:
                logging.error(f"Failed to fetch {symbol} after {max_retries} attempts.")
                return None

# ----------------- Main Loop -----------------

def start_stock_price_fetcher():
    while True:
        logging.info("📡 Fetching latest stock prices...")

        stock_symbols = get_all_stocks()
        rows_added = 0

        if not stock_symbols:
            logging.warning("⚠️ No stocks found in database.")
        else:
            for symbol in stock_symbols:
                price = fetch_stock_price(symbol)
                if price is not None:
                    update_latest_price(symbol, price)
                    rows_added += store_price_history_if_market_open(symbol, price)
                    logging.info(f"💾 {symbol} updated to {price}")

        if rows_added > 0:
            logging.info(f"✅ Total rows added to StockPriceHistory this cycle: {rows_added}")
        else:
            logging.info("ℹ️ No rows added to StockPriceHistory this cycle.")

        time.sleep(10)

# ----------------- Entrypoint -----------------

if __name__ == "__main__":
    start_stock_price_fetcher()
