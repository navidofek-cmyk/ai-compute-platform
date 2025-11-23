"""
AI-powered endpoints pro konverzační rozhraní
"""
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import structlog

from app.services.ai_assistant import get_ai_assistant
from app.services.compute_client import get_compute_client

logger = structlog.get_logger()

router = APIRouter(
    prefix="/api/v1/ai",
    tags=["AI Assistant"]
)


class NaturalLanguageQuery(BaseModel):
    """Přirozený jazykový dotaz"""
    query: str = Field(..., description="Dotaz v přirozeném jazyce", min_length=3)
    auto_execute: bool = Field(True, description="Automaticky spustit výpočet")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Vynásob dvě matice 3x3 s náhodnými čísly",
                "auto_execute": True
            }
        }


class AnalysisRequest(BaseModel):
    """Požadavek na AI analýzu výsledku"""
    operation: str = Field(..., description="Typ operace")
    result: Dict[str, Any] = Field(..., description="Výsledek z compute service")
    
    class Config:
        json_schema_extra = {
            "example": {
                "operation": "statistics",
                "result": {
                    "statistics": {
                        "mean": 50.5,
                        "std_dev": 28.8,
                        "min": 1.0,
                        "max": 100.0,
                        "count": 1000
                    }
                }
            }
        }


class RecommendationRequest(BaseModel):
    """Požadavek na doporučení parametrů"""
    operation: str = Field(..., description="Typ operace")
    context: Optional[Dict[str, Any]] = Field(None, description="Kontext požadavku")
    
    class Config:
        json_schema_extra = {
            "example": {
                "operation": "monte_carlo",
                "context": {
                    "data_size": "large",
                    "accuracy_required": "high"
                }
            }
        }


@router.post("/query", summary="Přirozený jazykový dotaz")
async def natural_language_query(query: NaturalLanguageQuery):
    """
    Převede přirozený jazyk na API požadavek a volitelně ho spustí.
    
    Příklady dotazů:
    - "Vynásob dvě matice 3x3"
    - "Udělej statistickou analýzu 1000 náhodných čísel"
    - "Spusť Monte Carlo simulaci s 10000 iteracemi"
    """
    try:
        assistant = get_ai_assistant()
        
        # Převod na strukturovaný dotaz
        structured_query = assistant.generate_query_from_text(query.query)
        
        logger.info("nl_query_generated", original=query.query, structured=structured_query)
        
        response = {
            "original_query": query.query,
            "generated_query": structured_query,
            "status": "generated"
        }
        
        # Pokud má být automaticky spuštěno
        if query.auto_execute:
            operation = structured_query.get("operation")
            parameters = structured_query.get("parameters", {})
            
            # Zavolání compute service podle typu operace
            compute_client = get_compute_client()
            
            if operation == "matrix_multiply":
                result = compute_client.multiply_matrices(
                    parameters.get("matrix_a"),
                    parameters.get("matrix_b")
                )
            elif operation == "statistics":
                result = compute_client.analyze_statistics(
                    parameters.get("data", [])
                )
            elif operation == "monte_carlo":
                result = compute_client.run_monte_carlo(
                    parameters.get("iterations", 1000),
                    parameters.get("seed", 0)
                )
            elif operation == "vector_operation":
                result = compute_client.vector_operation(
                    parameters.get("operation_type"),
                    parameters.get("vector_a"),
                    parameters.get("vector_b")
                )
            else:
                raise ValueError(f"Neznámá operace: {operation}")
            
            # AI analýza výsledku
            analysis = assistant.analyze_result(operation, result)
            
            response.update({
                "status": "executed",
                "result": result,
                "ai_analysis": analysis
            })
            
            logger.info("nl_query_executed", operation=operation)
        
        return response
        
    except Exception as e:
        logger.error("nl_query_failed", error=str(e), query=query.query)
        raise HTTPException(
            status_code=500,
            detail=f"Chyba při zpracování dotazu: {str(e)}"
        )


@router.post("/analyze", summary="AI analýza výsledku")
async def analyze_result(request: AnalysisRequest):
    """
    Vytvoří lidsky čitelnou AI analýzu výsledku výpočtu.
    
    Použití:
    1. Spusťte výpočet přes standardní API
    2. Pošlete výsledek sem pro AI vysvětlení
    """
    try:
        assistant = get_ai_assistant()
        analysis = assistant.analyze_result(request.operation, request.result)
        
        logger.info("ai_analysis_completed", operation=request.operation)
        
        return {
            "operation": request.operation,
            "analysis": analysis,
            "result_summary": request.result
        }
        
    except Exception as e:
        logger.error("ai_analysis_failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Chyba při AI analýze: {str(e)}"
        )


@router.post("/recommend", summary="Doporučení parametrů")
async def recommend_parameters(request: RecommendationRequest):
    """
    AI doporučí optimální parametry pro danou operaci.
    
    Použití:
    - Před spuštěním operace se zeptejte na optimální parametry
    - AI vezme v úvahu kontext a doporučí nejlepší nastavení
    """
    try:
        assistant = get_ai_assistant()
        recommendation = assistant.recommend_parameters(
            request.operation,
            request.context
        )
        
        logger.info("ai_recommendation_completed", operation=request.operation)
        
        return {
            "operation": request.operation,
            "context": request.context,
            "recommendation": recommendation
        }
        
    except Exception as e:
        logger.error("ai_recommendation_failed", error=str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Chyba při vytváření doporučení: {str(e)}"
        )


@router.get("/health", summary="AI Assistant health check")
async def ai_health():
    """Kontrola stavu AI asistenta"""
    try:
        assistant = get_ai_assistant()
        return {
            "status": "healthy",
            "model": assistant.model,
            "service": "AI Assistant"
        }
    except Exception as e:
        logger.error("ai_health_check_failed", error=str(e))
        raise HTTPException(
            status_code=503,
            detail=f"AI Assistant není dostupný: {str(e)}"
        )
