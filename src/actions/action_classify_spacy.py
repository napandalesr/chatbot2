from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction, SlotSet
import spacy
from pathlib import Path

# Importar bases de conocimiento
from .data import TECNOLOGIAS, EMPRESAS, IDIOMAS

# Cargar modelo spaCy
MODEL_PATH = Path(__file__).parent.parent / "nlp" / "model-best"
nlp = spacy.load(MODEL_PATH)

class ActionClassifySpacy(Action):
    def name(self) -> Text:
        return "action_classify_spacy"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get("text", "").strip()
        intent_name = tracker.latest_message.get("intent", {}).get("name", "")
        entities = tracker.latest_message.get("entities", [])
        
        if not user_message:
            dispatcher.utter_message(text="No entendí tu mensaje.")
            return [SlotSet("fallback_triggered", True)]

        mensaje_lower = user_message.lower().strip()
        
        # 0️⃣ Manejar "todas" según contexto previo
        if mensaje_lower in ["todas", "todas las tecnologías", "todas las tecnologias"]:
            tema_sugerido = tracker.get_slot("tema_sugerido")
            
            if tema_sugerido == "tecnologias":
                return [
                    SlotSet("fallback_triggered", False),
                    SlotSet("tecnologia", "todas"),
                    FollowupAction("action_tecnologia_general")
                ]
            else:
                dispatcher.utter_message(
                    json_message={
                        "text": "¿A qué te refieres con 'todas'? ¿Todas las tecnologías, todas las experiencias laborales, o todos los idiomas?",
                        "suggestions": [
                            "Todas las tecnologías",
                            "Todas las experiencias",
                            "Todos los idiomas",
                            "Toda mi educación"
                        ]
                    }
                )
                return [SlotSet("fallback_triggered", False)]
        
        # 1️⃣ Usar entidades extraídas por Rasa
        tecnologia_entidad = self._obtener_entidad_tecnologia(entities)
        if tecnologia_entidad:
            return [
                SlotSet("tecnologia", tecnologia_entidad),
                SlotSet("fallback_triggered", False),
                FollowupAction("action_tecnologia_especifica")
            ]
        
        empresa_entidad = self._obtener_entidad_empresa(entities)
        if empresa_entidad:
            return [
                SlotSet("empresa", empresa_entidad),
                SlotSet("fallback_triggered", False),
                FollowupAction("action_experiencia_especifica")
            ]

        idioma_entidad = self._obtener_entidad_idioma(entities)
        if idioma_entidad:
            return [
                SlotSet("idioma", idioma_entidad),
                SlotSet("fallback_triggered", False),
                FollowupAction("action_idioma_especifico")
            ]

        # 2️⃣ Buscar en bases de conocimiento
        tecnologia = self._buscar_en_tecnologias(mensaje_lower)
        if tecnologia:
            return [
                SlotSet("tecnologia", tecnologia),
                SlotSet("fallback_triggered", False),
                FollowupAction("action_tecnologia_especifica")
            ]
        
        empresa = self._buscar_en_empresas(mensaje_lower)
        if empresa:
            return [
                SlotSet("empresa", empresa),
                SlotSet("fallback_triggered", False),
                FollowupAction("action_experiencia_especifica")
            ]

        idioma = self._buscar_en_idiomas(mensaje_lower)
        if idioma:
            return [
                SlotSet("idioma", idioma),
                SlotSet("fallback_triggered", False),
                FollowupAction("action_idioma_especifico")
            ]

        # 3️⃣ Palabras generales desde sinónimos
        categoria_general = self._obtener_categoria_general(entities)
        if categoria_general:
            return self._manejar_categoria_general(categoria_general)

        # 4️⃣ Último recurso: spaCy
        return await self._clasificar_con_spacy(dispatcher, user_message, intent_name)

    # =====================
    # Métodos auxiliares
    # =====================
    def _obtener_entidad_tecnologia(self, entities: List[Dict]) -> str:
        for entity in entities:
            if entity.get("entity") == "tecnologia":
                return entity.get("value", "").lower()
        return None

    def _obtener_entidad_empresa(self, entities: List[Dict]) -> str:
        for entity in entities:
            if entity.get("entity") == "empresa":
                valor = entity.get("value", "").lower()
                if valor in EMPRESAS:
                    return valor
                for emp_key, emp_info in EMPRESAS.items():
                    if emp_info["display_name"].lower() == valor:
                        return emp_key
                return valor
        return None

    def _obtener_entidad_idioma(self, entities: List[Dict]) -> str:
        for entity in entities:
            if entity.get("entity") == "idioma":
                return entity.get("value", "").lower()
        return None

    def _obtener_categoria_general(self, entities: List[Dict]) -> str:
        """Obtiene categoría general desde entidades de sinónimos"""
        categorias_map = {
            "tecnologia_general": "tecnologias",
            "experiencia_general": "experiencias",
            "idioma_general": "idiomas",
            "educacion_general": "educacion"
        }
        
        for entity in entities:
            valor = entity.get("value", "").lower()
            for categoria_sinonimo, categoria in categorias_map.items():
                if valor == categoria_sinonimo.replace("_", " "):
                    return categoria
        return None

    def _buscar_en_tecnologias(self, mensaje: str) -> str:
        for tech_key, tech_info in TECNOLOGIAS.items():
            if tech_key == mensaje:
                return tech_key
            if tech_info["display_name"].lower() == mensaje:
                return tech_key
        return None

    def _buscar_en_empresas(self, mensaje: str) -> str:
        for emp_key, emp_info in EMPRESAS.items():
            if emp_key == mensaje:
                return emp_key
            if emp_info["display_name"].lower() == mensaje:
                return emp_key
        return None

    def _buscar_en_idiomas(self, mensaje: str) -> str:
        if "idiomas" in IDIOMAS and isinstance(IDIOMAS["idiomas"], list):
            for idioma_info in IDIOMAS["idiomas"]:
                if idioma_info.get("nombre", "").lower() == mensaje:
                    return idioma_info.get("nombre", "").lower()
        return None

    def _manejar_categoria_general(self, categoria: str) -> List[Dict[Text, Any]]:
        """Maneja categorías generales identificadas"""
        followup_map = {
            "tecnologias": "action_tecnologia_general",
            "experiencias": "action_experiencia_general",
            "idiomas": "action_idioma_general",
            "educacion": "action_educacion_general"
        }
        
        if categoria in followup_map:
            return [
                SlotSet("tema_sugerido", categoria),
                SlotSet("fallback_triggered", False),
                FollowupAction(followup_map[categoria])
            ]
        return []

    async def _clasificar_con_spacy(self, dispatcher, user_message: str, intent_name: str):
        doc = nlp(user_message)
        if "textcat" not in nlp.pipe_names:
            dispatcher.utter_message(text="No sé a qué te refieres.")
            return [SlotSet("fallback_triggered", True)]

        scores = doc.cats
        label = max(scores, key=scores.get)
        confidence = scores[label]

        if confidence < 0.5:
            dispatcher.utter_message(text="No entiendo bien tu mensaje. ¿Podrías aclararlo?")
            return [SlotSet("fallback_triggered", True)]

        followup_actions = {
            "tecnologia_especifica": "action_tecnologia_especifica",
            "tecnologia_general": "action_tecnologia_general", 
            "empresa_especifica": "action_experiencia_especifica",
            "empresa_general": "action_experiencia_general",
            "idioma_especifico": "action_idioma_especifico",
            "idioma_general": "action_idioma_general"
        }

        if label in followup_actions:
            return [
                SlotSet("fallback_triggered", False),
                FollowupAction(followup_actions[label])
            ]
        dispatcher.utter_message(text="No logro identificar a qué te refieres.")
        return [SlotSet("fallback_triggered", True)]