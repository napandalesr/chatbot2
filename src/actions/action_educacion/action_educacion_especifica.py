from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.interfaces import Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import random

from ..data import EDUCACION
from ..constants import ICONOS_CONTENIDO

class ActionEducacionEspecifica(Action):
    def name(self) -> Text:
        return "action_educacion_especifica"
    
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        institucion = tracker.get_slot("institucion")
        
        if not institucion:
            dispatcher.utter_message(
                json_message={
                    "text": "No pude identificar la institución educativa. ¿Podrías especificar cuál te interesa?",
                }
            )
            return []
        
        # Buscar la institución en la base de conocimiento
        educacion_info = self._buscar_educacion_por_institucion(institucion)
        
        if not educacion_info:
            # Si no se encuentra, mostrar opciones disponibles
            return self._respuesta_educacion_no_encontrada(dispatcher, institucion)
        
        # Construir los elementos del mensaje
        introducciones, lines, footer = self._construir_elementos_respuesta_especifica(educacion_info)
        
        # Enviar mensaje con formato JSON
        dispatcher.utter_message(
            json_message={
                "text": random.choice(introducciones),
                "title": f"**{ICONOS_CONTENIDO.get('educacion', '🎓')} {educacion_info['nombre'].upper()}**",
                "list": lines,
                "footer": footer
            }
        )
        
        return [SlotSet("institucion", educacion_info["nombre"])]
    
    def _buscar_educacion_por_institucion(self, nombre_institucion: str) -> Dict:
        """Busca educación por nombre de institución"""
        for educacion in EDUCACION:
            if nombre_institucion.lower() in educacion["nombre"].lower():
                return educacion
        return None
    
    def _construir_elementos_respuesta_especifica(self, info: Dict) -> tuple:
        """Construye los elementos para la respuesta específica"""
        
        # Introducciones aleatorias
        introducciones = [
            f"Esta es mi formación en {info['nombre']}:",
            f"Estudié en {info['nombre']} donde:",
            f"Mi paso por {info['nombre']} incluyó:",
            f"En {info['nombre']} completé:"
        ]
        
        # Líneas de información
        lines = [
            f"**Carrera:** {info['grado']}",
            f"**Institución:** {info['nombre']}",
            f"**Periodo:** {info['fecha']}"
        ]
        
        # Información adicional si existe
        if 'estado' in info:
            lines.append(f"**Estado:** {info['estado']}")
        if 'titulo' in info:
            lines.append(f"**Título obtenido:** {info['titulo']}")
        if 'promedio' in info:
            lines.append(f"**Promedio:** {info['promedio']}")
        if 'mencion' in info:
            lines.append(f"**Mención:** {info['mencion']}")
        if 'proyecto' in info:
            lines.append(f"**Proyecto destacado:** {info['proyecto']}")
        
        # Footer con frase contextual
        frases_footer = [
            "Esta formación ha sido fundamental para mi desarrollo profesional",
            "Los conocimientos adquiridos aquí son la base de mi carrera tecnológica",
            "Esta experiencia educativa me preparó para los desafíos del desarrollo de software",
            "La universidad me dio las herramientas para especializarme en ingeniería de software"
        ]
        
        footer = f"{random.choice(frases_footer)}\n ¿Te interesa conocer otra parte de mi formación?"
        
        return introducciones, lines, footer
    
    def _respuesta_educacion_no_encontrada(self, dispatcher: CollectingDispatcher, institucion: str) -> List[Dict[Text, Any]]:
        """Responde cuando no se encuentra la institución educativa"""
        
        instituciones_disponibles = [edu["nombre"] for edu in EDUCACION]
        
        dispatcher.utter_message(
            json_message={
                "text": f"No tengo información sobre {institucion} en mi formación.",
                "title": "**🎓 INSTITUCIONES DISPONIBLES**",
                "list": [f"• {nombre}" for nombre in instituciones_disponibles],
                "footer": "Puedes preguntarme por cualquiera de estas instituciones"
            }
        )
        
        return [SlotSet("institucion", None)]