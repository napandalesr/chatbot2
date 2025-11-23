from rasa_sdk import Action 
from rasa_sdk.interfaces import Tracker
from typing import Any, Text, Dict, List
import random

from ..data import EMPRESAS, TECNOLOGIAS

class ActionPerfilGeneral(Action):
  def name(self) -> Text:
    return "action_perfil_general"
  
  async def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    titulares = [
      f"¡Soy **Ingeniero de Sistemas Full-Stack** con 4+ años de experiencia 🚀",
      f"¡Soy **Desarrollador Full-Stack** especializado en tecnologías modernas 💻", 
      f"Soy **Ingeniero de Sistemas** con expertise en desarrollo web y móvil 🛠️"
    ]
        
    introduction = random.choice(titulares)
    introduction += "\n\n"
    introduction += "Mi pasión es crear soluciones tecnológicas escalables y de alto impacto. "
    introduction += "Me especializo en el desarrollo de aplicaciones web y móviles usando las mejores prácticas y arquitecturas modernas."

    total_empresas = len(EMPRESAS)
    años_experiencia = 6  
    
    
    lines = [f"**• {años_experiencia}+ años** de experiencia profesional"]
    lines.append(f"**• {total_empresas} empresas** desde startups hasta multinacionales")
    lines.append("")
    
    # Fortalezas principales
    lines.append("**💪 Fortalezas principales:**")
    fortalezas = [
      "Desarrollo Full-Stack con React, Node.js y TypeScript",
      "Arquitectura de software escalable y mantenible",
      "Optimización de performance y experiencia de usuario", 
      "Liderazgo técnico",
      "Metodologías ágiles y DevOps"
    ]
    for fortaleza in fortalezas:
      lines.append(f"  • {fortaleza}")
    
    categorias_especializacion = {}
    for info in TECNOLOGIAS.values():
      categoria = info.get("categoria", "general")
      if categoria not in categorias_especializacion:
        categorias_especializacion[categoria] = []
      categorias_especializacion[categoria].append(info)

    dispatcher.utter_message(
      json_message = {
        "text": introduction,
        "title": "**📊 MI PERFIL**",
        "list": lines
      }
    )

    return []