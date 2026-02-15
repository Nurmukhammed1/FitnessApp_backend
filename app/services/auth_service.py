from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.models.nutrition import NutritionGoal
from app.schemas.user import UserCreate, LoginRequest, UserRead, AuthResponse
from fastapi import HTTPException, status


async def register(data: UserCreate, db: AsyncSession) -> AuthResponse:
    # Check duplicates
    existing = await db.execute(
        select(User).where((User.email == data.email) | (User.username == data.username))
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or username already registered")

    user = User(
        email=data.email,
        username=data.username,
        password_hash=hash_password(data.password),
    )
    db.add(user)
    await db.flush()

    # Create default nutrition goals
    goal = NutritionGoal(
        user_id=user.id,
        daily_calories=2000,
        protein_goal=150,
        carbs_goal=250,
        fats_goal=65,
        water_goal=2000,
    )
    db.add(goal)
    await db.flush()

    token = create_access_token({"sub": user.id})
    return AuthResponse(token=token, user=UserRead.model_validate(user))


async def login(data: LoginRequest, db: AsyncSession) -> AuthResponse:
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token({"sub": user.id})
    return AuthResponse(token=token, user=UserRead.model_validate(user))


async def get_me(user: User) -> UserRead:
    return UserRead.model_validate(user)
