import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Float, Integer, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


# ────────────────────────────────────────────
# Nutrition Log
# ────────────────────────────────────────────
class NutritionLog(Base):
    __tablename__ = "nutrition_logs"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    food_id: Mapped[str | None] = mapped_column(
        String(36), nullable=True
    )
    food_name: Mapped[str] = mapped_column(String(255), nullable=False)
    meal_type: Mapped[str] = mapped_column(String(20), nullable=False)  # breakfast/lunch/dinner/snack
    servings: Mapped[float] = mapped_column(Float, default=1)
    calories: Mapped[float] = mapped_column(Float, default=0)
    protein: Mapped[float] = mapped_column(Float, default=0)
    carbs: Mapped[float] = mapped_column(Float, default=0)
    fats: Mapped[float] = mapped_column(Float, default=0)
    logged_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    # ── relationships ──
    user: Mapped["User"] = relationship(back_populates="nutrition_logs")

    def __repr__(self) -> str:
        return f"<NutritionLog(id={self.id}, food_name={self.food_name})>"


# ────────────────────────────────────────────
# Nutrition Goal  (one per user)
# ────────────────────────────────────────────
class NutritionGoal(Base):
    __tablename__ = "nutrition_goals"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    daily_calories: Mapped[float] = mapped_column(Float, default=2000)
    protein_goal: Mapped[float] = mapped_column(Float, default=150)
    carbs_goal: Mapped[float] = mapped_column(Float, default=250)
    fats_goal: Mapped[float] = mapped_column(Float, default=65)
    water_goal: Mapped[float] = mapped_column(Float, default=2000)

    # ── relationships ──
    user: Mapped["User"] = relationship(back_populates="nutrition_goal")

    def __repr__(self) -> str:
        return f"<NutritionGoal(user_id={self.user_id})>"


# ────────────────────────────────────────────
# Water Log
# ────────────────────────────────────────────
class WaterLog(Base):
    __tablename__ = "water_logs"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    logged_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    # ── relationships ──
    user: Mapped["User"] = relationship(back_populates="water_logs")

    def __repr__(self) -> str:
        return f"<WaterLog(id={self.id}, amount={self.amount})>"


# ────────────────────────────────────────────
# Saved Meal
# ────────────────────────────────────────────
class SavedMeal(Base):
    __tablename__ = "saved_meals"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    foods_json: Mapped[str] = mapped_column(Text, nullable=False)
    totals_json: Mapped[str] = mapped_column(Text, nullable=False)

    # ── relationships ──
    user: Mapped["User"] = relationship(back_populates="saved_meals")

    def __repr__(self) -> str:
        return f"<SavedMeal(id={self.id}, name={self.name})>"
