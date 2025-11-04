from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from typing import List, Optional
from ..services.analysis_runner import run_analysis_task

router = APIRouter()

class AnalysisRequest(BaseModel):
    platform: str  # bilibili/xhs/douyin
    user_uid: Optional[str] = None
    competitor_uids: Optional[List[str]] = None
    competitor_links: Optional[List[str]] = None

    @field_validator('platform')
    @classmethod
    def validate_platform(cls, v: str) -> str:
        allowed = {"bilibili", "xhs", "douyin"}
        if v not in allowed:
            raise ValueError(f"platform必须为 {allowed}")
        return v

@router.post("/run")
def run_analysis(req: AnalysisRequest):
    try:
        job = run_analysis_task(req.platform, req.user_uid, req.competitor_uids or [], req.competitor_links or [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return job
