# =============================================================================
# TASK 2 – Step 2: Create rental_data.csv (Source 2 staging file)
#           and load it into SQL Server as CarRentalOLTP.dbo.RentalTransactions
# =============================================================================
# This script:
#   1. Strips customer columns and saves rental_data.csv
#   2. Connects to SQL Server and creates the CarRentalOLTP database
#   3. Creates the dbo.RentalTransactions table with proper data types
#   4. Bulk-inserts all 60 000 rows from rental_data.csv
#
# Requirements:
#   pip install pandas pyodbc sqlalchemy
#
# SQL Server connection:
#   Change SERVER_NAME below to match your machine name or use '.' / 'localhost'
#   If you use Windows Authentication leave UID/PWD as empty strings.
# =============================================================================

import pandas as pd
import os

# ── Paths ─────────────────────────────────────────────────────────────────────
INPUT_FILE        = "Car_Rental_SLStyle_18Months.csv"
RENTAL_OUTPUT_CSV = "rental_data.csv"

# ── SQL Server connection settings ────────────────────────────────────────────
# Change SERVER_NAME to your SQL Server instance name.
# Examples:  "."  /  "localhost"  /  "DESKTOP-ABC123\SQLEXPRESS"
SERVER_NAME = "."                  # <-- change if needed
DATABASE    = "CarRentalOLTP"
USE_WINDOWS_AUTH = True            # True  → Windows Authentication (recommended)
SQL_USER    = ""                   # only used when USE_WINDOWS_AUTH = False
SQL_PASSWORD = ""                  # only used when USE_WINDOWS_AUTH = False

# =============================================================================
# PART A – Build rental_data.csv
# =============================================================================

print("=" * 60)
print("PART A: Creating rental_data.csv")
print("=" * 60)

# Load original dataset
print("Loading original dataset...")
df = pd.read_csv(INPUT_FILE)
print(f"  Loaded {len(df):,} rows.")

# Columns that go to the CUSTOMER source (CSV) — remove these
customer_only_columns = [
    "Customer_Type",
    "Customer_Gender",
    "Customer_Age",
    "License_Type"
]

# Keep everything else (Rental_ID stays as the join key)
rental_df = df.drop(columns=customer_only_columns)

# Fix data types before saving
rental_df["Rental_Start_Date"] = pd.to_datetime(rental_df["Rental_Start_Date"]).dt.date
rental_df["Rental_End_Date"]   = pd.to_datetime(rental_df["Rental_End_Date"]).dt.date

print(f"\n  Columns in rental_data.csv ({len(rental_df.columns)}):")
for col in rental_df.columns:
    print(f"    {col}")

rental_df.to_csv(RENTAL_OUTPUT_CSV, index=False)
size_kb = os.path.getsize(RENTAL_OUTPUT_CSV) / 1024
print(f"\n✅ Saved '{RENTAL_OUTPUT_CSV}'  ({size_kb:.1f} KB, {len(rental_df):,} rows)")

# =============================================================================
# PART B – Load rental_data.csv into SQL Server
# =============================================================================

print("\n" + "=" * 60)
print("PART B: Loading into SQL Server")
print("=" * 60)

try:
    import pyodbc
    from sqlalchemy import create_engine, text
    import urllib
except ImportError:
    print("\n⚠️  pyodbc / sqlalchemy not installed.")
    print("   Run:  pip install pyodbc sqlalchemy")
    print("   Then re-run this script.")
    raise SystemExit

# ── Build connection string ────────────────────────────────────────────────────
if USE_WINDOWS_AUTH:
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER_NAME};"
        f"Trusted_Connection=yes;"
    )
else:
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER_NAME};"
        f"UID={SQL_USER};PWD={SQL_PASSWORD};"
    )

params = urllib.parse.quote_plus(conn_str)

# ── Step 1: Create the database if it does not exist ──────────────────────────
print(f"\nConnecting to SQL Server (server='{SERVER_NAME}')...")
engine_master = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params}",
    connect_args={"autocommit": True}
)

with engine_master.connect() as con:
    result = con.execute(
        text(f"SELECT name FROM sys.databases WHERE name = '{DATABASE}'")
    ).fetchone()
    if result is None:
        con.execute(text(f"CREATE DATABASE [{DATABASE}]"))
        print(f"  ✅ Database '{DATABASE}' created.")
    else:
        print(f"  ℹ️  Database '{DATABASE}' already exists.")

# ── Step 2: Connect to CarRentalOLTP ──────────────────────────────────────────
conn_str_db = conn_str + f"DATABASE={DATABASE};"
params_db   = urllib.parse.quote_plus(conn_str_db)
engine      = create_engine(f"mssql+pyodbc:///?odbc_connect={params_db}")

# ── Step 3: Create the RentalTransactions table ────────────────────────────────
CREATE_TABLE_SQL = """
IF OBJECT_ID('dbo.RentalTransactions', 'U') IS NOT NULL
    DROP TABLE dbo.RentalTransactions;

CREATE TABLE dbo.RentalTransactions (
    Rental_ID                  INT           PRIMARY KEY,
    Rental_Start_Date          DATE          NOT NULL,
    Rental_End_Date            DATE          NOT NULL,
    Rental_Duration_Days       INT           NOT NULL,
    Branch_Name                VARCHAR(100)  NOT NULL,
    Car_Brand                  VARCHAR(50)   NOT NULL,
    Car_Model                  VARCHAR(50)   NOT NULL,
    Vehicle_Year               INT           NOT NULL,
    Engine_CC                  INT           NOT NULL,
    Fuel_Type                  VARCHAR(20)   NOT NULL,
    Transmission               VARCHAR(20)   NOT NULL,
    Mileage_KM                 INT           NOT NULL,
    Body_Type                  VARCHAR(30)   NOT NULL,
    Color                      VARCHAR(30)   NOT NULL,
    Payment_Method             VARCHAR(30)   NOT NULL,
    Insurance_Type             VARCHAR(30)   NOT NULL,
    Daily_Rate_LKR             DECIMAL(12,2) NOT NULL,
    Rental_Cost_LKR            DECIMAL(12,2) NOT NULL,
    Insurance_Fee_LKR          DECIMAL(12,2) NOT NULL,
    Additional_Driver_Fee_LKR  DECIMAL(12,2) NOT NULL,
    Fuel_Charge_LKR            DECIMAL(12,2) NOT NULL,
    Total_Amount_LKR           DECIMAL(12,2) NOT NULL,
    Staff_ID                   INT           NOT NULL,
    Vehicle_Status             VARCHAR(20)   NOT NULL,
    Year                       INT           NOT NULL,
    Month                      INT           NOT NULL
);
"""

print("\nCreating table dbo.RentalTransactions...")
with engine.connect() as con:
    con.execute(text(CREATE_TABLE_SQL))
    con.commit()
print("  ✅ Table created.")

# ── Step 4: Load the CSV and insert in batches ─────────────────────────────────
print("\nLoading rental_data.csv for insert...")
rental_df = pd.read_csv(RENTAL_OUTPUT_CSV)

# Ensure correct types for SQL insert
rental_df["Rental_Start_Date"] = pd.to_datetime(rental_df["Rental_Start_Date"])
rental_df["Rental_End_Date"]   = pd.to_datetime(rental_df["Rental_End_Date"])

int_cols = ["Rental_ID","Rental_Duration_Days","Vehicle_Year",
            "Engine_CC","Mileage_KM","Staff_ID","Year","Month"]
for col in int_cols:
    rental_df[col] = rental_df[col].astype(int)

dec_cols = ["Daily_Rate_LKR","Rental_Cost_LKR","Insurance_Fee_LKR",
            "Additional_Driver_Fee_LKR","Fuel_Charge_LKR","Total_Amount_LKR"]
for col in dec_cols:
    rental_df[col] = rental_df[col].astype(float)

BATCH_SIZE = 5000
total = len(rental_df)
print(f"  Inserting {total:,} rows in batches of {BATCH_SIZE}...")

for start in range(0, total, BATCH_SIZE):
    batch = rental_df.iloc[start : start + BATCH_SIZE]
    batch.to_sql(
        "RentalTransactions",
        con=engine,
        schema="dbo",
        if_exists="append",
        index=False,
        method="multi"
    )
    print(f"  Inserted rows {start+1:,} – {min(start+BATCH_SIZE, total):,}")

print(f"\n✅ All {total:,} rows loaded into [{DATABASE}].[dbo].[RentalTransactions]")

# ── Step 5: Quick validation ───────────────────────────────────────────────────
print("\nValidation query:")
with engine.connect() as con:
    result = con.execute(text("""
        SELECT
            COUNT(*)            AS TotalRows,
            MIN(Rental_Start_Date) AS EarliestDate,
            MAX(Rental_Start_Date) AS LatestDate,
            COUNT(DISTINCT Branch_Name) AS Branches,
            COUNT(DISTINCT Car_Brand)   AS CarBrands,
            SUM(Total_Amount_LKR)       AS TotalRevenue
        FROM dbo.RentalTransactions
    """)).fetchone()

print(f"  Total rows    : {result[0]:,}")
print(f"  Date range    : {result[1]}  →  {result[2]}")
print(f"  Branches      : {result[3]}")
print(f"  Car brands    : {result[4]}")
print(f"  Total revenue : LKR {result[5]:,.2f}")
print("\n✅ PART B complete.")
