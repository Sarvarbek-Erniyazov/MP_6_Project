# File: src/1_web_scrapping.py

import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import os
import logging

# --- Setup directories ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --- Config ---
DAYS_OF_DATA = 365
INTERVAL = '1h'
LIMIT = 1000

COIN_MAPPING = {
    "JUP": "JUPUSDT",
    "SEI": "SEIUSDT",
    "ARB": "ARBUSDT",
    "TIA": "TIAUSDT",
    "APE": "APEUSDT",
    "GALA": "GALAUSDT",
    "FIL": "FILUSDT",
    "OP": "OPUSDT",
}

BASE_URL = "https://api.binance.com/api/v3/klines"

# --- Utility functions ---
def get_timestamp(days_ago: int = 0) -> int:
    target_date = datetime.utcnow() - timedelta(days=days_ago)
    return int(target_date.timestamp() * 1000)

def fetch_historical_data(symbol: str, days: int) -> pd.DataFrame | None:
    all_data = []
    start_time = get_timestamp(days)
    end_time = get_timestamp(0)
    current_end_time = end_time

    logging.info(f"Fetching {days} days of {INTERVAL} data for {symbol}")

    while current_end_time > start_time:
        params = {
            'symbol': symbol,
            'interval': INTERVAL,
            'limit': LIMIT,
            'endTime': current_end_time
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if not data:
                logging.info("No more data returned from API.")
                break

            all_data = data + all_data
            current_end_time = data[0][0] - 1
            time.sleep(0.1)

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed for {symbol}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error for {symbol}: {e}")
            return None

    df = pd.DataFrame(all_data, columns=[
        'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
        'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
        'Taker Buy Quote Asset Volume', 'Ignore'
    ])
    df['Datetime'] = pd.to_datetime(df['Open Time'], unit='ms')
    df = df.set_index('Datetime')
    df_final = df[['Open', 'High', 'Low', 'Close', 'Volume']].apply(pd.to_numeric, errors='coerce')
    return df_final.dropna()
