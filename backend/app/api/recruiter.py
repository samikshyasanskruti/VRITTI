from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.database.database import get_db
from backend.app.models.database_models import Job, Resume
from backend.app.services.matching.matcher import match_resume_to_jobs
import json
router=APIRouter()
class RecruiterRequest(BaseModel):
    job_id:int
    top_k:int=20
@router.post("/rank-candidates")
def rank_candidates(payload:RecruiterRequest, db:Session=Depends(get_db)):
    job=db.get(Job,payload.job_id)
    if not job: raise HTTPException(404,"Job not found.")
    resumes=db.query(Resume).all()
    if not resumes: return {"job_id":job.id,"candidates":[]}
    j={"id":job.id,"title":job.title,"company":job.company,"location":job.location,"description":job.description,"required_skills":json.loads(job.required_skills_json or "[]"),"preferred_skills":json.loads(job.preferred_skills_json or "[]")}
    ranked=[]
    for r in resumes:
        p=json.loads(r.profile_json or "{}")
        result=match_resume_to_jobs(p,r.text,[j],1)
        if result: ranked.append({"resume_id":r.id,"filename":r.filename,**result[0]})
    ranked.sort(key=lambda x:x["score"],reverse=True)
    return {"job_id":job.id,"count":len(ranked),"candidates":ranked[:max(1,min(payload.top_k,100))]}
