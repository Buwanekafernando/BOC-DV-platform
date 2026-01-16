from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.db_models import User
from models.schemas import QueryRequest, QueryResponse
from utils.auth import get_current_user
from utils.dataset_manager import DatasetManager
from services.query_engine import QueryEngine
import json

router = APIRouter(prefix="/query", tags=["Query"])

@router.post("/{dataset_id}", response_model=QueryResponse)
async def execute_query(
    dataset_id: str,
    query: QueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute a query on a dataset with filters and aggregations"""
    dataset = DatasetManager.verify_dataset_access(db, dataset_id, current_user)
    
    transformations = json.loads(dataset.transformations) if dataset.transformations else []
    measures = json.loads(dataset.measures) if dataset.measures else []
    
    try:
        result = QueryEngine.execute_query(dataset.file_path, query, transformations, measures)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing query: {str(e)}"
        )

@router.post("/{dataset_id}/preview", response_model=QueryResponse)
async def preview_data(
    dataset_id: str,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Preview first N rows of a dataset"""
    dataset = DatasetManager.verify_dataset_access(db, dataset_id, current_user)
    
    transformations = json.loads(dataset.transformations) if dataset.transformations else []
    measures = json.loads(dataset.measures) if dataset.measures else []
    
    try:
        result = QueryEngine.preview_data(dataset.file_path, limit, transformations, measures)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error previewing data: {str(e)}"
        )
