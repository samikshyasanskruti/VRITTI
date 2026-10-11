from fastapi import APIRouter
from pydantic import BaseModel, Field
from backend.app.services.simulator.what_if_engine import run_what_if
router=APIRouter()
class SimRequest(BaseModel):
    current_score: float = Field(ge=0,le=100)
    missing_skills: list[str]
    selected_skills: list[str]
@router.post("/what-if")
def what_if(payload:SimRequest):
    return simulate(payload.current_score,payload.missing_skills,payload.selected_skills)
