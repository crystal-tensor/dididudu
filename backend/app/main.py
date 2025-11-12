from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime, timedelta

from .routers import auth, analysis, payments, reports

app = FastAPI(title="UP主竞争分析平台", version="0.1.0")

# 在 FastAPI 初始化后添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发期先放开；上线再收紧为你的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = "/Users/danielcrystal/work/dididudu/frontend"

# 静态资源改挂载到 /static，避免覆盖 /api/*
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# 显式返回各页面
@app.get("/")
@app.get("/index.html")
def page_index():
    return FileResponse(f"{FRONTEND_DIR}/index.html")

@app.get("/pricing.html")
def page_pricing():
    return FileResponse(f"{FRONTEND_DIR}/pricing.html")

@app.get("/reports.html")
def page_reports():
    return FileResponse(f"{FRONTEND_DIR}/reports.html")

# API 路由
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(payments.router, prefix="/api/payments", tags=["payments"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])

@app.get("/api/health")
def health():
    return {"status": "ok"}

# 开启 CORS（开发期放开，线上收紧为你的前端域名）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 简单的内存态存储：scene -> {status, created_at}
SCENE_TTL_MINUTES = 10
scene_store = {}

def get_scene_status(scene: str):
    data = scene_store.get(scene)
    if not data:
        return "not_found"
    # 过期检查
    if datetime.utcnow() - data["created_at"] > timedelta(minutes=SCENE_TTL_MINUTES):
        data["status"] = "expired"
    return data["status"]

@app.get("/api/auth/wechat/authorize")
def authorize(scene: str = Query(..., min_length=3)):
    # 创建/重置场景为 pending
    scene_store[scene] = {"status": "pending", "created_at": datetime.utcnow()}
    # 简单返回一个引导页；二维码由前端生成
    html = f"""
    <html><body>
      <h3>扫码占位：scene={scene}</h3>
      <p>这是占位授权页，真实对接请替换为公众号网页授权。</p>
    </body></html>
    """
    return HTMLResponse(content=html, status_code=200)

@app.get("/api/auth/wechat/poll")
def poll(scene: str = Query(..., min_length=3)):
    status = get_scene_status(scene)
    return JSONResponse({"scene": scene, "status": status})

@app.post("/api/auth/wechat/confirm")
def confirm(scene: str = Query(..., min_length=3)):
    if scene not in scene_store:
        # 如果没 authorize 过，也创建
        scene_store[scene] = {"status": "pending", "created_at": datetime.utcnow()}
    scene_store[scene]["status"] = "confirmed"
    return JSONResponse({"scene": scene, "status": "confirmed"})
