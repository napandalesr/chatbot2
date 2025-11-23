from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.config.db import SessionLocal
from domain.entities.user import UserEntity
from application.dto.user_dto import UserDto
from sqlalchemy import select

async def get_db():
  async with SessionLocal() as session:
    yield session

class UserController:
  router = APIRouter(prefix="/users", tags=["Users"])
    
  @staticmethod
  @router.post("/")
  async def create_user(user: UserDto, db: AsyncSession = Depends(get_db)):
    new_user = UserEntity(name= user.name, email= user.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

  @staticmethod
  @router.get("/")
  async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserEntity))
    users = result.scalars().all()
    return users

  @staticmethod
  @router.get("/by-email/")
  async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserEntity).where(UserEntity.email == email))
    user = result.scalar_one_or_none()
    if not user:
      raise HTTPException(status_code=404, detail="User not found")
    return user

user_controller = UserController()