from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.food import FoodRead
from app.services import food_service

router = APIRouter(prefix="/api/foods", tags=["foods"])


@router.get("/search", response_model=list[FoodRead])
async def search_foods(q: str = Query(..., min_length=1), db: AsyncSession = Depends(get_db)):
    return await food_service.search_foods(q, db)


@router.get("/recent", response_model=list[FoodRead])
async def recent_foods(
    userId: str = Query(...),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    return await food_service.get_recent_foods(userId, limit, db)


@router.get("/{food_id}", response_model=FoodRead)
async def get_food(food_id: str, db: AsyncSession = Depends(get_db)):
    return await food_service.get_food(food_id, db)
