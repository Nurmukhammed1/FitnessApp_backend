from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import engine, Base

# Import all models so Base.metadata knows about them
from app.models import (  # noqa: F401
    User, Workout, Exercise, ExerciseSet,
    Food, NutritionLog, NutritionGoal, WaterLog, SavedMeal,
)

from app.routers import auth, workouts, foods, nutrition


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (dev convenience – use Alembic in production)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

# ── Register routers ──
app.include_router(auth.router)
app.include_router(workouts.router)
app.include_router(foods.router)
app.include_router(nutrition.router)


@app.get("/")
async def root():
    return {"message": f"{settings.PROJECT_NAME} API is running"}
