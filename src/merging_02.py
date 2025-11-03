# File: src/merging_02.py

import pandas as pd
import os
import logging

# --- Configurations ---
RAW_DATA_DIR = r"C:\Users\sharg\Desktop\uyga vazifa\unsupervised learning\4-oy\6-project\binance.com\data\raw"
MERGED_DATA_DIR = r"C:\Users\sharg\Desktop\uyga vazifa\unsupervised learning\4-oy\6-project\binance.com\data\merged"
LOG_FILE = r"C:\Users\sharg\Desktop\uyga vazifa\unsupervised learning\4-oy\6-project\binance.com\logs\2.merging.log"
COINS = ['APE', 'ARB', 'FIL', 'GALA', 'JUP', 'OP', 'SEI', 'TIA']

# --- Setup directories ---
os.makedirs(MERGED_DATA_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# --- Setup logging ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Load single coin data ---
def load_coin_data(coin):
    file_path = os.path.join(RAW_DATA_DIR, f"{coin}_historical_data_hourly.csv")
    df = pd.read_csv(file_path, parse_dates=['Datetime'], index_col='Datetime')
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    df = df.rename(columns={
        'Open': f'{coin}_Open',
        'High': f'{coin}_High',
        'Low': f'{coin}_Low',
        'Close': f'{coin}_Close',
        'Volume': f'{coin}_Volume'
    })
    logging.info(f"{coin} data loaded: {df.shape[0]} rows")
    return df

# --- Merge all coins ---
def merge_all_coins():
    merged_df = None
    for coin in COINS:
        df = load_coin_data(coin)
        if merged_df is None:
            merged_df = df
        else:
            merged_df = merged_df.join(df, how='outer')
    merged_df = merged_df.dropna()
    logging.info(f"Merged all coins: {merged_df.shape[0]} rows, {merged_df.shape[1]} columns")
    return merged_df

# --- Save merged features ---
def save_merged_features(df):
    merged_file = os.path.join(MERGED_DATA_DIR, 'merged_features.csv')
    df.to_csv(merged_file)
    logging.info(f"Merged features saved to: {merged_file}")
    return merged_file

# --- Run merge ---
if __name__ == "__main__":
    merged_df = merge_all_coins()
    merged_file = save_merged_features(merged_df)
    print("Merged features saved to:", merged_file)
    print("Log written to:", LOG_FILE)
