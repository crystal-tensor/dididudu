from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from typing import List, Optional
from ..services.analysis_runner import run_analysis_task

router = APIRouter()

class AnalysisRequest(BaseModel):
    platform: str  # bilibili/xhs/douyin
    user_uid: Optional[str] = None
    competitor_uids: Optional[List[str]] = None
    competitor_links: Optional[List[str]] = None

    @validator('platform')
    def validate_platform(cls, v):
        allowed = {"bilibili", "xhs", "douyin"}
        if v not in allowed:
            raise ValueError("platform必须为 {}".format(allowed))
        return v

@router.post("/run")
def run_analysis(req: AnalysisRequest):
    try:
        job = run_analysis_task(req.platform, req.user_uid, req.competitor_uids or [], req.competitor_links or [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return job
