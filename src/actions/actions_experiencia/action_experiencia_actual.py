from typing import Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List

from ..data import EMPRESAS

class ActionExperienciaActual(Action):
    def name(self) -> Text:
      return "action_experiencia_actual"

    def run(
      self,
      dispatcher: CollectingDispatcher,
      tracker: Tracker,
      domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
      experiencia_actual = list(EMPRESAS.values())[-1]
      empresa_nombre = list(EMPRESAS.keys())[-1]
      
      mensaje = (
        f"Actualmente trabajo en **{experiencia_actual['display_name']}** "
        f"como **{experiencia_actual['cargo']}**.\n\n"
        f"📅 **Tiempo:** {experiencia_actual['tiempo']} ({experiencia_actual['periodo']})\n"
        f"📝 **Descripción:** {experiencia_actual['descripcion']}\n\n"
        f"🛠 **Tecnologías principales:** {', '.join(experiencia_actual['tecnologias'][:8])}\n\n"
      #  f"🏆 **Logros destacados:**\n"
      )
      
      #for logro in experiencia_actual['logros']:
      #  mensaje += f"   • {logro}\n"
      
      mensaje += f"\n¿Te gustaría saber más sobre mi experiencia en {experiencia_actual['display_name']} o en otras empresas donde he trabajado?"
      
      dispatcher.utter_message(text=mensaje)
      return []