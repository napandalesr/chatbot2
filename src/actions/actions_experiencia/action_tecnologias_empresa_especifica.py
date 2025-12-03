from rasa_sdk import Action 
from rasa_sdk.interfaces import Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import random

from ..data import EMPRESAS
from ..constants import ICONOS_CONTENIDO

class ActionTecnologiasEmpresaEspecifica(Action):
  def name(self) -> Text:
    return "action_tecnologias_empresa_especifica"

  def run(self, dispatcher: CollectingDispatcher,
          tracker: Tracker,
          domain: Dict[Text, Any]) -> List[Dict]:
    empresa = tracker.get_slot("empresa")
    empresa_normalizada = empresa.lower().replace(" ", "_")
    empresa_info = EMPRESAS.get(empresa_normalizada)
    
    if not empresa_info:
      dispatcher.utter_message(
        json_message={
          "text": f"Lo siento, no tengo información específica sobre mi experiencia en {empresa}.",
        }
      )
      return [SlotSet("empresa", None)]

    tecnologias = empresa_info.get("tecnologias", [])
    if not tecnologias:
      dispatcher.utter_message(
        json_message={
          "text": f"Lo siento, no tengo información sobre las tecnologías utilizadas en {empresa}.",
        }
      )
      return [SlotSet("empresa", None)]

    dispatcher.utter_message(
      json_message={
        "text": f"En {empresa_info['display_name']} como {empresa_info['cargo']} trabajé con las siguientes tecnologías:",
        "footer": f"- {', '.join(tecnologias)}",
      }
    )
    return [SlotSet("empresa", empresa_normalizada)]