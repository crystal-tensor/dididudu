# 统一状态（内存占位实现）
import os
from typing import Dict, Set

SESSIONS: Dict[str, str] = {}         # token -> user_id
SCENES: Dict[str, dict] = {}          # 扫码场景状态
PAID_USERS: Set[str] = set()          # 已付费会员的 user_id 集合

# 手机可访问的后端地址（用于二维码中的确认页）
PUBLIC_URL = os.getenv('BACKEND_PUBLIC_URL', 'http://localhost:8000')