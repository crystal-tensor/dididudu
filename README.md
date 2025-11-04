<<<<<<< HEAD
# dididudu
=======
# UP主竞争分析平台

一个面向 Bilibili/小红书/抖音创作者的专业分析平台：
- 微信注册登录（占位接口，可对接 code2session）
- 输入自己的账号与 1-3 个竞品 UID/链接，一键生成分析
- 报告前 2 页免费，更多页需购买（单次或会员）
- 会员计费：单次 ¥9.9；包月 ¥19.9；包季 ¥29.9；包年 ¥39.9

## 目录结构
- backend/ FastAPI 后端
- frontend/ 静态前端页面
- example.py 收集/汇总数据（示例）
- report3.py 生成图表与报告（已支持 EXPORT_DIR 导出）
- bilibili_up_videos.csv 示例数据

## 运行
1. 安装依赖（不使用虚拟环境）
```bash
pip3 install -r /Users/danielcrystal/work/dididudu/requirements.txt
```
2. 启动后端
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
3. 打开前端
- 用浏览器直接打开 `frontend/index.html`
- 或用任意静态服务器托管 `frontend/`

> 注意：前端调用的是 `/api/*` 路径，开发环境下请通过浏览器插件或本地代理将前端请求代理到 `http://localhost:8000`。

## 关键端点
- `POST /api/auth/wechat/login` 微信登录占位，返回 token 与 user_id
- `POST /api/analysis/run` 触发分析（platform/user_uid/competitor_uids/competitor_links）
- `GET /api/reports/list?user_id=xxx` 列出报告
- `GET /api/reports/{user_id}/{job_id}/page/{n}` 获取第 n 页（1-2 免费，>2 返回402）
- `POST /api/payments/order` 创建订单（single/monthly/quarterly/yearly + wechat/alipay）

## 报告导出
- 后端运行器会以环境变量 `EXPORT_DIR` 调用 `report3.py`，将图片导出到：
  `/Users/danielcrystal/work/dididudu/reports/{user}/{job_id}/page_{n}.png`

## 接入建议（生产）
- 认证：接入微信小程序或公众号 `code2session`，并使用JWT + Redis维护会话
- 数据：将 `example.py` 改造成接受平台与UID/链接的参数化脚本或Python模块
- 存储：使用PostgreSQL/MySQL记录用户、订单、会员权益；对象存储保存报告图片
- 支付：接入微信/支付宝官方SDK，异步通知更新订单状态与会员权益
- 前端：可升级为 Next.js/Tailwind/Ant Design 的SPA，使用OAuth/扫码登录
>>>>>>> 723424d (feat: initial push of dididudu project)
