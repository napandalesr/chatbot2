from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.config.db import SessionLocal
from domain.entities.message import MessageEntity
from application.dto.conversation_dto import ConversationDto
from domain.entities.user import UserEntity
import os
import httpx
import uuid 
from sqlalchemy import select, func
from datetime import datetime

RASA_API = os.getenv("RASA_API_URL")

async def get_db():
  async with SessionLocal() as session:
    yield session

class ConversationController:
  router = APIRouter(prefix="/conversation", tags=["Conversations"])
    
  @staticmethod
  @router.post("")
  async def create_conversation(msg: ConversationDto, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, msg.id_user)
    payload = {
      "message": msg.received,
      "sender": msg.id_user
    }

    if user and user.name:
      payload["metadata"] = {
        "user_name": user.name
      }
    rasa_responses = await call_rasa(payload)

    if rasa_responses and len(rasa_responses) > 0:
      chatbot_response = "\n\n".join(
          item.get("text", "").strip() for item in rasa_responses if item.get("text")
      ).strip()
    else:
      chatbot_response = "Lo siento, no pude procesar tu mensaje en este momento."

    user_uuid = uuid.UUID(msg.id_user)
    new_message = MessageEntity(
      received=msg.received,
      chatbot=chatbot_response,
      id_user=user_uuid,
    )
    #db.add(new_message)
    #await db.commit()
    #await db.refresh(new_message)
    return rasa_responses
  
  @staticmethod
  @router.get("/stats")
  async def get_stats(db: AsyncSession = Depends(get_db)):
    total_messages_result = await db.execute(select(func.count(MessageEntity.id)))
    total_messages = total_messages_result.scalar()
    active_users_result= await db.execute(
      select(func.count(func.distinct(MessageEntity.id_user)))
    )

    active_users = active_users_result.scalar()

    return {
      "total_messages": total_messages,
      "active_users": active_users,
      "last_updated": datetime.now().isoformat()
    }

async def get_user_by_id(db: AsyncSession, user_id: str):
  try:
    user_uuid = uuid.UUID(user_id)
    result = await db.execute(
      select(UserEntity).where(UserEntity.id == user_uuid)
    )
    return result.scalar_one_or_none()
  except:
    return None

async def call_rasa(payload):
  try:
    async with httpx.AsyncClient(timeout=5) as client:
      response = await client.post(RASA_API, json=payload)
      # print(f"Response: {response.json()}")
      # chatbot_fastapi   | Response: [{'recipient_id': 'string', 'text': 'Hola! ¿Cómo estás?'}]
      return response.json()
  except:
    return [{"text": "Lo siento, hubo un error procesando tu mensaje."}]

conversation_controller = ConversationController()