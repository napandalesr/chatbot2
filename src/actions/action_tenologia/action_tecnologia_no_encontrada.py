from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import random

class ActionTecnologiaNoEncontrada(Action):
    def name(self) -> Text:
        return "action_tecnologia_no_encontrada"
    
    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        tecnologia = tracker.get_slot("tecnologia_no_encontrada")
        
        # Capitalizar para mostrar
        if tecnologia:
            tecnologia_display = tecnologia.capitalize()
        else:
            tecnologia_display = "esta tecnología"
        
        # Opciones de respuesta
        respuestas = [
            f"😅 No tengo experiencia profesional con {tecnologia_display} en mi historial laboral. **Tengo experiencia sólida con React/Next.js, Node.js/NestJS y otras tecnologías modernas**. ¿Te gustaría conocer mis habilidades en alguna de estas?",
            f"🤔 {tecnologia_display} no forma parte de mi stack actual. **Sin embargo, domino React/Next.js para frontend y Node.js/NestJS para backend**. ¿Quieres que te cuente sobre alguna en particular?",
            f"📚 Mi experiencia no incluye {tecnologia_display}, pero **tengo conocimientos avanzados en JavaScript/TypeScript, React/Next.js y Node.js/NestJS**. ¿Te interesa saber más sobre estas tecnologías?",
            f"💡 Aunque no he trabajado con {tecnologia_display}, **tengo habilidades sólidas en desarrollo full stack con React, TypeScript, Node.js y Docker**. ¿Quieres que te detalle mi experiencia con alguna de estas?"
        ]
        
        # Botones de sugerencia
        sugerencias = [
            {"title": "👍 Sí, cuéntame sobre React", "payload": "/pregunta_tecnologia_especifica{\"tecnologia\":\"react\"}"},
            {"title": "🤝 Sí, cuéntame sobre Next.js", "payload": "/pregunta_tecnologia_especifica{\"tecnologia\":\"nextjs\"}"},
            {"title": "🚀 Sí, cuéntame sobre Node.js", "payload": "/pregunta_tecnologia_especifica{\"tecnologia\":\"node_js\"}"},
            {"title": "💼 Sí, cuéntame sobre TypeScript", "payload": "/pregunta_tecnologia_especifica{\"tecnologia\":\"typescript\"}"},
            {"title": "📊 Ver todas mis tecnologías", "payload": "/pregunta_tecnologia_general"}
        ]
        
        respuesta = random.choice(respuestas)
        
        # Enviar mensaje con botones
        dispatcher.utter_message(
            json_message={
                "text": respuesta,
            }
        )
        
        # Establecer tema_sugerido para action_seguir_tema
        return [
            SlotSet("tema_sugerido", "tecnologias"),
            SlotSet("tecnologia_no_encontrada", None),
            SlotSet("fallback_triggered", False)
        ]