from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from infrastructure.config.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UserEntity(Base):
  __tablename__ = "users"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
  name = Column(String, nullable=False)
  email = Column(String, unique=True, index=True)
  messages = relationship("MessageEntity", back_populates="user", cascade="all, delete-orphan")
  created_at = Column(DateTime, default=datetime.utcnow, nullable=False)