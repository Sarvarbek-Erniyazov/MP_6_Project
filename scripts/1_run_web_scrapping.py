# File: scripts/1_run_web_scrapping.py

import os
import sys
import logging
import time
import importlib.util

# --- Paths ---
SRC_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', '1_web_scrapping.py'))

# --- Import scraper dynamically because filename starts with a number ---
spec = importlib.util.spec_from_file_location("scraper", SRC_FILE)
scraper = importlib.util.module_from_spec(spec)
sys.modules["scraper"] = scraper
spec.loader.exec_module(scraper)

# --- Setup logging ---
logging.basicConfig(
    filename=os.path.join(scraper.LOG_DIR, "1.web_scrapping.log"),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    logging.info("--- Starting Data Fetch ---")

    for symbol, binance_symbol in scraper.COIN_MAPPING.items():
        logging.info(f"Fetching data for {symbol} ({binance_symbol})...")
        print(f"[INFO] Fetching data for {symbol} ({binance_symbol})...")
        max_retries = 3
        delay = 1

        for attempt in range(max_retries):
            df_data = scraper.fetch_historical_data(binance_symbol, scraper.DAYS_OF_DATA)
            if df_data is not None and not df_data.empty:
                output_file = os.path.join(scraper.DATA_DIR, f"{symbol}_historical_data_hourly.csv")
                df_data.to_csv(output_file)
                logging.info(f"Saved {len(df_data)} rows to {output_file}")
                print(f"[INFO] Saved {symbol} data ({len(df_data)} rows).")
                break

            logging.warning(f"Attempt {attempt+1} failed or returned empty. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2
        else:
            logging.error(f"Failed to fetch data for {symbol} after {max_retries} attempts.")
            print(f"[ERROR] Failed to fetch {symbol} data.")

    logging.info("--- Data Acquisition Complete ---")
    print("[INFO] Data Acquisition Complete.")
