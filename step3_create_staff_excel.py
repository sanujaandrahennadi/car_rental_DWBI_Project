# =============================================================================
# TASK 2 – Step 3: Generate staff_info.xlsx (Source 3 – optional enrichment)
# =============================================================================
# The original dataset contains only Staff_ID (integers 1–14).
# This script creates a realistic staff lookup table and saves it as an
# Excel file (.xlsx) to serve as the third data source type.
#
# Output  : staff_info.xlsx
# Columns : Staff_ID, Staff_Name, Designation, Branch_Name,
#           Email, Phone, Years_Experience, Employment_Type
# =============================================================================

import pandas as pd
import os

OUTPUT_FILE = "staff_info.xlsx"

# ── Staff data (realistic Sri Lankan names, 14 staff across 5 branches) ───────
staff_data = [
    # Staff_ID, Staff_Name,         Designation,       Branch_Name,               Email,                          Phone,         Years_Exp, Employment
    (1,  "Kamal Perera",        "Branch Manager",  "Colombo City Rentals",        "k.perera@carrental.lk",       "0711234567",  8,  "Full-Time"),
    (2,  "Nimal Silva",         "Senior Agent",    "Negombo Airport Rentals",     "n.silva@carrental.lk",        "0722345678",  6,  "Full-Time"),
    (3,  "Amali Fernando",      "Rental Agent",    "Kandy Drive Hub",             "a.fernando@carrental.lk",     "0733456789",  3,  "Full-Time"),
    (4,  "Ruwan Jayawardena",   "Branch Manager",  "Kandy Drive Hub",             "r.jayawardena@carrental.lk",  "0744567890",  10, "Full-Time"),
    (5,  "Ishara Dissanayake",  "Rental Agent",    "Negombo Airport Rentals",     "i.dissanayake@carrental.lk",  "0755678901",  2,  "Full-Time"),
    (6,  "Priya Wickramasinghe","Senior Agent",    "Galle Coastal Cars",          "p.wickramasinghe@carrental.lk","0766789012", 5,  "Full-Time"),
    (7,  "Chaminda Rajapaksa",  "Rental Agent",    "Colombo City Rentals",        "c.rajapaksa@carrental.lk",    "0777890123",  4,  "Full-Time"),
    (8,  "Sandya Kumari",       "Customer Support","Jaffna Auto Rent",            "s.kumari@carrental.lk",       "0788901234",  3,  "Full-Time"),
    (9,  "Thilina Bandara",     "Branch Manager",  "Galle Coastal Cars",          "t.bandara@carrental.lk",      "0799012345",  9,  "Full-Time"),
    (10, "Dilrukshi Mendis",    "Senior Agent",    "Colombo City Rentals",        "d.mendis@carrental.lk",       "0710123456",  7,  "Full-Time"),
    (11, "Ashan Rathnayake",    "Rental Agent",    "Jaffna Auto Rent",            "a.rathnayake@carrental.lk",   "0721234567",  2,  "Part-Time"),
    (12, "Fathima Rauf",        "Branch Manager",  "Jaffna Auto Rent",            "f.rauf@carrental.lk",         "0732345678",  11, "Full-Time"),
    (13, "Prasad Gunasekara",   "Rental Agent",    "Negombo Airport Rentals",     "p.gunasekara@carrental.lk",   "0743456789",  1,  "Part-Time"),
    (14, "Malsha Hettiarachchi","Customer Support","Kandy Drive Hub",             "m.hettiarachchi@carrental.lk","0754567890",  4,  "Full-Time"),
]

columns = [
    "Staff_ID", "Staff_Name", "Designation", "Branch_Name",
    "Email", "Phone", "Years_Experience", "Employment_Type"
]

staff_df = pd.DataFrame(staff_data, columns=columns)

# ── Print preview ──────────────────────────────────────────────────────────────
print("Staff table preview:")
print(staff_df.to_string(index=False))
print(f"\nTotal staff : {len(staff_df)}")
print(f"Designations: {sorted(staff_df['Designation'].unique())}")
print(f"Branches    : {sorted(staff_df['Branch_Name'].unique())}")

# ── Save as Excel (.xlsx) ──────────────────────────────────────────────────────
# Using openpyxl engine — install with: pip install openpyxl
with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    staff_df.to_excel(writer, sheet_name="StaffInfo", index=False)

    # Auto-adjust column widths for readability
    worksheet = writer.sheets["StaffInfo"]
    for col_cells in worksheet.columns:
        max_len = max(len(str(cell.value or "")) for cell in col_cells)
        col_letter = col_cells[0].column_letter
        worksheet.column_dimensions[col_letter].width = max_len + 4

size_kb = os.path.getsize(OUTPUT_FILE) / 1024
print(f"\n✅ Saved '{OUTPUT_FILE}'  ({size_kb:.1f} KB)")
print(f"   Sheet: StaffInfo  |  {len(staff_df)} rows  |  {len(columns)} columns")
print(f"   Columns: {columns}")
