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
    final_decision: str = "Analysis complete"
    decision_reasoning: str = "Decision process finished"
    final_confidence: float = 0.0
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
        
        # Extract responses - handle both dict and State object
        try:
            if isinstance(final_state, dict):
                climate_text = ""
                if "climate_analysis" in final_state and final_state["climate_analysis"]:
                    ca = final_state["climate_analysis"]
                    climate_text = ca.analysis if hasattr(ca, 'analysis') else str(ca)
                
                economy_text = ""
                if "economy_analysis" in final_state and final_state["economy_analysis"]:
                    ea = final_state["economy_analysis"]
                    economy_text = ea.analysis if hasattr(ea, 'analysis') else str(ea)
                
                health_text = ""
                if "health_analysis" in final_state and final_state["health_analysis"]:
                    ha = final_state["health_analysis"]
                    health_text = ha.analysis if hasattr(ha, 'analysis') else str(ha)
                
                citizen_text = ""
                if "citizen_perspective" in final_state and final_state["citizen_perspective"]:
                    cp = final_state["citizen_perspective"]
                    citizen_text = cp.analysis if hasattr(cp, 'analysis') else str(cp)
                
                ethics_text = ""
                if "ethics_evaluation" in final_state and final_state["ethics_evaluation"]:
                    ee = final_state["ethics_evaluation"]
                    ethics_text = ee.analysis if hasattr(ee, 'analysis') else str(ee)
                
                final_decision = final_state.get("final_decision", "No decision yet")
                decision_reasoning = final_state.get("decision_reasoning", "Analysis pending")
                final_confidence = final_state.get("final_confidence", 0.0)
            else:
                # State object
                climate_text = final_state.climate_analysis.analysis if final_state.climate_analysis else ""
                economy_text = final_state.economy_analysis.analysis if final_state.economy_analysis else ""
                health_text = final_state.health_analysis.analysis if final_state.health_analysis else ""
                citizen_text = final_state.citizen_perspective.analysis if final_state.citizen_perspective else ""
                ethics_text = final_state.ethics_evaluation.analysis if final_state.ethics_evaluation else ""
                
                final_decision = final_state.final_decision or "No decision yet"
                decision_reasoning = final_state.decision_reasoning or "Analysis pending"
                final_confidence = final_state.final_confidence or 0.0
        except Exception as extract_err:
            # Fallback to empty/default values
            return DecisionResponse(
                final_decision=f"Error extracting results: {str(extract_err)}",
                decision_reasoning="System processing encountered an issue",
                final_confidence=0.0,
                climate_analysis="",
                economy_analysis="",
                health_analysis="",
                citizen_perspective="",
                ethics_evaluation=""
            )
        
        return DecisionResponse(
            final_decision=final_decision,
            decision_reasoning=decision_reasoning,
            final_confidence=final_confidence,
            climate_analysis=climate_text,
            economy_analysis=economy_text,
            health_analysis=health_text,
            citizen_perspective=citizen_text,
            ethics_evaluation=ethics_text
        )
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Decision process failed: {str(e)}\n{error_trace}"
        )


