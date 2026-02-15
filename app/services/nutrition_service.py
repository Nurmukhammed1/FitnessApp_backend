from datetime import date

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.nutrition import NutritionLog, NutritionGoal, WaterLog
from app.schemas.nutrition import (
    NutritionLogCreate, NutritionLogRead,
    DailySummary, MealsByType,
    WaterLogCreate, WaterLogRead,
    NutritionGoalRead, NutritionGoalUpdate,
)


# ── Nutrition Logs ──

async def create_log(data: NutritionLogCreate, db: AsyncSession) -> NutritionLogRead:
    log = NutritionLog(
        user_id=data.userId,
        food_id=data.foodId,
        food_name=data.foodName,
        meal_type=data.mealType,
        servings=data.servings,
        calories=data.calories,
        protein=data.protein,
        carbs=data.carbs,
        fats=data.fats,
        date=data.date,
    )
    db.add(log)
    await db.flush()
    return NutritionLogRead.model_validate(log)


async def delete_log(log_id: str, db: AsyncSession) -> None:
    result = await db.execute(select(NutritionLog).where(NutritionLog.id == log_id))
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nutrition log not found")
    await db.delete(log)
    await db.flush()


async def get_daily_summary(user_id: str, day: date, db: AsyncSession) -> DailySummary:
    # Nutrition totals
    stmt = select(
        func.coalesce(func.sum(NutritionLog.calories), 0),
        func.coalesce(func.sum(NutritionLog.protein), 0),
        func.coalesce(func.sum(NutritionLog.carbs), 0),
        func.coalesce(func.sum(NutritionLog.fats), 0),
    ).where(NutritionLog.user_id == user_id, NutritionLog.date == day)

    row = (await db.execute(stmt)).one()

    # Water total
    water_stmt = select(
        func.coalesce(func.sum(WaterLog.amount), 0)
    ).where(WaterLog.user_id == user_id, WaterLog.date == day)
    water = (await db.execute(water_stmt)).scalar() or 0

    return DailySummary(
        calories=row[0], protein=row[1], carbs=row[2], fats=row[3], water=water
    )


async def get_meals_by_type(user_id: str, day: date, db: AsyncSession) -> MealsByType:
    result = await db.execute(
        select(NutritionLog)
        .where(NutritionLog.user_id == user_id, NutritionLog.date == day)
        .order_by(NutritionLog.logged_at)
    )
    logs = result.scalars().all()
    grouped = MealsByType()
    for log in logs:
        entry = NutritionLogRead.model_validate(log)
        getattr(grouped, log.meal_type).append(entry)
    return grouped


# ── Water ──

async def log_water(data: WaterLogCreate, db: AsyncSession) -> WaterLogRead:
    from datetime import date as _date, datetime, timezone

    water = WaterLog(
        user_id=data.userId,
        amount=data.amount,
        date=_date.today(),
    )
    db.add(water)
    await db.flush()
    return WaterLogRead.model_validate(water)


# ── Goals ──

async def get_goals(user_id: str, db: AsyncSession) -> NutritionGoalRead:
    goal = await db.get(NutritionGoal, user_id)
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goals not found")
    return NutritionGoalRead.model_validate(goal)


async def update_goals(data: NutritionGoalUpdate, db: AsyncSession) -> NutritionGoalRead:
    goal = await db.get(NutritionGoal, data.userId)
    if not goal:
        goal = NutritionGoal(user_id=data.userId)
        db.add(goal)

    goal.daily_calories = data.dailyCalories
    goal.protein_goal = data.proteinGoal
    goal.carbs_goal = data.carbsGoal
    goal.fats_goal = data.fatsGoal
    goal.water_goal = data.waterGoal
    await db.flush()
    return NutritionGoalRead.model_validate(goal)
