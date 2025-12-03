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
        
        # Caso especial: "todas"
        if tecnologia.lower() == "todas":
            return [FollowupAction("action_tecnologia_general")]
        
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
        
        # SI NO SE ENCUENTRA LA TECNOLOGÍA (caso Python, Vue, etc.)
        if not tecnologia_info:
            if tecnologia:
                tecnologia_display = tecnologia.capitalize()
            else:
                tecnologia_display = "esta tecnología"
            
            respuestas = [
                f"😅 No tengo experiencia profesional con **{tecnologia_display}** en mi historial laboral. **Tengo experiencia sólida con React/Next.js, Node.js/NestJS y otras tecnologías modernas**. ¿Te gustaría conocer mis habilidades en alguna de estas?",
                f"🤔 **{tecnologia_display}** no forma parte de mi stack actual. **Sin embargo, domino React/Next.js para frontend y Node.js/NestJS para backend**. ¿Quieres que te cuente sobre alguna en particular?",
            ]
            
            respuesta = random.choice(respuestas)
            
            dispatcher.utter_message(
                json_message={
                    "text": respuesta,
                    "buttons": [
                        {"title": "👍 Sí, cuéntame sobre React", "payload": "/pregunta_tecnologia_especifica{\"tecnologia\":\"react\"}"},
                        {"title": "🤝 Sí, cuéntame sobre Next.js", "payload": "/pregunta_tecnologia_especifica{\"tecnologia\":\"nextjs\"}"},
                        {"title": "🚀 Sí, cuéntame sobre Node.js", "payload": "/pregunta_tecnologia_especifica{\"tecnologia\":\"node_js\"}"},
                        {"title": "📊 Ver todas mis tecnologías", "payload": "/pregunta_tecnologia_general"}
                    ]
                }
            )
            
            # Establecer tema_sugerido para contexto futuro
            return [
                SlotSet("tema_sugerido", "tecnologias"),
                SlotSet("tecnologia", None),
                SlotSet("fallback_triggered", False)
            ]
        
        # SI SE ENCUENTRA LA TECNOLOGÍA
        introducciones, lines, footer = self._construir_elementos_respuesta(tecnologia_info, tecnologia_normalizada)
        
        dispatcher.utter_message(
            json_message={
                "text": random.choice(introducciones),
                "list": lines,
                "footer": footer
            }
        )
        
        return [SlotSet("tecnologia", tecnologia_normalizada)]
    
    def _construir_elementos_respuesta(self, info: Dict, tech_key: str) -> tuple:
        """Construye los elementos para la respuesta estructurada"""
        introducciones = [
            f"Esta es mi experiencia con {ICONOS_CONTENIDO.get('tecnologia', '💻')} **{info['display_name']}**:",
            f"Estos son mis conocimientos en {ICONOS_CONTENIDO.get('tecnologia', '💻')} **{info['display_name']}**:",
        ]
        
        lines = [
            f"**Nivel:** {info['nivel']}",
            f"**Experiencia:** {info['experiencia']}",
        ]
        
        if 'años_experiencia' in info:
            lines.append(f"**Años de experiencia:** {info['años_experiencia']}")
        
        if 'detalles' in info:
            lines.append(f"**Habilidades específicas:** {info['detalles']}")
        
        frases = [
            "¡Estoy listo para aplicar estos conocimientos en nuevos desafíos!",
            "Me encanta trabajar con esta tecnología y seguir aprendiendo.",
        ]
        
        footer = f"{random.choice(frases)}\n ¿Te gustaría conocer mi experiencia con otra tecnología?"
        
        return introducciones, lines, footer