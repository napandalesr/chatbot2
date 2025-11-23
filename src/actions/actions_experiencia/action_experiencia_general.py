from rasa_sdk import Action 
from rasa_sdk.interfaces import Tracker
from typing import Any, Text, Dict, List
import random

from ..data import EMPRESAS
from ..constants import ICONOS_CONTENIDO

class ActionExperienciaGeneral(Action):
  def name(self) -> Text:
    return "action_experiencia_general"
  
  async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    introducciones = [
      f"Con gusto. Te comparto un resumen de mi trayectoria prefesional {ICONOS_CONTENIDO['experiencia']}",
      f"Claro. Permíteme presentarte mi experiencia laboral {ICONOS_CONTENIDO['proyecto']}",
      f"Con gusto. Te cuento mi carrera profesional {ICONOS_CONTENIDO['metricas']}",
      f"Perfecto. Aquí tienes un resumen de mi experiencia {ICONOS_CONTENIDO['programador']}",
      f"Por supuesto. Te comparto mi trayectoria professional {ICONOS_CONTENIDO['habilidad']}"
    ]

    introduction = random.choice(introducciones)
    lines = []
        
    # Ordenar empresas por periodo (simplificado - se asume orden correcto en el dict)
    for empresa_key, info in EMPRESAS.items():
        nombre = info.get('display_name', empresa_key)
        periodo = info.get('periodo', '')
        cargo = info.get('cargo', '')
        tiempo = info.get('tiempo', '')
        
        lines.append(f"**{nombre}**: {periodo} ({tiempo}) - {cargo}")

    dispatcher.utter_message(
      json_message = {
        "text": introduction,
        "title": f"**{ICONOS_CONTENIDO['calendario']} TIMELINE PROFESIONAL**",
        "list": lines
      }
    )

    return []