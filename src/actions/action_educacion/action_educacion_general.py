from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.interfaces import Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import random

from ..data import EDUCACION
from ..constants import ICONOS_CONTENIDO

class ActionEducacionGeneral(Action):
    def name(self) -> Text:
        return "action_educacion_general"
    
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Obtener toda la educación
        lista_educacion = EDUCACION
        
        if not lista_educacion:
            dispatcher.utter_message(text="No tengo información sobre mi formación académica en este momento.")
            return []
        
        # Construir los elementos del mensaje
        introducciones, lines, footer = self._construir_elementos_respuesta_general(lista_educacion)
        
        # Enviar mensaje con formato JSON
        dispatcher.utter_message(
            json_message={
                "text": random.choice(introducciones),
                "title": f"**{ICONOS_CONTENIDO.get('educacion', '🎓')} FORMACIÓN ACADÉMICA**",
                "list": lines,
                "footer": footer
            }
        )
        
        return []
    
    def _construir_elementos_respuesta_general(self, lista_educacion: List[Dict]) -> tuple:
        """Construye los elementos para la respuesta general"""
        
        # Introducciones aleatorias
        introducciones = [
            "Esta es mi formación académica:",
            "Mi trayectoria educativa incluye:",
            "Estos son mis estudios formales:",
            "He completado la siguiente formación:"
        ]
        
        # Líneas de información (list items)
        lines = []
        for educacion in lista_educacion:
            lines.append(f"**{educacion['grado']}**")
            lines.append(f"• **Institución:** {educacion['nombre']}")
            lines.append(f"• **Periodo:** {educacion['fecha']}")
            
            # Información adicional si existe
            if 'estado' in educacion:
                lines.append(f"• **Estado:** {educacion['estado']}")
            if 'titulo' in educacion:
                lines.append(f"• **Título:** {educacion['titulo']}")
            if 'promedio' in educacion:
                lines.append(f"• **Promedio:** {educacion['promedio']}")
        
        # Footer con frase contextual
        frases_footer = [
            "Mi formación en ingeniería me ha proporcionado una base sólida para el desarrollo de software",
            "La educación universitaria me dio las herramientas fundamentales para mi carrera tecnológica",
            "Esta formación ha sido la base de mi crecimiento profesional en el desarrollo de software"
        ]
        
        footer = f"{random.choice(frases_footer)}\n ¿Te gustaría conocer más detalles?"
        
        return introducciones, lines, footer


