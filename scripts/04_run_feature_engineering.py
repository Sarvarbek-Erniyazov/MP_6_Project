import os
import sys

# Add project root to Python path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from src.feature_engineering_04 import run_feature_engineering

# Define paths
input_path = os.path.join(base_dir, 'data', 'multi-class_JUP_data', 'multi_class_JUP_features.csv')
output_dir = os.path.join(base_dir, 'data', 'multi_class_JUP_engineered_features')
log_path = os.path.join(base_dir, 'logs', '4.FE.log')

if __name__ == "__main__":
    print("Running Feature Engineering Module...\n")
    output = run_feature_engineering(input_path, output_dir, log_path)
    print(f"✅ Feature Engineering Completed!\nOutput file saved to:\n{output}")
