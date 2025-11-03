

import sys
import os


SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.append(SRC_DIR)


from merging_02 import merge_all_coins, save_merged_features

if __name__ == "__main__":
    merged_df = merge_all_coins()
    merged_file = save_merged_features(merged_df)
    print("Merged features saved to:", merged_file)
