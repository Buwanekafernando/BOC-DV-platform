from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
import shutil
from database import get_db


from models.db_models import User, Dataset
from models.schemas import DatasetUploadResponse, DatasetMetadata, DataProfileResponse
from utils.auth import get_current_user
from utils.dataset_manager import DatasetManager
from utils.validators import validate_csv_file
from services.data_profiler import DataProfiler
from config import settings

router = APIRouter(prefix="/datasets", tags=["Datasets"])

@router.post("/upload", response_model=DatasetUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a CSV dataset"""
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are allowed"
        )
    
    # Generate unique dataset ID
    dataset_id = str(uuid.uuid4())
    file_path = os.path.join(settings.UPLOAD_DIR, f"{dataset_id}.csv")
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )
    
    # Validate CSV
    validate_csv_file(file_path, settings.MAX_UPLOAD_SIZE // (1024 * 1024))
    
    # Get file size and row count
    file_size = os.path.getsize(file_path)
    row_count = DataProfiler.get_row_count(file_path)
    
    # Create database record
    dataset = Dataset(
        id=dataset_id,
        filename=f"{dataset_id}.csv",
        original_filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        row_count=row_count,
        user_id=current_user.id
    )
    
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    
    return DatasetUploadResponse(
        dataset_id=dataset_id,
        filename=file.filename,
        file_size=file_size,
        message="File uploaded successfully"
    )

@router.get("/", response_model=List[DatasetMetadata])
async def list_datasets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all datasets for current user"""
    datasets = DatasetManager.get_user_datasets(db, current_user.id)
    return datasets

@router.get("/{dataset_id}", response_model=DatasetMetadata)
async def get_dataset(
    dataset_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dataset metadata"""
    dataset = DatasetManager.verify_dataset_access(db, dataset_id, current_user)
    return dataset

@router.get("/{dataset_id}/profile", response_model=DataProfileResponse)
async def profile_dataset(
    dataset_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get data profiling results for a dataset"""
    dataset = DatasetManager.verify_dataset_access(db, dataset_id, current_user)
    
    try:
        profile = DataProfiler.profile_dataset(dataset.file_path)
        profile["dataset_id"] = dataset_id
        return profile
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error profiling dataset: {str(e)}"
        )

@router.delete("/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dataset(
    dataset_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a dataset"""
    DatasetManager.delete_dataset(db, dataset_id, current_user)
    return None
