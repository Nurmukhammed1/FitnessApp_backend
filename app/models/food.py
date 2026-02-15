import uuid
from datetime import datetime

from sqlalchemy import String, Float, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Food(Base):
    __tablename__ = "foods"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name_en: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name_ru: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    calories: Mapped[float] = mapped_column(Float, nullable=False)
    protein: Mapped[float] = mapped_column(Float, default=0)
    carbs: Mapped[float] = mapped_column(Float, default=0)
    fats: Mapped[float] = mapped_column(Float, default=0)
    serving_size: Mapped[float] = mapped_column(Float, default=100)
    serving_unit: Mapped[str] = mapped_column(String(20), default="g", server_default="g")
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_custom: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")

    def __repr__(self) -> str:
        return f"<Food(id={self.id}, name_en={self.name_en})>"
