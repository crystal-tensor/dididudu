from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import time
import base64
from io import BytesIO
import qrcode
import os

router = APIRouter()

# 简易内存会话与扫码态
from ..state import SESSIONS, SCENES, PUBLIC_URL, PAID_USERS

class WechatLoginRequest(BaseModel):
    code: str  # 微信临时code

class TokenResponse(BaseModel):
    token: str
    user_id: str

class BindAccountRequest(BaseModel):
    platform: str  # bilibili/xhs/douyin
    uid: Optional[str] = None
    links: Optional[list[str]] = None


def get_user_id(token: str) -> str:
    if token not in SESSIONS:
        raise HTTPException(status_code=401, detail="未登录或会话失效")
    return SESSIONS[token]

@router.post("/wechat/login", response_model=TokenResponse)
def wechat_login(req: WechatLoginRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="无效code")
    user_id = f"wx_{abs(hash(req.code)) % 10_000_000}"
    token = f"tk_{abs(hash(user_id))}"
    SESSIONS[token] = user_id
    return TokenResponse(token=token, user_id=user_id)

@router.get("/wechat/login", response_model=TokenResponse)
def wechat_login_get(code: str = Query(..., description="临时code，可随意填写测试")):
    if not code:
        raise HTTPException(status_code=400, detail="无效code")
    user_id = f"wx_{abs(hash(code)) % 10_000_000}"
    token = f"tk_{abs(hash(user_id))}"
    SESSIONS[token] = user_id
    return TokenResponse(token=token, user_id=user_id)

# 扫码登录：获取二维码（手机可访问的确认页）
@router.get("/wechat/qrcode")
def wechat_qrcode():
    scene = f"sc_{int(time.time()*1000)}"
    scan_url = f"{PUBLIC_URL}/api/auth/wechat/scan?scene={scene}"
    # 生成二维码
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(scan_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    SCENES[scene] = {"status": "pending", "token": None, "created_at": time.time()}
    return {"scene": scene, "qrcode": f"data:image/png;base64,{b64}", "expires_in": 180, "url": scan_url}

# 扫码登录：供手机打开的确认页面（占位）
@router.get("/wechat/scan", response_class=HTMLResponse)
def wechat_scan(scene: str):
    info = SCENES.get(scene)
    if not info:
        return HTMLResponse("<h3>链接已失效</h3>", status_code=404)
    html = (
        "<!doctype html>\n"
        "<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>"
        "<title>确认登录</title></head>\n"
        "<body style='font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial;'>"
        "<div style='max-width:520px;margin:40px auto;padding:20px;border:1px solid #eee;border-radius:12px;'>"
        "<h2>确认登录</h2>"
        "<p>是否同意在本设备登录？</p>"
        "<button style='padding:10px 16px;border-radius:8px;background:#1677ff;color:#fff;border:none;font-weight:700' onclick='confirmLogin()'>同意登录</button>"
        "<div id='msg' style='margin-top:10px;color:#666'></div>"
        "</div>"
        "<script>\n"
        "async function confirmLogin(){\n"
        f"  const r = await fetch('/api/auth/wechat/confirm?scene={scene}', {{method:'POST'}});\n"
        "  const t = await r.json();\n"
        "  if(r.ok){ document.getElementById('msg').innerText = '登录成功，您可以返回电脑端继续'; }\n"
        "  else{ document.getElementById('msg').innerText = '登录失败：'+(t.detail||r.status); }\n"
        "}\n"
        "</script>\n"
        "</body></html>"
    )
    return HTMLResponse(html)

# 扫码登录：前端轮询
@router.get("/wechat/poll")
def wechat_poll(scene: str):
    info = SCENES.get(scene)
    if not info:
        raise HTTPException(status_code=404, detail="无效scene")
    if time.time() - info["created_at"] > 180:
        info["status"] = "expired"
    return info

# 扫码登录：模拟回调确认（占位）
@router.post("/wechat/confirm")
def wechat_confirm(scene: str):
    info = SCENES.get(scene)
    if not info:
        raise HTTPException(status_code=404, detail="无效scene")
    if info.get("status") == "expired":
        raise HTTPException(status_code=400, detail="二维码已过期")
    user_id = f"wx_{abs(hash(scene)) % 10_000_000}"
    token = f"tk_{abs(hash(user_id))}"
    SESSIONS[token] = user_id
    info.update({"status": "confirmed", "token": token, "user_id": user_id})
    return {"ok": True, "token": token, "user_id": user_id}

# 新增：查询当前登录与会员状态
class MeResponse(BaseModel):
    user_id: str
    is_member: bool

@router.get("/me", response_model=MeResponse)
def me(token: str = Query(...)):
    if token not in SESSIONS:
        raise HTTPException(status_code=401, detail="未登录或会话失效")
    user_id = SESSIONS[token]
    return MeResponse(user_id=user_id, is_member=(user_id in PAID_USERS))

@router.post("/bind")
def bind_accounts(req: BindAccountRequest, token: str):
    user_id = get_user_id(token)
    return {"ok": True, "user_id": user_id, "platform": req.platform, "uid": req.uid, "links": req.links or []}
