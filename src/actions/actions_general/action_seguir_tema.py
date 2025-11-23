from rasa_sdk import Action
from rasa_sdk.events import FollowupAction
from rasa_sdk.interfaces import Tracker
from typing import Any, Text, Dict, List
import random

class ActionSeguirTema(Action):
  def name(self):
    return "action_seguir_tema"

  def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    tema = tracker.get_slot("tema_sugerido")
    if not tema:
      opciones_fallback = [
        "No estoy seguro de qué te refieres😅. ¿Podrías ser más específico?",
        "Hmm, no entiendo bien😅. ¿Podrías darme más detalles?",
        "No logro identificar eso😅. ¿Puedes reformularlo o ser más claro?"
      ]
      dispatcher.utter_message(
        json_message={
          "text": random.choice(opciones_fallback),
        }
      )
      #dispatcher.utter_message("No sé qué tema quieres 😅")
      return []
    
    acciones = {
      "experiencias": "action_experiencia_general",
      "tecnologias": "action_tecnologia_general",
      "perfil": "action_perfil_general",
    }

    accion = acciones.get(tema)
    if accion:
      return [FollowupAction(accion)]
    else:
      dispatcher.utter_message(
        json_message={
          "text": f"No tengo información sobre {tema}",
        }
      )
      return []