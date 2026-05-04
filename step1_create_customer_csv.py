# =============================================================================
# TASK 2 – Step 1: Create customer_data.csv (Source 1)
# =============================================================================
# This script extracts the customer dimension columns from the original
# dataset and saves them as a separate CSV file.
#
# Output : customer_data.csv
# Columns: Rental_ID, Customer_Type, Customer_Gender,
#           Customer_Age, License_Type
# =============================================================================

import pandas as pd
import os

# ── Paths ─────────────────────────────────────────────────────────────────────
INPUT_FILE  = "Car_Rental_SLStyle_18Months.csv"   # original dataset
OUTPUT_FILE = "customer_data.csv"                  # Source 1 output

# ── Step 1: Load the original dataset ─────────────────────────────────────────
print("Loading original dataset...")
df = pd.read_csv(INPUT_FILE)
print(f"  Loaded {len(df):,} rows and {len(df.columns)} columns.")

# ── Step 2: Select only the customer-related columns ──────────────────────────
# Rental_ID is kept as the foreign key to link back to the fact table
customer_columns = [
    "Rental_ID",
    "Customer_Type",
    "Customer_Gender",
    "Customer_Age",
    "License_Type"
]

customer_df = df[customer_columns].copy()

# ── Step 3: Basic data quality checks ─────────────────────────────────────────
print("\nData quality checks:")
print(f"  Rows          : {len(customer_df):,}")
print(f"  Null values   :\n{customer_df.isnull().sum()}")
print(f"\n  Customer_Type values  : {sorted(customer_df['Customer_Type'].unique())}")
print(f"  Customer_Gender values: {sorted(customer_df['Customer_Gender'].unique())}")
print(f"  License_Type values   : {sorted(customer_df['License_Type'].unique())}")
print(f"  Age range             : {customer_df['Customer_Age'].min()} – {customer_df['Customer_Age'].max()}")

# ── Step 4: Save to CSV ────────────────────────────────────────────────────────
customer_df.to_csv(OUTPUT_FILE, index=False)
size_kb = os.path.getsize(OUTPUT_FILE) / 1024
print(f"\n✅ Saved '{OUTPUT_FILE}'  ({size_kb:.1f} KB)")
print(f"   Columns: {list(customer_df.columns)}")
print(f"   First 3 rows:\n{customer_df.head(3).to_string(index=False)}")
