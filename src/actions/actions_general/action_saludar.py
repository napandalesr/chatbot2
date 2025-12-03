from rasa_sdk import Action
from rasa_sdk.interfaces import Tracker
from typing import Any, Text, Dict, List
import random

from ..constants import ICONOS_CONTENIDO
from ..db import get_user, create_conversation

class ActionSaludo(Action):
  def name(self) -> Text:
    return "action_saludar"
  
  async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    sender_id = tracker.sender_id

    response = get_user(sender_id)
    latest_message = tracker.latest_message

    print(f"latest_message, {latest_message['text']}")

    user = response['user']
    
    respuestas = [
      f"Hola {user[1]}, {ICONOS_CONTENIDO['saludo']} soy Neider",
      f"Un gusto saludarte {ICONOS_CONTENIDO['feliz']}",
      f"Hola {user[1]}, espero te encuentres bien"
    ]

    respuestas_tecnicas = [
      f"Saludos {ICONOS_CONTENIDO['saludo']}. Soy ingeniero de sistemas",
      f"Hola {user[1]}, Llevo más de 6 años transformando ideas en codigo",
      f"Bienvenido {ICONOS_CONTENIDO['feliz']}. Soy Neider ingeniero desarrollador con amplia experienca en Javascript/Typescript"
    ]

    respuesta_elegida = random.choice(respuestas + respuestas_tecnicas)

    create_conversation(sender_id, latest_message['text'], respuesta_elegida)

    dispatcher.utter_message(
      json_message={
        "text": respuesta_elegida,
      }
    )
    return []
