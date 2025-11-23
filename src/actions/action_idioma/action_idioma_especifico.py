from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.interfaces import Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import random

from ..data import IDIOMAS
from ..constants import ICONOS_CONTENIDO

class ActionIdiomaEspecifico(Action):
    def name(self) -> Text:
        return "action_idioma_especifico"
    
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        idioma = tracker.get_slot("idioma")
        
        if not idioma:
          return [FollowupAction("action_classify_spacy")]
        
        # Buscar el idioma en la base de conocimiento
        idioma_info = self._buscar_idioma_por_nombre(idioma)
        
        if not idioma_info:
            # Si no se encuentra el idioma, responder negativamente pero de forma útil
            return self._respuesta_idioma_no_encontrado(dispatcher, idioma)
        
        # Construir los elementos del mensaje
        introducciones, lines, footer = self._construir_elementos_respuesta_especifica(idioma_info)
        
        # Enviar mensaje con formato JSON
        dispatcher.utter_message(
            json_message={
                "text": random.choice(introducciones),
                "title": f"**{ICONOS_CONTENIDO.get('idioma', '🌍')} {idioma_info['nombre'].upper()}**",
                "list": lines,
                "footer": footer
            }
        )
        
        return [SlotSet("idioma", idioma_info["nombre"])]
    
    def _buscar_idioma_por_nombre(self, nombre_idioma: str) -> Dict:
        """Busca un idioma por nombre en la base de conocimiento"""
        lista_idiomas = IDIOMAS.get("idiomas", [])
        
        for idioma in lista_idiomas:
            if nombre_idioma.lower() in idioma["nombre"].lower():
                return idioma
        return None
    
    def _construir_elementos_respuesta_especifica(self, info: Dict) -> tuple:
        """Construye los elementos para la respuesta específica"""
        
        # Introducciones aleatorias según el nivel
        nivel = info['nivel']
        if nivel == "Nativo":
            introducciones = [
                f"Sí, manejo {info['nombre']} a nivel nativo:",
                f"El {info['nombre']} es mi lengua materna:",
                f"Tengo dominio nativo de {info['nombre']}:"
            ]
        else:
            introducciones = [
                f"Tengo conocimientos de {info['nombre']} (nivel {nivel}):",
                f"Manejo {info['nombre']} con competencia {nivel}:",
                f"Estas son mis habilidades en {info['nombre']} (nivel {nivel}):"
            ]
        
        # Líneas de información
        lines = [
            f"**Nivel:** {nivel}"
        ]
        
        # Contexto de uso
        if 'contexto_uso' in info and info['contexto_uso']:
            lines.append("**Contextos de uso:**")
            for contexto in info['contexto_uso']:
                lines.append(f"• {contexto}")
        
        # Habilidades específicas
        if 'habilidades_especificas' in info and info['habilidades_especificas']:
            lines.append("**Habilidades:**")
            for habilidad in info['habilidades_especificas']:
                lines.append(f"• {habilidad}")
        
        # Footer según el nivel
        if nivel == "Nativo":
            frases_footer = [
                "Domino este idioma en todos los contextos profesionales y personales",
                "Tengo fluidez completa para cualquier situación comunicativa",
                "Mi dominio nativo me permite comunicarme con precisión y naturalidad"
            ]
        elif "A2" in nivel:
            frases_footer = [
                "Puedo comprender documentación técnica y comunicarme en contextos básicos",
                "Manejo lo necesario para recursos técnicos y comunicación simple",
                "Tengo competencia para lectura técnica y conversaciones básicas"
            ]
        elif "B1" in nivel or "B2" in nivel:
            frases_footer = [
                "Puedo mantener conversaciones y comprender contextos profesionales",
                "Tengo fluidez para situaciones laborales y cotidianas",
                "Manejo el idioma con confianza en entornos profesionales"
            ]
        else:
            frases_footer = [
                "Estoy desarrollando mis habilidades en este idioma",
                "Puedo comunicarme en situaciones básicas y familiares",
                "Tengo conocimientos fundamentales para contextos simples"
            ]
        
        footer = f"{random.choice(frases_footer)}\n ¿Te interesa conocer sobre otro idioma?"
        
        return introducciones, lines, footer
    
    def _respuesta_idioma_no_encontrado(self, dispatcher: CollectingDispatcher, idioma: str) -> List[Dict[Text, Any]]:
        """Responde cuando no se encuentra el idioma en la base de conocimiento"""
        
        lista_idiomas = IDIOMAS.get("idiomas", [])
        idiomas_disponibles = [idioma_info["nombre"] for idioma_info in lista_idiomas]
        
        # Usar formato JSON también para respuestas negativas
        dispatcher.utter_message(
            json_message={
                "text": f"No tengo conocimientos registrados de {idioma}.",
                "title": "**🌍 IDIOMAS DISPONIBLES**",
                "list": [f"• {nombre}" for nombre in idiomas_disponibles],
                "footer": "Puedes preguntarme por cualquiera de estos idiomas"
            }
        )
        
        return [SlotSet("idioma", None)]