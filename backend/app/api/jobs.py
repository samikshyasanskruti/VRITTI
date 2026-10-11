import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.database import get_db
from backend.app.models.database_models import Job
from backend.app.schemas.job_schema import JobCreate
from backend.app.services.job.jd_parser import parse_job_description
router = APIRouter()
@router.get("")
def get_jobs(limit:int=50, offset:int=0, q:str|None=None, db:Session=Depends(get_db)):
    query=db.query(Job)
    if q: query=query.filter((Job.title.ilike(f"%{q}%")) | (Job.company.ilike(f"%{q}%")) | (Job.description.ilike(f"%{q}%")))
    rows=query.order_by(Job.id).offset(max(0,offset)).limit(max(1,min(limit,200))).all()
    return [{"id":j.id,"external_id":j.external_id,"title":j.title,"company":j.company,"location":j.location,"description":j.description[:1200],"required_skills":json.loads(j.required_skills_json or "[]"),"preferred_skills":json.loads(j.preferred_skills_json or "[]"),"work_type":j.work_type} for j in rows]
@router.post("")
def create_job(payload:JobCreate, db:Session=Depends(get_db)):
    parsed=parse_job_description(payload.title,payload.description)
    row=Job(title=payload.title,company=payload.company,location=payload.location,description=payload.description,
        required_skills_json=json.dumps(payload.required_skills or parsed["skills"]),preferred_skills_json=json.dumps(payload.preferred_skills))
    db.add(row); db.commit(); db.refresh(row)
    return {"id":row.id,"title":row.title,"required_skills":json.loads(row.required_skills_json)}
@router.get("/{job_id}")
def get_job(job_id:int, db:Session=Depends(get_db)):
    j=db.get(Job,job_id)
    if not j: raise HTTPException(404,"Job not found.")
    return {"id":j.id,"title":j.title,"company":j.company,"location":j.location,"description":j.description,"required_skills":json.loads(j.required_skills_json or "[]"),"preferred_skills":json.loads(j.preferred_skills_json or "[]")}
