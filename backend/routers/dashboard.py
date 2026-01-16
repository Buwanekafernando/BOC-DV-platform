from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from models.db_models import User, Dashboard
from models.schemas import DashboardCreate
from utils.auth import get_current_user
from database import get_db

router = APIRouter(prefix="/dashboards", tags=["Dashboard"])

@router.post("/", status_code=201)
def save_dashboard(
    dashboard_in: DashboardCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Create new Dashboard instance
        new_dashboard = Dashboard(
            user_id=current_user.id,
            dataset_id=dashboard_in.dataset_id,
            name=dashboard_in.name,
            # Serialize JSON fields as they are defined as String columns in the model
            filters=json.dumps(dashboard_in.filters) if dashboard_in.filters else None,
            charts=json.dumps([c.dict() for c in dashboard_in.charts]) if dashboard_in.charts else None,
            layout=json.dumps(dashboard_in.layout) if dashboard_in.layout else None
        )
        
        db.add(new_dashboard)
        db.commit()
        db.refresh(new_dashboard)
        
        return {"dashboard_id": str(new_dashboard.id)}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

@router.get("/")
def list_dashboards(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    dashboards = db.query(Dashboard).filter(Dashboard.user_id == current_user.id).order_by(Dashboard.created_at.desc()).all()
    
    # Return basic metadata for listing
    return [
        {
            "id": str(d.id),
            "name": d.name,
            "created_at": d.created_at
        }
        for d in dashboards
    ]

@router.put("/{dashboard_id}", status_code=200)
def update_dashboard(
    dashboard_id: str,
    dashboard_in: DashboardCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    dashboard = db.query(Dashboard).filter(
        Dashboard.id == dashboard_id,
        Dashboard.user_id == current_user.id
    ).first()
    
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
        
    try:
        dashboard.name = dashboard_in.name
        dashboard.dataset_id = dashboard_in.dataset_id
        dashboard.filters = json.dumps(dashboard_in.filters) if dashboard_in.filters else None
        dashboard.charts = json.dumps([c.dict() for c in dashboard_in.charts]) if dashboard_in.charts else None
        dashboard.layout = json.dumps(dashboard_in.layout) if dashboard_in.layout else None
        
        db.commit()
        db.refresh(dashboard)
        return {"dashboard_id": str(dashboard.id), "message": "Updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

@router.delete("/{dashboard_id}", status_code=204)
def delete_dashboard(
    dashboard_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    dashboard = db.query(Dashboard).filter(
        Dashboard.id == dashboard_id,
        Dashboard.user_id == current_user.id
    ).first()
    
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
        
    try:
        db.delete(dashboard)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    return None

@router.get("/{dashboard_id}")
def get_dashboard(
    dashboard_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    dashboard = db.query(Dashboard).filter(
        Dashboard.id == dashboard_id,
        Dashboard.user_id == current_user.id
    ).first()
    
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
        
    # Prepare response with parsed JSON
    return {
        "id": str(dashboard.id),
        "dataset_id": str(dashboard.dataset_id),
        "name": dashboard.name,
        "filters": json.loads(dashboard.filters) if dashboard.filters else {},
        "charts": json.loads(dashboard.charts) if dashboard.charts else [],
        "layout": json.loads(dashboard.layout) if dashboard.layout else {},
        "created_at": dashboard.created_at
    }