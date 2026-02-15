from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.workout import WorkoutCreate, WorkoutRead, WorkoutStats
from app.services import workout_service

router = APIRouter(prefix="/api/workouts", tags=["workouts"])


@router.post("", response_model=WorkoutRead, status_code=201)
async def create_workout(data: WorkoutCreate, db: AsyncSession = Depends(get_db)):
    return await workout_service.create_workout(data, db)


@router.get("", response_model=list[WorkoutRead])
async def get_workouts(userId: str = Query(...), db: AsyncSession = Depends(get_db)):
    return await workout_service.get_workouts(userId, db)


@router.delete("/{workout_id}", status_code=204)
async def delete_workout(workout_id: str, db: AsyncSession = Depends(get_db)):
    await workout_service.delete_workout(workout_id, db)


@router.get("/stats", response_model=WorkoutStats)
async def get_stats(userId: str = Query(...), db: AsyncSession = Depends(get_db)):
    return await workout_service.get_workout_stats(userId, db)
