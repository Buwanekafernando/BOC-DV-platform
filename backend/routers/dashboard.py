from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.db_models import User
from models.schemas import DashboardCreate
from utils.auth import get_current_user
from utils.dataset_manager import DatasetManager
from services.query_engine import QueryEngine
from database import execute_query, fetch_all
import json



router = APIRouter(prefix="/dashboard", tags=["Dashboard"])



@router.post("/dashboards")
def save_dashboard(
    dashboard: DashboardCreate,
    user: User = Depends(get_current_user)
):
    query = """
        INSERT INTO dashboards (user_id, name, dataset_id, filters, charts, layout)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """
    
    result = execute_query(
        query,
        (
            str(user.id),
            dashboard.name,
            dashboard.dataset_id,
            json.dumps(dashboard.filters),
            json.dumps([c.dict() for c in dashboard.charts]),
            json.dumps(dashboard.layout)
        )
    )
    dashboard_id = result.fetchone()[0]

    return {"dashboard_id": dashboard_id}
#List dashboards for the current user

@router.get("/dashboards")
def list_dashboards(user: User = Depends(get_current_user)):
    query = """
        SELECT id, name, created_at
        FROM dashboards
        WHERE user_id = %s
        ORDER BY created_at DESC
    """
    return fetch_all(query, (str(user.id),))