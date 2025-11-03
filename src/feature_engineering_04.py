import pandas as pd
import numpy as np
import os
import logging

# ----------------- Logging Setup -----------------
def setup_logger(log_path):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

# ----------------- RSI Calculation -----------------
def calculate_rsi(series, window=14):
    """Calculates the Relative Strength Index (RSI)."""
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.ewm(com=window - 1, adjust=False).mean()
    avg_loss = loss.ewm(com=window - 1, adjust=False).mean()

    with np.errstate(divide='ignore', invalid='ignore'):
        rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))
    return rsi

# ----------------- Main Feature Engineering -----------------
def run_feature_engineering(input_path, output_dir, log_path):
    setup_logger(log_path)
    logging.info("Starting Feature Engineering...")

    # 1. Load Data
    if not os.path.exists(input_path):
        logging.error(f"Input CSV not found: {input_path}")
        raise FileNotFoundError(f"Input CSV not found: {input_path}")

    df = pd.read_csv(input_path)
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df.set_index('Datetime', inplace=True)

    # 2. Feature Engineering
    logging.info("Generating FE_Return and FE_Volatility features...")
    df['FE_JUP_Return_Log'] = np.log(df['JUP_Close'] / df['JUP_Close'].shift(1))
    df['FE_JUP_Volatility_5'] = df['FE_JUP_Return_Log'].rolling(window=5).std()
    df['FE_JUP_Volatility_20'] = df['FE_JUP_Return_Log'].rolling(window=20).std()

    logging.info("Generating FE_Trend and FE_Momentum features...")
    df['FE_JUP_SMA_10'] = df['JUP_Close'].rolling(window=10).mean()
    df['FE_JUP_SMA_50'] = df['JUP_Close'].rolling(window=50).mean()
    df['FE_JUP_Close_vs_SMA10'] = df['JUP_Close'] / df['FE_JUP_SMA_10'] - 1
    df['FE_JUP_RSI_14'] = calculate_rsi(df['JUP_Close'], window=14)

    logging.info("Generating FE_Lag features...")
    df['FE_JUP_Close_Lag1'] = df['JUP_Close'].shift(1)
    df['FE_JUP_Volume_Lag1'] = df['JUP_Volume'].shift(1)
    df['FE_JUP_Hourly_Range'] = df['JUP_High'] - df['JUP_Low']
    df['FE_JUP_OC_Delta'] = df['JUP_Close'] - df['JUP_Open']

    logging.info("Generating FE_Time-Based features...")
    df['FE_Hour'] = df.index.hour
    df['FE_DayOfWeek'] = df.index.dayofweek
    df['FE_DayOfMonth'] = df.index.day

    # 3. Cleanup
    df.drop(columns=['JUP_Future_Return'], inplace=True, errors='ignore')
    df_engineered = df.dropna()

    # 4. Save
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'multi_class_JUP_engineered_features.csv')
    df_engineered.to_csv(output_path)

    logging.info(f"Feature Engineering completed successfully.")
    logging.info(f"Saved to: {output_path}")
    logging.info(f"Final shape: {df_engineered.shape}")

    return output_path
