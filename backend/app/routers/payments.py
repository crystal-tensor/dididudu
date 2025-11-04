from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal

router = APIRouter()

PricingType = Literal["single", "monthly", "quarterly", "yearly"]

PRICES = {
    "single": 9.9,
    "monthly": 19.9,
    "quarterly": 29.9,
    "yearly": 39.9,
}

class OrderRequest(BaseModel):
    plan: PricingType
    channel: Literal["wechat", "alipay"]

@router.post("/order")
def create_order(req: OrderRequest):
    if req.plan not in PRICES:
        raise HTTPException(status_code=400, detail="不支持的套餐")
    # 占位返回：生产应创建支付链接或二维码
    return {
        "order_id": f"ord_{req.plan}",
        "amount": PRICES[req.plan],
        "channel": req.channel,
        "pay_qr": f"mock://{req.channel}/{req.plan}/{PRICES[req.plan]}",
    }

@router.get("/order/{order_id}")
def query_order(order_id: str):
    # 占位：生产应查询支付状态
    return {"order_id": order_id, "status": "PAID"}

# 新增：激活当前登录用户为会员（占位）
from ..state import SESSIONS, PAID_USERS

@router.post("/activate")
def activate_membership(token: str):
    if token not in SESSIONS:
        raise HTTPException(status_code=401, detail="未登录或会话失效")
    user_id = SESSIONS[token]
    PAID_USERS.add(user_id)
    return {"ok": True, "user_id": user_id, "is_member": True}
