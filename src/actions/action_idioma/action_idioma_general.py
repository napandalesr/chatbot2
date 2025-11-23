from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.interfaces import Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import random

# Importar base de conocimiento desde data.py
from ..data import IDIOMAS
from ..constants import ICONOS_CONTENIDO

class ActionIdiomaGeneral(Action):
    def name(self) -> Text:
        return "action_idioma_general"
    
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Obtener todos los idiomas
        lista_idiomas = IDIOMAS.get("idiomas", [])
        
        if not lista_idiomas:
            dispatcher.utter_message(
                json_message={
                    "text": "No tengo información sobre mis conocimientos de idiomas en este momento.",
                }
            )
            return []
        
        # Construir los elementos del mensaje
        introducciones, lines = self._construir_elementos_respuesta_general(lista_idiomas)
        
        # Enviar mensaje con formato JSON
        dispatcher.utter_message(
            json_message={
                "text": random.choice(introducciones),
                "title": f"**{ICONOS_CONTENIDO.get('idioma', '🌍')} IDIOMAS QUE MANEJO**",
                "list": lines,
            }
        )
        
        return []
    
    def _construir_elementos_respuesta_general(self, lista_idiomas: List[Dict]) -> tuple:
        """Construye los elementos para la respuesta general"""
        
        # Introducciones aleatorias
        introducciones = [
            "Estos son los idiomas que manejo:",
            "Mis competencias lingüísticas incluyen:",
            "Puedo comunicarme en los siguientes idiomas:",
            "Estos son los idiomas en los que tengo experiencia:"
        ]
        
        # Líneas de información (list items)
        lines = []
        for idioma in lista_idiomas:
            nivel = idioma.get("nivel", "Básico")
            lines.append(f"**{idioma['nombre']}** - {nivel}")
        
        return introducciones, lines


