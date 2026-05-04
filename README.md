# 🚗 CarRentalDW — Data Warehouse & Business Intelligence Project

## 📌 Project Overview
A complete end-to-end DW & BI solution built on a **Sri Lanka Multi-Branch Car Rental dataset** containing **60,000 transactions** across **5 branches** and **4 provinces** over an **18-month period (January 2022 – June 2023)**.

The solution follows a Kimball-style five-layer pipeline architecture:

```
Layer 1 — Data Sources       (rental_data.csv, customer_data.csv, staff_info.xlsx)
Layer 2 — Staging Area       (CarRental_Staging)
Layer 3 — ETL / SSIS         (4 Packages)
Layer 4 — Data Warehouse     (CarRental_DW — Star Schema)
Layer 5 — BI / Reporting     (SSAS Cube + Excel OLAP + Power BI)
```

## 🗄️ Data Warehouse Design
### Star Schema — Tables

| Table | Type | Primary Key | Description |
|---|---|---|---|
| DimDate | Dimension | DateKey (INT) | Calendar dimension Jan 2022 – Dec 2023 |
| DimBranch | Dimension | BranchKey | 5 branches — Province → City → Branch hierarchy |
| DimStaff | Dimension | StaffKey | 14 staff members with designation and experience |
| DimCustomer | Dimension | CustomerKey | 48 demographic segments (Type + Gender + AgeGroup + License) |
| DimVehicle | SCD Type 2 | VehicleKey | 187 vehicles with historical Fuel_Type/Transmission tracking |
| FactRental | Accumulating Fact | RentalSK | 60,000 transactions with 6 FK references |

### Fact Table Measures

| Measure | Type | Aggregation |
|---|---|---|
| Rental_Duration_Days | INT | SUM, AVG |
| Mileage_KM | INT | SUM, AVG |
| Daily_Rate_LKR | DECIMAL(10,2) | AVG, MIN, MAX |
| Rental_Cost_LKR | DECIMAL(10,2) | SUM |
| Insurance_Fee_LKR | DECIMAL(10,2) | SUM |
| Additional_Driver_Fee_LKR | DECIMAL(10,2) | SUM |
| Fuel_Charge_LKR | DECIMAL(10,2) | SUM |
| Total_Amount_LKR | DECIMAL(10,2) | SUM, AVG |
| txn_process_time_hours | FLOAT | AVG |

## ⚙️ ETL Packages (SSIS)

| Package | Purpose | Order |
|---|---|---|
| 01_Load_Staging.dtsx | Loads all 3 source files into staging tables | 1st |
| 02_Load_Dimensions.dtsx | Populates all 5 dimension tables (incl. SCD Type 2) | 2nd |
| 03_Load_FactRental.dtsx | Loads fact table with surrogate key lookups | 3rd |
| 04_Update_AccumulatingFact.dtsx | Updates completion time + process hours | 4th |

## 📊 SSAS Cube — Hierarchies

| Hierarchy | Dimension | Levels |
|---|---|---|
| Calendar | DimDate | Year → Quarter → MonthNumber → DayOfMonth |
| Geography | DimBranch | Province → City → Branch_Name |
| Vehicle | DimVehicle | Car_Brand → Car_Model → Vehicle_Year |

**Cube Name:** CarRental_Cube
**SSAS Database:** CarRentalDW_Cube

## 📈 Power BI Reports

| Report | Description |
|---|---|
| Report 1 — Matrix Visual | Cross-tabulation of Branch × Customer_Type with revenue, duration and count |
| Report 2 — Cascading Slicers | Interactive dashboard with Province → Branch cascading filters and 4 visuals |
| Report 3 — Drill-Down | Date hierarchy drill-down: Year → Quarter → Month → Day |
| Report 4 — Drill-Through | Branch summary → right-click → Branch Detail page |

## 🔧 Tech Stack
- **Database:** Microsoft SQL Server (SSMS)
- **ETL:** SQL Server Integration Services (SSIS) in Visual Studio
- **OLAP Cube:** SQL Server Analysis Services (SSAS) — Multidimensional
- **Reporting:** Power BI Desktop + Power BI Service
- **Excel:** OLAP Pivot Tables (Roll-up, Drill-down, Slice, Dice, Pivot)

## 🚀 Getting Started
See `sql/ddl/` for table creation scripts.

Quick steps:
1. Create `CarRental_DW` and `CarRental_Staging` databases in SSMS
2. Run all scripts in `sql/ddl/` in order
3. Place source files in `data/source-files/`
4. Execute SSIS packages in order (01 → 02 → 03 → 04)
5. Deploy SSAS project from `ssas/` folder
6. Open Power BI report from `powerbi/` folder

