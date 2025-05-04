import time
import requests
import logging
import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

# Initialize logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# Load .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env')

# Load Finnhub API Key
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

# PostgreSQL connection details
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# ----------------- Database Functions -----------------

def get_all_stocks():
    """Fetch all stocks from stocks_stock table."""
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
        logging.error(f"Database error while fetching stocks: {e}")
        return []

def update_latest_price(stock_symbol, new_price):
    """Update the latest price for a stock."""
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
        logging.error(f"Database error while updating price: {e}")

# ----------------- API Fetching Functions -----------------

def fetch_stock_price(symbol, max_retries=3, wait_seconds=2):
    """Fetch live stock price from Finnhub."""
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}'
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get('c')  # 'c' stands for current price
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
        logging.info("Fetching latest stock prices...")

        stock_symbols = get_all_stocks()

        if not stock_symbols:
            logging.warning("No stocks found in database.")
        else:
            for symbol in stock_symbols:
                price = fetch_stock_price(symbol)
                if price is not None:
                    update_latest_price(symbol, price)
                    logging.info(f"{symbol} updated to {price}")
        
        time.sleep(10)  # Fetch every 10 seconds

# ----------------- Entrypoint -----------------

if __name__ == "__main__":
    start_stock_price_fetcher()