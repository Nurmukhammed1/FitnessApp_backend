from datetime import datetime, timedelta, timezone

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.workout import Workout, Exercise, ExerciseSet
from app.schemas.workout import WorkoutCreate, WorkoutRead, WorkoutStats


async def create_workout(data: WorkoutCreate, db: AsyncSession) -> WorkoutRead:
    workout = Workout(
        user_id=data.userId,
        start_time=data.startTime,
        end_time=data.endTime,
        notes=data.notes,
        xp_earned=data.xpEarned,
    )
    db.add(workout)
    await db.flush()

    for ex_data in data.exercises:
        exercise = Exercise(
            workout_id=workout.id,
            name=ex_data.name,
            exercise_type=ex_data.exercise_type,
            order_index=ex_data.order_index,
        )
        db.add(exercise)
        await db.flush()

        for s_data in ex_data.sets:
            s = ExerciseSet(
                exercise_id=exercise.id,
                reps=s_data.reps,
                weight=s_data.weight,
                duration=s_data.duration,
                completed=s_data.completed,
                order_index=s_data.order_index,
            )
            db.add(s)

    await db.flush()

    # Reload with relationships
    result = await db.execute(
        select(Workout)
        .where(Workout.id == workout.id)
        .options(selectinload(Workout.exercises).selectinload(Exercise.sets))
    )
    workout = result.scalar_one()
    return WorkoutRead.model_validate(workout)


async def get_workouts(user_id: str, db: AsyncSession) -> list[WorkoutRead]:
    result = await db.execute(
        select(Workout)
        .where(Workout.user_id == user_id)
        .options(selectinload(Workout.exercises).selectinload(Exercise.sets))
        .order_by(Workout.start_time.desc())
    )
    workouts = result.scalars().all()
    return [WorkoutRead.model_validate(w) for w in workouts]


async def delete_workout(workout_id: str, db: AsyncSession) -> None:
    result = await db.execute(select(Workout).where(Workout.id == workout_id))
    workout = result.scalar_one_or_none()
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    await db.delete(workout)
    await db.flush()


async def get_workout_stats(user_id: str, db: AsyncSession) -> WorkoutStats:
    # Total count
    total_q = await db.execute(
        select(func.count(Workout.id)).where(Workout.user_id == user_id)
    )
    total_count = total_q.scalar() or 0

    # Weekly count
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    weekly_q = await db.execute(
        select(func.count(Workout.id)).where(
            Workout.user_id == user_id,
            Workout.start_time >= week_ago,
        )
    )
    weekly_count = weekly_q.scalar() or 0

    return WorkoutStats(totalCount=total_count, weeklyCount=weekly_count)
