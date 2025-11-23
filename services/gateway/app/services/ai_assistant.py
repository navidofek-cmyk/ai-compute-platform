"""
OpenAI Assistant Service - Inteligentní vrstva pro komunikaci s uživatelem
"""
import os
from typing import Dict, Any, Optional
import logging
from openai import OpenAI
import json

logger = logging.getLogger(__name__)


class AIAssistant:
    """OpenAI asistent pro inteligentní interakci s compute službou"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None,
                 max_tokens: Optional[int] = None, temperature: Optional[float] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY není nastavený! Zkontrolujte .env soubor")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.max_tokens = max_tokens or int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        self.temperature = temperature or float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        
        logger.info(f"AI Assistant inicializován s modelem {self.model}")
    
    def analyze_result(self, operation: str, result: Dict[str, Any]) -> str:
        """
        Analyzuje výsledek výpočtu a vytvoří lidsky čitelné vysvětlení
        
        Args:
            operation: Typ operace (matrix_multiply, statistics, monte_carlo, vector)
            result: Výsledek z compute service
            
        Returns:
            Lidsky čitelné vysvětlení výsledku
        """
        prompt = self._create_analysis_prompt(operation, result)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Jsi pomocný asistent, který vysvětluje matematické a statistické výsledky jednoduchým způsobem. Odpovídáš v češtině."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            explanation = response.choices[0].message.content.strip()
            logger.info(f"AI analýza dokončena pro {operation}")
            return explanation
            
        except Exception as e:
            logger.error(f"Chyba při AI analýze: {e}")
            return f"Nepodařilo se vytvořit AI analýzu: {str(e)}"
    
    def generate_query_from_text(self, user_input: str) -> Dict[str, Any]:
        """
        Převede přirozený jazyk na API požadavek
        
        Args:
            user_input: Uživatelský text (např. "vynásob dvě matice 3x3")
            
        Returns:
            Strukturovaný API požadavek
        """
        prompt = f"""
Převeď následující požadavek uživatele na JSON API požadavek pro výpočetní službu.

Dostupné operace:
1. matrix_multiply - násobení matic
2. statistics - statistická analýza
3. monte_carlo - Monte Carlo simulace
4. vector_operation - vektorové operace (add, subtract, dot_product, cross_product)

Uživatelský požadavek: {user_input}

Vrať POUZE validní JSON objekt s klíči:
- operation: typ operace
- parameters: parametry pro danou operaci

Příklad pro násobení matic:
{{
  "operation": "matrix_multiply",
  "parameters": {{
    "matrix_a": [[1, 2], [3, 4]],
    "matrix_b": [[5, 6], [7, 8]]
  }}
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Jsi asistent, který převádí přirozený jazyk na API požadavky. Vracíš POUZE validní JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=0.3  # Nižší teplota pro přesnější JSON
            )
            
            json_str = response.choices[0].message.content.strip()
            # Odstranění markdown code blocku pokud existuje
            if json_str.startswith("```"):
                json_str = json_str.split("```")[1]
                if json_str.startswith("json"):
                    json_str = json_str[4:]
            
            query = json.loads(json_str)
            logger.info(f"AI vygenerovala query: {query}")
            return query
            
        except Exception as e:
            logger.error(f"Chyba při generování query: {e}")
            raise ValueError(f"Nepodařilo se zpracovat požadavek: {str(e)}")
    
    def recommend_parameters(self, operation: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Doporučí optimální parametry pro danou operaci
        
        Args:
            operation: Typ operace
            context: Kontext (např. velikost dat, požadovaná přesnost)
            
        Returns:
            Doporučené parametry
        """
        context_str = json.dumps(context) if context else "žádný specifický kontext"
        
        prompt = f"""
Doporuč optimální parametry pro operaci: {operation}
Kontext: {context_str}

Pro operace:
- matrix_multiply: velikost matic
- statistics: počet vzorků
- monte_carlo: počet simulací
- vector_operation: velikost vektorů

Vrať JSON s doporučenými parametry a zdůvodněním.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Jsi expert na optimalizaci výpočetních parametrů."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=0.5
            )
            
            recommendation = response.choices[0].message.content.strip()
            logger.info(f"AI doporučení vytvořeno pro {operation}")
            return {"recommendation": recommendation}
            
        except Exception as e:
            logger.error(f"Chyba při vytváření doporučení: {e}")
            return {"error": str(e)}
    
    def _create_analysis_prompt(self, operation: str, result: Dict[str, Any]) -> str:
        """Vytvoří prompt pro analýzu výsledku"""
        
        if operation == "matrix_multiply":
            return f"""
Vysvětli výsledek násobení matic:
- Rozměry výsledné matice: {result.get('result_dimensions')}
- Čas výpočtu: {result.get('computation_time_ms')} ms
- První řádek výsledku: {result.get('result', [[]])[0] if result.get('result') else 'N/A'}

Vysvětli co to znamená a zda je výkon dobrý.
"""
        
        elif operation == "statistics":
            stats = result.get('statistics', {})
            return f"""
Vysvětli statistickou analýzu:
- Průměr: {stats.get('mean')}
- Směrodatná odchylka: {stats.get('std_dev')}
- Minimum: {stats.get('min')}
- Maximum: {stats.get('max')}
- Počet vzorků: {stats.get('count')}

Co tyto hodnoty znamenají? Jak jsou data rozložená?
"""
        
        elif operation == "monte_carlo":
            return f"""
Vysvětli výsledek Monte Carlo simulace:
- Výsledek: {result.get('result')}
- Počet simulací: {result.get('iterations')}
- Čas výpočtu: {result.get('computation_time_ms')} ms

Co tento výsledek znamená a je počet simulací dostatečný?
"""
        
        elif operation == "vector":
            return f"""
Vysvětli výsledek vektorové operace:
- Operace: {result.get('operation')}
- Výsledek: {result.get('result')}
- Čas výpočtu: {result.get('computation_time_ms')} ms

Co tento výsledek znamená?
"""
        
        return f"Vysvětli výsledek operace {operation}: {json.dumps(result, indent=2)}"


# Singleton instance
_assistant_instance: Optional[AIAssistant] = None


def get_ai_assistant() -> AIAssistant:
    """Získá singleton instanci AI asistenta"""
    global _assistant_instance
    if _assistant_instance is None:
        from app.config import get_settings
        settings = get_settings()
        _assistant_instance = AIAssistant(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            max_tokens=settings.openai_max_tokens,
            temperature=settings.openai_temperature
        )
    return _assistant_instance
