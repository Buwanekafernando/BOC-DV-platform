from fastapi import APIRouter, Depends

from app.services.jwt_dependency import get_current_user

router = APIRouter(prefix="/share")

@router.post("/dashboard")
def share_dashboard(data: dict, user=Depends(get_current_user)):
    query = """
        INSERT INTO dashboard_shares (dashboard_id, shared_with, permission)
        VALUES (%s, %s, %s)
    """
    execute_query(query, (
        data["dashboard_id"],
        data["user_id"],
        data.get("permission", "view")
    ))

    return {"status": "shared"}
#Retrieve dashboards shared with the current user

@router.get("/dashboard")
def get_shared_dashboards(user=Depends(get_current_user)):
    query = """
        SELECT d.*
        FROM dashboards d
        JOIN dashboard_shares s ON d.id = s.dashboard_id
        WHERE s.shared_with = %s
    """
    return fetch_all(query, (user["id"],))



