from pydantic import BaseModel

class ConversationDto(BaseModel):
  received: str
  id_user: str