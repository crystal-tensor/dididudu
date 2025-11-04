import subprocess
import sys
from pathlib import Path
from datetime import datetime
import threading
import os

REPORT_ROOT = Path("/Users/danielcrystal/work/dididudu/reports")
REPORT_ROOT.mkdir(parents=True, exist_ok=True)

PYTHON = sys.executable
WORKDIR = Path("/Users/danielcrystal/work/dididudu")

# 简易内存任务表
JOBS: dict[str, dict] = {}


def _run_pipeline(job_id: str, export_dir: Path, platform: str, user_uid: str | None, competitor_uids: list[str], competitor_links: list[str]):
    try:
        # 1) 运行 example.py（此处未参数化，后续可改造成接收platform/uid/links）
        proc1 = subprocess.run([PYTHON, "example.py"], cwd=str(WORKDIR), capture_output=True, text=True)
        JOBS[job_id]["log_example"] = proc1.stdout + "\n" + proc1.stderr
        if proc1.returncode != 0:
            JOBS[job_id]["status"] = "failed"
            JOBS[job_id]["error"] = "example.py 执行失败"
            return
        
        # 2) 运行 report3.py，导出前若干页图片
        env = {**dict(**os.environ), **{"EXPORT_DIR": str(export_dir)}}
        proc2 = subprocess.run([PYTHON, "report3.py"], cwd=str(WORKDIR), env=env, capture_output=True, text=True)
        JOBS[job_id]["log_report"] = proc2.stdout + "\n" + proc2.stderr
        if proc2.returncode != 0:
            JOBS[job_id]["status"] = "failed"
            JOBS[job_id]["error"] = "report3.py 执行失败"
            return
        
        JOBS[job_id]["status"] = "done"
    except Exception as e:
        JOBS[job_id]["status"] = "failed"
        JOBS[job_id]["error"] = str(e)


def run_analysis_task(platform: str, user_uid: str | None, competitor_uids: list[str], competitor_links: list[str]):
    from datetime import datetime
    job_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    user_id = "anonymous"
    export_dir = REPORT_ROOT / user_id / job_id
    export_dir.mkdir(parents=True, exist_ok=True)

    JOBS[job_id] = {
        "job_id": job_id,
        "user_id": user_id,
        "status": "running",
        "export_dir": str(export_dir),
        "params": {
            "platform": platform,
            "user_uid": user_uid,
            "competitor_uids": competitor_uids,
            "competitor_links": competitor_links,
        },
    }

    t = threading.Thread(target=_run_pipeline, args=(job_id, export_dir, platform, user_uid, competitor_uids, competitor_links), daemon=True)
    t.start()

    return {
        "job_id": job_id,
        "user_id": user_id,
        "status": "running",
        "export_dir": str(export_dir),
        "message": "任务已创建，正在后台生成报告。前两页生成后可在报告中心查看。",
    }
