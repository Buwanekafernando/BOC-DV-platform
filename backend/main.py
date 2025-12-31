from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import uuid
import shutil

app = FastAPI(title="BI Software Backend")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "BI Software Backend is running"}

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    # Generate unique dataset ID
    dataset_id = str(uuid.uuid4())

    # Save file
    file_path = os.path.join(UPLOAD_DIR, f"{dataset_id}.csv")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "dataset_id": dataset_id,
        "filename": file.filename
    }
