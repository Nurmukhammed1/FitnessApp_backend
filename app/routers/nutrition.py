from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.nutrition import (
    NutritionLogCreate, NutritionLogRead,
    DailySummary, MealsByType,
    WaterLogCreate, WaterLogRead,
    NutritionGoalRead, NutritionGoalUpdate,
)
from app.services import nutrition_service

router = APIRouter(prefix="/api/nutrition", tags=["nutrition"])


# ── Nutrition logs ──

@router.post("/log", response_model=NutritionLogRead, status_code=201)
async def create_log(data: NutritionLogCreate, db: AsyncSession = Depends(get_db)):
    return await nutrition_service.create_log(data, db)


@router.delete("/log/{log_id}", status_code=204)
async def delete_log(log_id: str, db: AsyncSession = Depends(get_db)):
    await nutrition_service.delete_log(log_id, db)


@router.get("/summary", response_model=DailySummary)
async def get_summary(
    userId: str = Query(...),
    date: date = Query(...),
    db: AsyncSession = Depends(get_db),
):
    return await nutrition_service.get_daily_summary(userId, date, db)


@router.get("/meals", response_model=MealsByType)
async def get_meals(
    userId: str = Query(...),
    date: date = Query(...),
    db: AsyncSession = Depends(get_db),
):
    return await nutrition_service.get_meals_by_type(userId, date, db)


# ── Water ──

@router.post("/water", response_model=WaterLogRead, status_code=201)
async def log_water(data: WaterLogCreate, db: AsyncSession = Depends(get_db)):
    return await nutrition_service.log_water(data, db)


# ── Goals ──

@router.get("/goals", response_model=NutritionGoalRead)
async def get_goals(userId: str = Query(...), db: AsyncSession = Depends(get_db)):
    return await nutrition_service.get_goals(userId, db)


@router.put("/goals", response_model=NutritionGoalRead)
async def update_goals(data: NutritionGoalUpdate, db: AsyncSession = Depends(get_db)):
    return await nutrition_service.update_goals(data, db)
