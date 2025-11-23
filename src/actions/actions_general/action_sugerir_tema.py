from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.interfaces import Tracker
from typing import Any, Text, Dict, List
import random

from ..constants import ICONOS_CONTENIDO

class ActionSugerirTema(Action):
  def name(self) -> Text:
    return "action_sugerir_tema"
  
  async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    respuestas = [
      {"tema": "experiencias", "text": "¿Te gustaría saber sobre mi experiencia laboral?"},
      {"tema": "tecnologias", "text": "¿Quieres ver qué tecnologías manejo?"},
      {"tema": "perfil", "text": "¿Te gustaría que te muestre mi perfil?"},
    ]

    botones = [
      {"title": f"{ICONOS_CONTENIDO['experiencia']} Experiencia", "payload": "/intencion"},
      {"title": f"{ICONOS_CONTENIDO['tecnologia']} Tenologias", "payload": "/intencion"},
      {"title": f"{ICONOS_CONTENIDO['programador']}", "payload": "/itencion"},
    ]

    respuesta_elegida = random.choice(respuestas)

    dispatcher.utter_message(
      json_message={
        "text": respuesta_elegida['text'],
        "buttons": botones,
      }
    )

    return [SlotSet("tema_sugerido", respuesta_elegida['tema'])]
