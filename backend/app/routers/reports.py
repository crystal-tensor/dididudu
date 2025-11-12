from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List, Optional

router = APIRouter()

REPORT_ROOT = Path("/Users/danielcrystal/work/dididudu/reports")
REPORT_ROOT.mkdir(parents=True, exist_ok=True)

@router.get("/list")
def list_reports(user_id: str):
    user_dir = REPORT_ROOT / user_id
    if not user_dir.exists():
        return []
    items: List[dict] = []
    for job_dir in sorted(user_dir.glob("*")):
        if job_dir.is_dir():
            pages = sorted(job_dir.glob("page_*.png"))
            items.append({
                "job_id": job_dir.name,
                "pages": [p.name for p in pages],
            })
    return items

@router.get("/{user_id}/{job_id}/page/{page_no}")
def get_page(user_id: str, job_id: str, page_no: int, token: Optional[str] = None, preview: bool = False):
    # 会员判断：如果提供 token 且对应用户是会员，则不限制页数
    from ..state import SESSIONS, PAID_USERS
    is_member = False
    if token and token in SESSIONS:
        is_member = (SESSIONS[token] in PAID_USERS)

    # 非会员仅免费2页；预览模式下（preview=1）放行全部
    if not is_member and not preview and page_no > 2:
        raise HTTPException(status_code=402, detail="该页为付费内容，请购买会员或单次报告")

    page_path = REPORT_ROOT / user_id / job_id / f"page_{page_no}.png"
    if not page_path.exists():
        raise HTTPException(status_code=404, detail="页面不存在")
    return FileResponse(str(page_path), media_type='image/png')

@router.delete("/{user_id}/{job_id}")
def delete_report(user_id: str, job_id: str):
    user_dir = REPORT_ROOT / user_id
    job_dir = user_dir / job_id

    # 基本路径校验，防止越权
    try:
        user_dir.relative_to(REPORT_ROOT)
        job_dir.relative_to(user_dir)
    except Exception:
        raise HTTPException(status_code=400, detail="非法路径")

    if not job_dir.exists():
        raise HTTPException(status_code=404, detail="报告不存在")
    if not job_dir.is_dir():
        raise HTTPException(status_code=400, detail="不是报告目录")

    import shutil
    try:
        shutil.rmtree(job_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {e}")

    return {"ok": True, "user_id": user_id, "job_id": job_id}
