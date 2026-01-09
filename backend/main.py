
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from tempfile import NamedTemporaryFile
from typing import List


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
RESULT_DIR = "results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

@app.post("/upload/soh")
def upload_soh(file: UploadFile = File(...)):
    temp_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(temp_path, "wb") as f:
        f.write(file.file.read())
    df = pd.read_excel(temp_path)
    # Pivot table
    pivot = pd.pivot_table(df, index=["Name", "Material Code", "Material Description"], values=["Alternate Unit Qty"], aggfunc="sum").reset_index()
    pivot.rename(columns={"Name": "city", "Alternate Unit Qty": "Total Qty"}, inplace=True)
    pivot["city"] = pivot["city"].astype(str).str[8:]
    result_path = os.path.join(RESULT_DIR, "Fresh_SOH.xlsx")
    pivot.to_excel(result_path, index=False)
    return {"download_url": "/download/Fresh_SOH.xlsx"}

@app.post("/upload/frpo")
def upload_frpo(file: UploadFile = File(...)):
    temp_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(temp_path, "wb") as f:
        f.write(file.file.read())
    df = pd.read_excel(temp_path)

    # --- Hardcoded mappings (fill in your own) ---
    facility_to_city = {
        # Example:
        #"Super Store Dasna 2 - Warehouse": "Ghaziabad",
        # Add more mappings here
        
        "Bhopal B1 - Feeder Warehouse": "Bhopal", 
        "Bhopal B3 - Feeder Warehouse": "Bhopal", 
        "Super Store Dasna 2 - Warehouse": "Ghaziabad", 
        "Indore - Feeder Warehouse": "Indore", 
        "Hyderabad H3 - Feeder Warehouse": "Hyderabad", 
        "Ahmedabad A2 - Feeder Warehouse": "Ahmedabad", 
        "Farukhnagar F2 - Feeder Warehouse": "Gurgaon", 
        "Pune P2 - Feeder Warehouse": "Pune", 
        "Mumbai M10 - Feeder Warehouse": "Mumbai", 
        "Bengaluru B4 - Feeder Warehouse": "Bengaluru",
        "Bengaluru B3 - Feeder Warehouse": "Bengaluru", 
 
        "Farukhnagar - SR Feeder Warehouse": "Jhajjar", 
        "Pune P3 - Feeder Warehouse": "Pune", 
        "Visakhapatnam V1 - Feeder Warehouse": "Visakhapatnam", 
        "Dehradun - Feeder Warehouse": "Dehradun", 
        "Surat S1 - Feeder Warehouse": "Surat", 
        "Mumbai M11 - Feeder Warehouse": "Mumbai", 
        "Nagpur N1 - Feeder Warehouse": "Nagpur", 
        "Kundli - Feeder Warehouse": "Sonipat", 
        "Kolkata K4 - Feeder Warehouse": "Kolkata",
        "Rajpura R2 - Feeder Warehouse": "Rajpura",
        "Dasna D3 - Feeder Warehouse": "Hapur",
        "Ranchi R1 - Feeder Warehouse": "Ranchi",
        "Guwahati G1 - Feeder Warehouse": "Guwahati", 
        "Chennai C5 - Feeder Warehouse": "Chennai", 
        "Coimbatore C1 - Feeder Warehouse": "Coimbatore", 
        "Noida N1 - Feeder Warehouse": "Noida", 
        "Jaipur J3 - Feeder Warehouse": "Jaipur", 
        "Varanasi V1 - Feeder Warehouse": "Varanasi", 
        "Super Store Lucknow L4 - Warehouse": "Lucknow", 
        "Ludhiana L2 - Feeder Warehouse": "Ludhiana", 
        "Lucknow L5 - Feeder Warehouse": "Lucknow", 
        "Kolkata K5 - Feeder Warehouse": "Kolkata",
        "Kolkata K6 - Feeder Warehouse": "Kolkata", 
        "Mumbai M10 - Feeder Warehouse": "Mumbai",
        "Mumbai M11 - Feeder Warehouse": "Mumbai",

 
        "Goa G2 - Feeder Warehouse": "Goa", 
        "Patna P1 - Feeder Warehouse": "Patna"
    }
    facility_to_id = {
        # Example:
        "Super Store Dasna 2 - Warehouse": 2577,
        # Add more mappings here
        "Lucknow L5 - Feeder Warehouse": 2577, ""
        "Pune P3 - Feeder Warehouse": 4572, 
        "Bhopal B1 - Feeder Warehouse": 3821, 
        "Pune P2 - Feeder Warehouse": 1872, 
        "Kundli - Feeder Warehouse": 2010, 
        "Noida N1 - Feeder Warehouse": 2576,
        "Indore - Feeder Warehouse": "2006", 
        "Nagpur N1 - Feeder Warehouse": 2468, 
        "Ahmedabad A2 - Feeder Warehouse": 2470, 
        "Varanasi V1 - Feeder Warehouse": 4571, 
        "Mumbai M11 - Feeder Warehouse": 3164, 
        "Coimbatore C1 - Feeder Warehouse": 2681, 
        "Surat S1 - Feeder Warehouse": 2569, 
        "Super Store Lucknow L4 - Warehouse": 1206, 
        "Kolkata K5 - Feeder Warehouse": 2490, 
        "Rajpura R2 - Feeder Warehouse": 2006, 
        "Bengaluru B4 - Feeder Warehouse": 2142, 
        "Guwahati G1 - Feeder Warehouse": 3213, 
        "Goa G2 - Feeder Warehouse": 4449, 
        "Farukhnagar - SR Feeder Warehouse": 264, 
        "Farukhnagar F2 - Feeder Warehouse": 3126, 
        "Visakhapatnam V1 - Feeder Warehouse": 3127, 
        "Hyderabad H3 - Feeder Warehouse": 3201, 
        "Bengaluru B3 - Feeder Warehouse": 1873, 
        "Ranchi R1 - Feeder Warehouse": 2692, 
        "Dehradun - Feeder Warehouse": 2076, 
        "Ludhiana L2 - Feeder Warehouse": 2947, 
        "Chennai C5 - Feeder Warehouse": 3262, 
        "Dasna D3 - Feeder Warehouse": 2469, 
        "Kolkata K4 - Feeder Warehouse": 2015,
        "Patna P1 - Feeder Warehouse": 2015,

        "Mumbai M10 - Feeder Warehouse": 2123,
        "Mumbai M11 - Feeder Warehouse": 3164,
       
        "Jaipur J3 - Feeder Warehouse": 2960
    }

    # Map city and facility_id
    df["city"] = df["facility_name"].map(facility_to_city)
    df["facility_id"] = df["facility_name"].map(facility_to_id)

    # Select and rename columns
    out = df[["po_number", "order_date", "appointment_date", "expiry_date", "city", "facility_id", "item_id", "units_ordered"]].copy()
    out.rename(columns={
        "order_date": "po_issue_date",
        "expiry_date": "po_expiry_date",
        "units_ordered": "po_qty"
    }, inplace=True)

    # Convert dates to DD-MM-YYYY
    for col in ["po_issue_date", "appointment_date", "po_expiry_date"]:
        out[col] = pd.to_datetime(out[col], errors="coerce").dt.strftime("%d-%m-%Y")

    # Convert numeric columns
    for col in ["facility_id", "item_id", "po_qty", "po_number"]:
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0).astype(int)

    # Final columns order
    out = out[["po_number", "po_issue_date", "po_expiry_date", "facility_id", "city", "item_id", "po_qty"]]

    result_path = os.path.join(RESULT_DIR, "Fresh_FR.xlsx")
    out.to_excel(result_path, index=False)
    return {"download_url": "/download/Fresh_FR.xlsx"}

@app.post("/upload/srdata")
def upload_srdata(file: UploadFile = File(...)):
    temp_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(temp_path, "wb") as f:
        f.write(file.file.read())
    df = pd.read_excel(temp_path)
    cols = ["NAME OF THE EMPLOYEE", "Customer Reference", "Bill-To Street", "Item", "Material", "Quantity"]
    df = df[cols]
    for col in ["Item", "Material", "Quantity", "Customer Reference"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    df.rename(columns={"Customer Reference": "po_number", "Material": "Material Code"}, inplace=True)
    result_path = os.path.join(RESULT_DIR, "SR_Data.xlsx")
    df.to_excel(result_path, index=False)
    return {"download_url": "/download/SR_Data.xlsx"}

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(RESULT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    return {"error": "File not found"}
