from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re

from ..data import EMPRESAS

class ActionExperienciaTecnologia(Action):
    def name(self) -> Text:
        return "action_experiencia_tecnologia"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        
        # Obtener la tecnología del slot o entity
        tecnologia = next(tracker.get_latest_entity_values("tecnologia"), None)
        
        if not tecnologia:
            dispatcher.utter_message(text="¿Sobre qué tecnología específica te gustaría conocer mi experiencia? Por ejemplo: React, JavaScript, Python, etc.")
            return []
        
        tecnologia = tecnologia.lower()
        
        # Buscar en qué empresas usó la tecnología
        empresas_con_tecnologia = []
        experiencia_total_meses = 0
        año_inicio = None
        
        for empresa_key, empresa_data in EMPRESAS.items():
            tecnologias = [tech.lower() for tech in empresa_data.get('tecnologias', [])]
            
            # Verificar si usa la tecnología (búsqueda flexible)
            if self.coincide_tecnologia(tecnologia, tecnologias):
                tiempo = empresa_data.get('tiempo', '')
                periodo = empresa_data.get('periodo', '')
                
                # Extraer año de inicio del período
                año_empresa = self.extraer_año_inicio(periodo)
                if año_empresa and (año_inicio is None or año_empresa < año_inicio):
                    año_inicio = año_empresa
                
                # Calcular meses para cada empresa
                meses = self.calcular_meses_experiencia(tiempo)
                experiencia_total_meses += meses
                
                empresas_con_tecnologia.append({
                    'empresa': empresa_data['display_name'],
                    'cargo': empresa_data['cargo'],
                    'tiempo': tiempo,
                    'periodo': periodo,
                    'meses': meses
                })
        
        # Construir mensaje de respuesta
        if empresas_con_tecnologia:
            años_totales = experiencia_total_meses // 12
            meses_restantes = experiencia_total_meses % 12
            
            mensaje = f"Tengo **{años_totales} años"
            if meses_restantes > 0:
                mensaje += f" y {meses_restantes} meses"
            mensaje += f"** de experiencia con **{tecnologia.title()}**.\n\n"
            
            mensaje += f"He usado {tecnologia.title()} en:\n"
            for emp in empresas_con_tecnologia:
                mensaje += f"• **{emp['empresa']}** ({emp['cargo']}): {emp['tiempo']}\n"
            
            if año_inicio:
                mensaje += f"\nMi primera experiencia con {tecnologia.title()} fue en {año_inicio}."
            
        else:
            mensaje = f"No tengo experiencia registrada con **{tecnologia.title()}** en mi historial laboral."
        
        dispatcher.utter_message(text=mensaje)
        return [SlotSet("tecnologia", tecnologia)]
    
    def coincide_tecnologia(self, tecnologia_buscada: str, tecnologias_empresa: List[str]) -> bool:
        """Verifica si la tecnología coincide con alguna de las tecnologías de la empresa"""
        tecnologia_buscada = tecnologia_buscada.lower()
        
        # Búsqueda flexible para variaciones comunes
        variaciones = {
            'react': ['react', 'react_native', 'next_js'],
            'javascript': ['javascript', 'js'],
            'typescript': ['typescript', 'ts'],
            'node': ['node_js', 'node', 'nestjs'],
            'python': ['python'],
            'java': ['java'],
            'docker': ['docker'],
            # Agregar más variaciones según necesites
        }
        
        if tecnologia_buscada in variaciones:
            return any(tech in variaciones[tecnologia_buscada] for tech in tecnologias_empresa)
        else:
            return tecnologia_buscada in tecnologias_empresa
    
    def calcular_meses_experiencia(self, tiempo_str: str) -> int:
        """Calcula meses aproximados basado en la descripción de tiempo"""
        # (Usar la misma función que en la action anterior)
        tiempo_str = tiempo_str.lower()
        
        if 'actual' in tiempo_str:
            if '6 meses' in tiempo_str:
                return 6
            return 6
        
        if 'año' in tiempo_str and 'mes' in tiempo_str:
            partes = tiempo_str.split()
            años = 0
            meses = 0
            for parte in partes:
                if 'año' in parte:
                    años = int(''.join(filter(str.isdigit, parte)))
                elif 'mes' in parte:
                    meses = int(''.join(filter(str.isdigit, parte)))
            return años * 12 + meses
        
        elif 'años' in tiempo_str:
            años = int(''.join(filter(str.isdigit, tiempo_str.split('años')[0])))
            return años * 12
        
        elif 'año' in tiempo_str:
            años = int(''.join(filter(str.isdigit, tiempo_str.split('año')[0])))
            return años * 12
        
        elif 'meses' in tiempo_str:
            meses = int(''.join(filter(str.isdigit, tiempo_str.split('meses')[0])))
            return meses
        
        return 6
    
    def extraer_año_inicio(self, periodo: str) -> int:
        """Extrae el año de inicio del período"""
        años = re.findall(r'\b(20\d{2})\b', periodo)
        if años:
            return min(map(int, años))
        return None