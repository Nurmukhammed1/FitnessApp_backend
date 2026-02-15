from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# ── Request ──

class SetCreate(BaseModel):
    reps: int | None = None
    weight: float | None = None
    duration: float | None = None
    completed: bool = False
    order_index: int = 0


class ExerciseCreate(BaseModel):
    name: str
    exercise_type: str | None = None
    order_index: int = 0
    sets: list[SetCreate] = []


class WorkoutCreate(BaseModel):
    userId: str
    startTime: datetime
    endTime: datetime | None = None
    notes: str | None = None
    xpEarned: int = 0
    exercises: list[ExerciseCreate] = []


# ── Response ──

class SetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    reps: int | None = None
    weight: float | None = None
    duration: float | None = None
    completed: bool
    order_index: int


class ExerciseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    exercise_type: str | None = None
    order_index: int
    sets: list[SetRead] = []


class WorkoutRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    userId: str = Field(alias="user_id")
    startTime: datetime = Field(alias="start_time")
    endTime: datetime | None = Field(None, alias="end_time")
    notes: str | None = None
    xpEarned: int = Field(alias="xp_earned")
    exercises: list[ExerciseRead] = []


class WorkoutStats(BaseModel):
    totalCount: int
    weeklyCount: int
