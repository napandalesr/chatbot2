from rasa_sdk import Action
from rasa_sdk.interfaces import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List

from ..data import EMPRESAS

class ActionLogrosEmpresaEspecifica(Action):
    def name(self) -> Text:
      return "action_logros_empresa_especifica"

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

      logros = empresa_info.get("logros", {})
      
      # Manejar diferentes tipos de estructura de logros
      if not logros or (isinstance(logros, list) and len(logros) == 0):
        # Respuesta para empresas sin logros específicos
        dispatcher.utter_message(
          json_message={
            "text": f"En {empresa_info['display_name']} como {empresa_info['cargo']} durante {empresa_info['tiempo']} ({empresa_info['periodo']}). {empresa_info['descripcion']}",
          }
        )
        return [SlotSet("empresa", None)]

      # Si logros es una lista (estructura antigua), usar el primer logro
      if isinstance(logros, list):
        # Para empresas que todavía tienen logros como lista de strings
        logros_str = ", ".join(logros)
        dispatcher.utter_message(
          json_message={
            "text": f"En {empresa_info['display_name']} como {empresa_info['cargo']} logré: {logros_str}",
          }
        )
        return [SlotSet("empresa", None)]

      # Si logros es un diccionario (nueva estructura), usar el formato solicitado
      respuesta, lines = self._construir_respuesta_formato_especifico(empresa_info)
      
      dispatcher.utter_message(
        json_message={
          "text": respuesta,
          "list": lines,
        }
      )
      return [SlotSet("empresa", None)]

    def _construir_respuesta_formato_especifico(self, empresa_info: Dict) -> Text:
      """Construye la respuesta con el formato exacto solicitado"""
      logros = empresa_info["logros"]
      
      respuesta = f"En {empresa_info['display_name']} como {empresa_info['cargo']} tuve el reto de **{logros['titulo']}**:\n\n"
      
      lines = []
      lines.append(f"**Descripción:** {logros['descripcion']}\n\n")
      
      if logros.get('contexto'):
        lines.append(f"**Contexto del proyecto:** {logros['contexto']}\n\n")
      
      if logros.get('metricas_impacto'):
        lines.append("**Métricas de impacto alcanzadas:**\n")
        for metrica in logros['metricas_impacto']:
          lines.append(f"• {metrica}\n")
        lines.append("\n")
      
      if logros.get('tecnologias_involucradas'):
        lines.append(f"**Tecnologías utilizadas:** {', '.join(logros['tecnologias_involucradas'])}")
      
      return respuesta, lines