from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict


# ── Nutrition Log ──

class NutritionLogCreate(BaseModel):
    userId: str
    foodId: str | None = None
    foodName: str
    mealType: str   # breakfast / lunch / dinner / snack
    servings: float = 1
    calories: float = 0
    protein: float = 0
    carbs: float = 0
    fats: float = 0
    date: date


class NutritionLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    userId: str = Field(alias="user_id")
    foodId: str | None = Field(None, alias="food_id")
    foodName: str = Field(alias="food_name")
    mealType: str = Field(alias="meal_type")
    servings: float
    calories: float
    protein: float
    carbs: float
    fats: float
    loggedAt: datetime = Field(alias="logged_at")
    date: date


# ── Daily Summary ──

class DailySummary(BaseModel):
    calories: float
    protein: float
    carbs: float
    fats: float
    water: float


# ── Meals grouped by type ──

class MealsByType(BaseModel):
    breakfast: list[NutritionLogRead] = []
    lunch: list[NutritionLogRead] = []
    dinner: list[NutritionLogRead] = []
    snack: list[NutritionLogRead] = []


# ── Water Log ──

class WaterLogCreate(BaseModel):
    userId: str
    amount: float


class WaterLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    userId: str = Field(alias="user_id")
    amount: float
    loggedAt: datetime = Field(alias="logged_at")
    date: date


# ── Nutrition Goals ──

class NutritionGoalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    userId: str = Field(alias="user_id")
    dailyCalories: float = Field(alias="daily_calories")
    proteinGoal: float = Field(alias="protein_goal")
    carbsGoal: float = Field(alias="carbs_goal")
    fatsGoal: float = Field(alias="fats_goal")
    waterGoal: float = Field(alias="water_goal")


class NutritionGoalUpdate(BaseModel):
    userId: str
    dailyCalories: float = 2000
    proteinGoal: float = 150
    carbsGoal: float = 250
    fatsGoal: float = 65
    waterGoal: float = 2000
