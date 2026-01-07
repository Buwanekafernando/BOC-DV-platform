from fastapi import APIRouter, Depends
from seaborn import load_dataset
from app.services.forecasting_service import forecast_time_series
from app.services.jwt_dependency import get_current_user

router = APIRouter(prefix="/analytics")

@router.post("/forecast")
def forecast(data: dict, user=Depends(get_current_user)):
    df = load_dataset(data["dataset_id"], user["id"])

    return forecast_time_series(
        df,
        data["date_column"],
        data["value_column"],
        data.get("periods", 12)
    )
