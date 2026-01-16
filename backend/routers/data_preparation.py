from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.db_models import User, Dataset
from models.schemas import DatasetTransformUpdate, QueryResponse
from utils.auth import get_current_user
from utils.dataset_manager import DatasetManager
from services.query_engine import QueryEngine
import json

router = APIRouter(prefix="/data-prep", tags=["Data Preparation"])

@router.post("/{dataset_id}/preview", response_model=QueryResponse)
async def preview_transformations(
    dataset_id: str,
    transform_update: DatasetTransformUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Preview transformations on a dataset without saving"""
    dataset = DatasetManager.verify_dataset_access(db, dataset_id, current_user)
    
    # Existing measures
    measures = json.loads(dataset.measures) if dataset.measures else []
    
    try:
        # Convert Pydantic objects to dicts for the service
        steps = [step.dict() for step in transform_update.transformations]
        result = QueryEngine.preview_data(dataset.file_path, 50, steps, measures)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error previewing transformations: {str(e)}"
        )

@router.put("/{dataset_id}/save")
async def save_transformations(
    dataset_id: str,
    transform_update: DatasetTransformUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save transformation steps to the dataset"""
    dataset = DatasetManager.verify_dataset_access(db, dataset_id, current_user)
    
    try:
        steps = [step.dict() for step in transform_update.transformations]
        dataset.transformations = json.dumps(steps)
        db.commit()
        return {"message": "Transformations saved successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving transformations: {str(e)}"
        )
