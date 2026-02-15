from pydantic import BaseModel, ConfigDict


class FoodRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    name_en: str
    name_ru: str | None = None
    calories: float
    protein: float
    carbs: float
    fats: float
    serving_size: float
    serving_unit: str
    source: str | None = None
    is_custom: bool
