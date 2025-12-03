from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from infrastructure.config.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class MessageEntity(Base):
  __tablename__ = "messages"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
  received = Column(String, nullable=False)
  chatbot = Column(String, nullable=False)
  id_user = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
  user = relationship("UserEntity", back_populates="messages")
  created_at = Column(DateTime(timezone=True), server_default=func.now())