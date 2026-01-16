from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.db_models import User, Dataset
from models.schemas import DatasetMeasuresUpdate, QueryResponse
from utils.auth import get_current_user
from utils.dataset_manager import DatasetManager
from services.query_engine import QueryEngine
import json

router = APIRouter(prefix="/data-modeling", tags=["Data Modeling"])

@router.post("/{dataset_id}/preview", response_model=QueryResponse)
async def preview_measures(
    dataset_id: str,
    measures_update: DatasetMeasuresUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Preview measures on a dataset without saving"""
    dataset = DatasetManager.verify_dataset_access(db, dataset_id, current_user)
    
    # Existing transformations
    transformations = json.loads(dataset.transformations) if dataset.transformations else []
    
    try:
        measures = [m.dict() for m in measures_update.measures]
        result = QueryEngine.preview_data(dataset.file_path, 50, transformations, measures)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error previewing measures: {str(e)}"
        )

@router.put("/{dataset_id}/save")
async def save_measures(
    dataset_id: str,
    measures_update: DatasetMeasuresUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save measure definitions to the dataset"""
    dataset = DatasetManager.verify_dataset_access(db, dataset_id, current_user)
    
    try:
        measures = [m.dict() for m in measures_update.measures]
        dataset.measures = json.dumps(measures)
        db.commit()
        return {"message": "Measures saved successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving measures: {str(e)}"
        )
