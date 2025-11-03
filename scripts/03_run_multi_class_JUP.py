import os
import pandas as pd
import subprocess

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "multi-class_JUP_data")
CSV_FILE = os.path.join(DATA_DIR, "multi_class_JUP_features.csv")
SCRIPT_03 = os.path.join(BASE_DIR, "src", "multi_class_JUP_03.py")

# --- Check if CSV exists, otherwise run 03 script ---
if not os.path.exists(CSV_FILE):
    print("CSV not found, running multi_class_JUP_03.py to generate it...")
    subprocess.run(["python", SCRIPT_03], check=True)

# --- Load CSV ---
df = pd.read_csv(CSV_FILE, index_col="Datetime", parse_dates=True)

# --- Show class distribution ---
print("\nCheck class distribution for JUP_Target_MultiClass:\n")
print(df['JUP_Target_MultiClass'].value_counts())
