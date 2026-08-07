from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from oracle.config import settings
from oracle.graph.graph import build_graph
from oracle.state.state import State


class DecisionRequest(BaseModel):
    """Request body for decision making."""
    problem_description: str = Field(..., description="The problem to analyze")
    user_input: str = Field(default="", description="Additional context")


class DecisionResponse(BaseModel):
    """Response with ORACLE decision."""
    final_decision: str
    decision_reasoning: str
    final_confidence: float
    climate_analysis: str = ""
    economy_analysis: str = ""
    health_analysis: str = ""
    citizen_perspective: str = ""
    ethics_evaluation: str = ""
    status: str = "success"


app = FastAPI(title="ORACLE", version="0.1.0")
graph = None


@app.on_event("startup")
async def startup_event():
    """Initialize graph on startup."""
    global graph
    try:
        graph = build_graph()
    except Exception as e:
        print(f"Warning: Could not initialize graph: {e}")


@app.get("/health")
async def health() -> dict:
    """Health-check endpoint for production readiness monitoring."""
    return {
        "status": "ok",
        "api_configured": bool(settings.OPENAI_API_KEY),
        "graph_ready": graph is not None
    }


@app.get("/")
async def root() -> dict:
    return {
        "service": "ORACLE",
        "version": "0.1.0",
        "ready": bool(settings.OPENAI_API_KEY) and graph is not None
    }


@app.post("/decide", response_model=DecisionResponse)
async def make_decision(request: DecisionRequest) -> DecisionResponse:
    """
    Get ORACLE's multi-agent decision on a problem.
    
    Runs all domain agents (Climate, Economy, Health, Citizen, Ethics)
    in parallel, then Judge Agent synthesizes into final decision.
    """
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY not configured"
        )
    
    if not graph:
        raise HTTPException(
            status_code=503,
            detail="Graph not initialized"
        )
    
    try:
        # Create initial state
        initial_state = State(
            problem_description=request.problem_description,
            user_input=request.user_input
        )
        
        # Run graph
        final_state = graph.invoke(initial_state)
        
        # Extract responses
        climate_text = ""
        if final_state.climate_analysis:
            climate_text = final_state.climate_analysis.analysis
        
        economy_text = ""
        if final_state.economy_analysis:
            economy_text = final_state.economy_analysis.analysis
        
        health_text = ""
        if final_state.health_analysis:
            health_text = final_state.health_analysis.analysis
        
        citizen_text = ""
        if final_state.citizen_perspective:
            citizen_text = final_state.citizen_perspective.analysis
        
        ethics_text = ""
        if final_state.ethics_evaluation:
            ethics_text = final_state.ethics_evaluation.analysis
        
        return DecisionResponse(
            final_decision=final_state.final_decision or "Decision pending",
            decision_reasoning=final_state.decision_reasoning or "Analysis in progress",
            final_confidence=final_state.final_confidence or 0.0,
            climate_analysis=climate_text,
            economy_analysis=economy_text,
            health_analysis=health_text,
            citizen_perspective=citizen_text,
            ethics_evaluation=ethics_text
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Decision process failed: {str(e)}"
        )


