from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re

from ..data import EMPRESAS

class ActionTiempoExperienciaTotal(Action):
    def name(self) -> Text:
        return "action_tiempo_experiencia_total"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        
        # Calcular la experiencia total y encontrar el año más temprano
        experiencia_total_meses = 0
        empresas_contabilizadas = []
        año_inicio = None
        
        for empresa_key, empresa_data in EMPRESAS.items():
            tiempo = empresa_data.get('tiempo', '')
            periodo = empresa_data.get('periodo', '')
            
            # Extraer año de inicio del período
            año_empresa = self.extraer_año_inicio(periodo)
            if año_empresa and (año_inicio is None or año_empresa < año_inicio):
                año_inicio = año_empresa
            
            # Calcular meses para cada empresa
            meses = self.calcular_meses_experiencia(tiempo)
            experiencia_total_meses += meses
            
            empresas_contabilizadas.append({
                'empresa': empresa_data['display_name'],
                'tiempo': tiempo,
                'periodo': periodo,
                'meses': meses
            })
        
        # Calcular años y meses totales
        años_totales = experiencia_total_meses // 12
        meses_restantes = experiencia_total_meses % 12
        
        # Construir mensaje de respuesta
        mensaje = f"Tengo **{años_totales} años de experiencia total** en desarrollo "
        
        if meses_restantes > 0:
            mensaje += f"({años_totales} años y {meses_restantes} meses)"
        
        mensaje += f".\n\nMi experiencia incluye:\n"
        
        for emp in empresas_contabilizadas:
            mensaje += f"• **{emp['empresa']}**: {emp['tiempo']} ({emp['periodo']})\n"
        
        if año_inicio:
            mensaje += f"\nHe trabajado como desarrollador desde {año_inicio} hasta la actualidad, "
        else:
            mensaje += f"\nHe trabajado como desarrollador desde mis inicios profesionales, "
        
        mensaje += f"acumulando {experiencia_total_meses} meses de experiencia profesional."
        
        dispatcher.utter_message(text=mensaje)
        return []
    
    def calcular_meses_experiencia(self, tiempo_str: str) -> int:
        """Calcula meses aproximados basado en la descripción de tiempo"""
        tiempo_str = tiempo_str.lower()
        
        # Si contiene "actual", considerar hasta la fecha actual
        if 'actual' in tiempo_str:
            if '6 meses' in tiempo_str:
                return 6
            return 6  # Valor por defecto para empleo actual
        
        if 'año' in tiempo_str and 'mes' in tiempo_str:
            # Ejemplo: "1 año 6 meses"
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
            # Ejemplo: "2 años"
            años = int(''.join(filter(str.isdigit, tiempo_str.split('años')[0])))
            return años * 12
        
        elif 'año' in tiempo_str:
            # Ejemplo: "1 año"
            años = int(''.join(filter(str.isdigit, tiempo_str.split('año')[0])))
            return años * 12
        
        elif 'meses' in tiempo_str:
            # Ejemplo: "6 meses"
            meses = int(''.join(filter(str.isdigit, tiempo_str.split('meses')[0])))
            return meses
        
        # Por defecto para casos no especificados
        return 6
    
    def extraer_año_inicio(self, periodo: str) -> int:
        """Extrae el año de inicio del período"""
        # Buscar años de 4 dígitos en el período
        años = re.findall(r'\b(20\d{2})\b', periodo)
        if años:
            return min(map(int, años))
        return None