from rasa_sdk import Action 
from rasa_sdk.interfaces import Tracker
from typing import Any, Text, Dict, List
import random

from ..constants import ICONOS_CONTENIDO
from ..data import TECNOLOGIAS

class ActionTecnologiaGeneral(Action):
  def name(self) -> Text:
    return "action_tecnologia_general"
  
  async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    introducciones = [
      f"¡Te doy la bienvenida a mi panorama tecnológico completo! {ICONOS_CONTENIDO['proyecto']}",
      f"Con gusto! Te presento mi stack tecnológico general {ICONOS_CONTENIDO['computador']}",
      f"¡Excelente! Permíteme mostrarte mis habilidades tecnológicas organizadas por categorías {ICONOS_CONTENIDO['tecnologia']}"
    ]

    introduction = random.choice(introducciones)

    lines = self._agrupar_tecnologias_por_categoria(TECNOLOGIAS)

    dispatcher.utter_message(
      json_message = {
        "text": introduction,
        "title": f"**{ICONOS_CONTENIDO['programador']} TECNOLOGIAS**",
        "list": lines,
        "footer":  "¿Te gustaría profundizar en alguna tecnología en particular?"
      }
    )

    return []
  
  def _agrupar_tecnologias_por_categoria(self, tecnologias: Dict) -> Dict[Text, List]:
    data = []
    
    for key, info in tecnologias.items():
      data.append(f"En **{info.get('display_name', key)}**: tengo un nivel {info.get('nivel')} y {info.get('experiencia')} de experiencia")
    
    return data