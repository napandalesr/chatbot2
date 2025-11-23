from rasa_sdk import Action
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.interfaces import Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import random

# Importar base de conocimiento desde data.py
from ..data import EMPRESAS
from ..constants import ICONOS_CONTENIDO

class ActionExperienciaEspecifica(Action):
    def name(self) -> Text:
        return "action_experiencia_especifica"
    
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        empresa = tracker.get_slot("empresa")
        
        if not empresa:
          return [FollowupAction("action_classify_spacy")]
        
        # Normalizar el nombre de la empresa
        empresa_normalizada = empresa.lower().replace(" ", "_")
        
        # Buscar la empresa en la base de conocimiento
        empresa_info = EMPRESAS.get(empresa_normalizada)
        
        if not empresa_info:
            # Intentar búsqueda flexible por display_name
            for key, value in EMPRESAS.items():
                if empresa.lower() in value["display_name"].lower():
                    empresa_info = value
                    empresa_normalizada = key
                    break
        
        if not empresa_info:
            dispatcher.utter_message(
                json_message={
                    "text": f"Lo siento, no tengo información específica sobre mi experiencia en {empresa}.",
                }
            )
            return [SlotSet("empresa", None)]
        
        # Construir los elementos del mensaje
        introducciones, lines, footer = self._construir_elementos_respuesta(empresa_info, empresa_normalizada)
        
        # Enviar mensaje con formato JSON
        dispatcher.utter_message(
            json_message={
                "text": random.choice(introducciones),
                "title": f"**{ICONOS_CONTENIDO.get('programador', '💼')} EXPERIENCIA EN {empresa_info['display_name'].upper()}**",
                "list": lines,
                "footer": footer
            }
        )
        
        return [SlotSet("empresa", empresa_normalizada)]
    
    def _construir_elementos_respuesta(self, info: Dict, empresa_key: str) -> tuple:
        """Construye los elementos para la respuesta estructurada"""
        
        # Introducciones aleatorias
        introducciones = [
            f"Durante mi tiempo en {info['display_name']} tuve la oportunidad de:",
            f"Mi experiencia en {info['display_name']} incluyó:",
            f"En {info['display_name']} me desempeñé como {info['cargo']} donde:",
            f"Trabajé en {info['display_name']} desarrollando las siguientes actividades:"
        ]
        
        # Líneas de información (list items)
        lines = [
            f"**Cargo:** {info['cargo']}",
            f"**Duración:** {info['tiempo']} ({info['periodo']})",
            f"**Descripción:** {info['descripcion']}"
        ]
        
        # Tecnologías utilizadas
        if 'tecnologias' in info and info['tecnologias']:
            tecnologias_str = ", ".join(info['tecnologias'])
            lines.append(f"**Tecnologías:** {tecnologias_str}")
        
        # Logros destacados
        if 'logros' in info and info['logros']:
            for logro in info['logros']:
                lines.append(f"**Logro:** {logro}")
        
        # Footer con frase motivacional
        frases = [
            "Fue una experiencia muy enriquecedora donde pude aplicar y desarrollar mis habilidades",
            "Este rol me permitió crecer profesionalmente y enfrentar nuevos desafíos",
            "Valoro mucho la experiencia adquirida durante mi tiempo en esta empresa",
            "Tuve la oportunidad de trabajar en proyectos interesantes y aprender continuamente",
            "Esta experiencia fortaleció mis habilidades técnicas y de liderazgo"
        ]
        
        footer = f"{random.choice(frases)}\n ¿Te gustaría profundizar en alguna tecnología en particular?"
        
        return introducciones, lines, footer