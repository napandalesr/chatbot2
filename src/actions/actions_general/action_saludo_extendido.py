from rasa_sdk import Action
from rasa_sdk.interfaces import Tracker
from typing import Any, Text, Dict, List

import random

class ActionSaludoExtendido(Action):
  def name(self) -> Text:
    return "action_saludo_extendido"
  

  async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    respuestas = [
      "Bien, gracias. Estoy aquí para brindarte cualquier información sobre mi perfil profesional",
      "Excelente",
      "Muy bien"
    ]

    respuesta = random.choice(respuestas)
    dispatcher.utter_message(
      json_message={
        "text": respuesta,
      }
    )

    return []
