import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text, DateTime, Float, Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    end_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    # ── relationships ──
    user: Mapped["User"] = relationship(back_populates="workouts")
    exercises: Mapped[list["Exercise"]] = relationship(
        back_populates="workout", cascade="all, delete-orphan", order_by="Exercise.order_index"
    )

    def __repr__(self) -> str:
        return f"<Workout(id={self.id}, user_id={self.user_id})>"


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    workout_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    exercise_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    # ── relationships ──
    workout: Mapped["Workout"] = relationship(back_populates="exercises")
    sets: Mapped[list["ExerciseSet"]] = relationship(
        back_populates="exercise", cascade="all, delete-orphan", order_by="ExerciseSet.order_index"
    )

    def __repr__(self) -> str:
        return f"<Exercise(id={self.id}, name={self.name})>"


class ExerciseSet(Base):
    __tablename__ = "sets"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    exercise_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False, index=True
    )
    reps: Mapped[int | None] = mapped_column(Integer, nullable=True)
    weight: Mapped[float | None] = mapped_column(Float, nullable=True)
    duration: Mapped[float | None] = mapped_column(Float, nullable=True)
    completed: Mapped[bool] = mapped_column(default=False, server_default="false")
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    # ── relationships ──
    exercise: Mapped["Exercise"] = relationship(back_populates="sets")

    def __repr__(self) -> str:
        return f"<ExerciseSet(id={self.id}, reps={self.reps}, weight={self.weight})>"
