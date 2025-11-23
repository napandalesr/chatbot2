from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.interfaces import Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import random

# Importar base de conocimiento desde data.py
from ..data import TECNOLOGIAS
from ..constants import ICONOS_CONTENIDO

class ActionTecnologiaEspecifica(Action):
    def name(self) -> Text:
        return "action_tecnologia_especifica"
    
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tecnologia = tracker.get_slot("tecnologia")
        
        if not tecnologia:
            dispatcher.utter_message(
                json_message={
                    "text": "No pude identificar la tecnología sobre la que quieres información. ¿Podrías especificar cuál tecnología te interesa?",
                }
            )
            return []
        
        # Normalizar el nombre de la tecnología
        tecnologia_normalizada = tecnologia.lower().replace(" ", "_").replace(".", "_")
        
        # Buscar la tecnología en la base de conocimiento
        tecnologia_info = TECNOLOGIAS.get(tecnologia_normalizada)
        
        if not tecnologia_info:
            # Intentar búsqueda flexible por display_name
            for key, value in TECNOLOGIAS.items():
                if tecnologia.lower() in value["display_name"].lower():
                    tecnologia_info = value
                    tecnologia_normalizada = key
                    break
        
        if not tecnologia_info:
            dispatcher.utter_message(
                json_message={
                    "text": f"Lo siento, no tengo información específica sobre {tecnologia}.",
                }
            )
            return [SlotSet("tecnologia", None)]
        
        # Construir los elementos del mensaje
        introducciones, lines, footer = self._construir_elementos_respuesta(tecnologia_info, tecnologia_normalizada)
        
        # Enviar mensaje con formato JSON
        dispatcher.utter_message(
            json_message={
                "text": random.choice(introducciones),
                "title": f"**{ICONOS_CONTENIDO.get('tecnologia', '💻')} {tecnologia_info['display_name'].upper()}**",
                "list": lines,
                "footer": footer
            }
        )
        
        return [SlotSet("tecnologia", tecnologia_normalizada)]
    
    def _construir_elementos_respuesta(self, info: Dict, tech_key: str) -> tuple:
        """Construye los elementos para la respuesta estructurada"""
        
        # Introducciones aleatorias
        introducciones = [
            f"Esta es mi experiencia con {info['display_name']}:",
            f"Estos son mis conocimientos en {info['display_name']}:",
            f"Tengo la siguiente experiencia en {info['display_name']}:",
            f"Mis habilidades en {info['display_name']} incluyen:"
        ]
        
        # Líneas de información (list items)
        lines = [
            f"**Nivel:** {info['nivel']}",
            f"**Experiencia:** {info['experiencia']}",
            f"**Categoría:** {info.get('categoria', 'No especificada').title()}"
        ]
        
        # Años de experiencia (si existe)
        if 'años_experiencia' in info:
            lines.append(f"**Años de experiencia:** {info['años_experiencia']}")
        
        # Detalles técnicos
        if 'detalles' in info:
            lines.append(f"**Habilidades específicas:** {info['detalles']}")
        
        # Footer con frase motivacional
        frases = [
            "¡Estoy listo para aplicar estos conocimientos en nuevos desafíos!",
            "Me encanta trabajar con esta tecnología y seguir aprendiendo.",
            "He acumulado experiencia sólida que me permite resolver problemas complejos.",
            "Siempre busco optimizar y mejorar mis habilidades con esta tecnología.",
            "Esta tecnología es una de mis especialidades y disfruto trabajando con ella."
        ]
        
        footer = f"{random.choice(frases)}\n ¿Te gustaría conocer mi experiencia con otra tecnología?"
        
        return introducciones, lines, footer