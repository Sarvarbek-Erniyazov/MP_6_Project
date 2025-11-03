import pandas as pd
import numpy as np
import os
import logging

# --- Directories ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "merged")
SAVE_DIR = os.path.join(BASE_DIR, "data", "multi-class_JUP_data")
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --- Logging setup ---
log_file = os.path.join(LOG_DIR, "3.multi-class_JUP.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filemode="w"
)

logging.info("Started multi-class JUP target creation")

# --- Load merged data ---
merged_file = os.path.join(DATA_DIR, "merged_features.csv")
df = pd.read_csv(merged_file, index_col="Datetime", parse_dates=True)
logging.info(f"Loaded merged features: {df.shape}")

# --- Keep only JUP columns ---
jup_cols = [col for col in df.columns if col.startswith('JUP_')]
df = df[jup_cols]
logging.info(f"Filtered only JUP columns: {df.shape}")

# --- Create future 1-hour return ---
df['JUP_Future_Return'] = (df['JUP_Close'].shift(-1) - df['JUP_Close']) / df['JUP_Close']

# --- Multi-class target (0=Down, 1=Sideways, 2=Up) with threshold ±0.3% ---
threshold = 0.003
conditions = [
    df['JUP_Future_Return'] > threshold,   # Up
    df['JUP_Future_Return'] < -threshold   # Down
]
choices = [2, 0]
df['JUP_Target_MultiClass'] = np.select(conditions, choices, default=1)

# --- Log and drop missing ---
logging.info(f"Missing values per column:\n{df.isnull().sum()}")
df = df.dropna()

logging.info("Created JUP multi-class target with threshold ±0.3%")

# --- Save processed dataset ---
save_file = os.path.join(SAVE_DIR, "multi_class_JUP_features.csv")
df.to_csv(save_file)
logging.info(f"Saved multi-class JUP dataset: {save_file}")

print("Multi-class JUP target dataset is ready.")
