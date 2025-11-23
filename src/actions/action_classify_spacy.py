from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction, SlotSet
import spacy
from pathlib import Path
import re
import random

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
        
        print(f"🔍 [DEBUG] ActionClassifySpacy - Intent: '{intent_name}', Mensaje: '{user_message}'")

        if not user_message:
            dispatcher.utter_message(
                json_message={
                    "text": "No entendí tu mensaje.",
                }
            )
            return []

        # 1️⃣ Buscar en TECNOLOGIAS (búsqueda directa en el mensaje)
        tecnologia = self._buscar_en_tecnologias(user_message)
        if tecnologia:
            print(f"✅ [DEBUG] Tecnología encontrada: {tecnologia}")
            return [SlotSet("tecnologia", tecnologia), FollowupAction("action_tecnologia_especifica")]

        # 2️⃣ Buscar en EMPRESAS
        empresa = self._buscar_en_empresas(user_message)
        if empresa:
            print(f"✅ [DEBUG] Empresa encontrada: {empresa}")
            return [SlotSet("empresa", empresa), FollowupAction("action_experiencia_especifica")]

        # 3️⃣ Buscar en IDIOMAS
        idioma = self._buscar_en_idiomas(user_message)
        if idioma:
            print(f"✅ [DEBUG] Idioma encontrado: {idioma}")
            return [SlotSet("idioma", idioma), FollowupAction("action_idioma_especifico")]

        # 4️⃣ Si es palabra_suelta y no se encontró en bases, dar respuesta útil
        if intent_name == "palabra_suelta":
            return await self._manejar_palabra_suelta_no_encontrada(dispatcher, user_message)

        # 5️⃣ Solo usar spaCy como último recurso
        return await self._clasificar_con_spacy(dispatcher, user_message, intent_name)

    async def _manejar_palabra_suelta_no_encontrada(self, dispatcher: CollectingDispatcher, user_message: str) -> List[Dict[Text, Any]]:
        """Maneja palabras sueltas que no se encontraron en las bases de conocimiento"""
        sugerencias = {
            "tecnologias": ["react", "node.js", "typescript", "docker", "next.js"],
            "empresas": ["indra", "praxis", "ol software", "marabunta"],
            "idiomas": ["inglés", "español"]
        }
        
        respuesta = (
            f"Veo que mencionas '{user_message}'. ¿Te refieres a alguna tecnología, empresa o idioma?\n\n"
            f"💻 **Tecnologías**: {', '.join(sugerencias['tecnologias'])}\n"
            f"🏢 **Empresas**: {', '.join(sugerencias['empresas'])}\n"
            f"🌍 **Idiomas**: {', '.join(sugerencias['idiomas'])}"
        )
        
        dispatcher.utter_message(
            json_message={
                "text": respuesta,
            }
        )
        return []

    async def _clasificar_con_spacy(
        self, dispatcher: CollectingDispatcher, user_message: str, intent_name: str
    ) -> List[Dict[Text, Any]]:
        """Clasificación general con spaCy"""
        print("🔍 [DEBUG] Usando clasificación spaCy...")
        
        doc = nlp(user_message)
        if "textcat" not in nlp.pipe_names:
            dispatcher.utter_message(
                json_message={
                    "text": "No se a qué te refieres.",
                }
            )
            return []

        scores = doc.cats
        label = max(scores, key=scores.get)
        confidence = scores[label]

        print(f"🎯 [DEBUG] spaCy - Categoría: '{label}' (confianza: {confidence:.4f})")

        if confidence < 0.5:
            label = "desconocido"

        # Redireccionar según categoría detectada
        if label == "tecnologia_especifica":
            print("✅ [DEBUG] spaCy detectó tecnología específica")
            return [FollowupAction("action_tecnologia_especifica")]
        elif label == "tecnologia_general":
            print("✅ [DEBUG] spaCy detectó tecnología general")
            return [FollowupAction("action_tecnologia_general")]
        elif label == "empresa_especifica":
            print("✅ [DEBUG] spaCy detectó empresa específica")
            return [FollowupAction("action_experiencia_especifica")]
        elif label == "empresa_general":
            print("✅ [DEBUG] spaCy detectó empresa general")
            return [FollowupAction("action_experiencia_general")]
        elif label == "idioma_especifico":
            print("✅ [DEBUG] spaCy detectó idioma específico")
            return [FollowupAction("action_idioma_especifico")]
        elif label == "idioma_general":
            print("✅ [DEBUG] spaCy detectó idioma general")
            return [FollowupAction("action_idioma_general")]
        else:
            opciones_fallback = [
                "No estoy seguro de qué te refieres. ¿Podrías ser más específico?",
                "Hmm, no entiendo bien. ¿Podrías darme más detalles?",
                "No logro identificar eso. ¿Puedes reformularlo o ser más claro?"
            ]
            dispatcher.utter_message(
                json_message={
                    "text": random.choice(opciones_fallback),
                }
            )

        return []

    def _buscar_en_tecnologias(self, mensaje: str) -> str:
        """Búsqueda directa en tecnologías desde el mensaje original"""
        mensaje_lower = mensaje.lower()
        
        # Buscar por clave de tecnología en el mensaje
        for tech_key in TECNOLOGIAS.keys():
            # Buscar la clave y sus variantes
            tech_variants = [
                tech_key,
                tech_key.replace('_', ' '),
                tech_key.replace('_', '')
            ]
            
            for variant in tech_variants:
                if variant in mensaje_lower:
                    print(f"✅ [DEBUG] Encontrado por clave: {tech_key} (variante: {variant})")
                    return tech_key
        
        # Buscar por display name en el mensaje
        for tech_key, tech_info in TECNOLOGIAS.items():
            display_name = tech_info["display_name"].lower()
            if display_name in mensaje_lower:
                print(f"✅ [DEBUG] Encontrado por display name: {tech_key} -> {display_name}")
                return tech_key
        
        return None

    def _buscar_en_empresas(self, mensaje: str) -> str:
        """Búsqueda en empresas desde el mensaje original"""
        mensaje_lower = mensaje.lower()
        
        # Buscar por clave de empresa en el mensaje
        for emp_key in EMPRESAS.keys():
            # Buscar la clave y sus variantes
            emp_variants = [
                emp_key,
                emp_key.replace('_', ' '),
                emp_key.replace('_', '')
            ]
            
            for variant in emp_variants:
                if variant in mensaje_lower:
                    print(f"✅ [DEBUG] Encontrado empresa por clave: {emp_key}")
                    return emp_key
        
        # Buscar por display name en el mensaje
        for emp_key, emp_info in EMPRESAS.items():
            display_name = emp_info["display_name"].lower()
            if display_name in mensaje_lower:
                print(f"✅ [DEBUG] Encontrado empresa por display name: {emp_key} -> {display_name}")
                return emp_key
        
        return None

    def _buscar_en_idiomas(self, mensaje: str) -> str:
        """Búsqueda en idiomas desde el mensaje original"""
        mensaje_lower = mensaje.lower()
        
        # Buscar por clave de idioma en el mensaje
        for idioma_key in IDIOMAS.keys():
            # Buscar la clave y sus variantes
            idioma_variants = [
                idioma_key,
                idioma_key.replace('_', ' '),
                idioma_key.replace('_', '')
            ]
            
            for variant in idioma_variants:
                if variant in mensaje_lower:
                    print(f"✅ [DEBUG] Encontrado idioma por clave: {idioma_key}")
                    return idioma_key
        
        # Buscar por display name en el mensaje
        for idioma_key, idioma_info in IDIOMAS.items():
            display_name = idioma_info["display_name"].lower()
            if display_name in mensaje_lower:
                print(f"✅ [DEBUG] Encontrado idioma por display name: {idioma_key} -> {display_name}")
                return idioma_key
        
        return None