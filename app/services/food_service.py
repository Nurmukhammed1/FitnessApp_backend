from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.food import Food
from app.models.nutrition import NutritionLog
from app.schemas.food import FoodRead


async def search_foods(query: str, db: AsyncSession) -> list[FoodRead]:
    stmt = select(Food).where(
        or_(
            Food.name_en.ilike(f"%{query}%"),
            Food.name_ru.ilike(f"%{query}%"),
        )
    ).limit(50)
    result = await db.execute(stmt)
    foods = result.scalars().all()
    return [FoodRead.model_validate(f) for f in foods]


async def get_recent_foods(user_id: str, limit: int, db: AsyncSession) -> list[FoodRead]:
    # Find distinct food_ids recently logged by user
    subq = (
        select(NutritionLog.food_id)
        .where(NutritionLog.user_id == user_id, NutritionLog.food_id.is_not(None))
        .order_by(NutritionLog.logged_at.desc())
        .distinct()
        .limit(limit)
    ).subquery()

    stmt = select(Food).where(Food.id.in_(select(subq)))
    result = await db.execute(stmt)
    foods = result.scalars().all()
    return [FoodRead.model_validate(f) for f in foods]


async def get_food(food_id: str, db: AsyncSession) -> FoodRead:
    food = await db.get(Food, food_id)
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
    return FoodRead.model_validate(food)
