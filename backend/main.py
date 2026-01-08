
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
    cols = ["po_number", "po_issue_date", "po_expiry_date", "facility_id", "city", "item_id", "po_qty"]
    df = df[cols]
    for col in ["facility_id", "item_id", "po_qty", "po_number"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    for col in ["po_issue_date", "po_expiry_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%d-%m-%Y")
    result_path = os.path.join(RESULT_DIR, "Fresh_FR.xlsx")
    df.to_excel(result_path, index=False)
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
