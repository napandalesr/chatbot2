from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.interfaces import Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import random

from ..data import EDUCACION_INFORMAL

class ActionCursosExtracurriculares(Action):
  def name(self) -> Text:
    return "action_cursos_extracurriculares"

  def run(self, dispatcher: CollectingDispatcher,  tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
    if not EDUCACION_INFORMAL:
      dispatcher.utter_message(text="Actualmente no tengo cursos extracurriculares registrados en mi base de datos.")
      return []
        
    # Mostrar lista de todos los cursos
    mensaje = "He realizado los siguientes cursos extracurriculares:\n\n"
        
    for i, curso in enumerate(EDUCACION_INFORMAL, 1):
      mensaje += f"{i}. **{curso['titulo']}** - {curso['empresa_emisora']}\n"
        
    mensaje += "\n¿Te gustaría ver el certificado de alguno de estos cursos?"
        
    dispatcher.utter_message(text=mensaje)
        
    return []