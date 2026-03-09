from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="シフト管理システム")

# セッション（管理者ログイン用）
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "changeme"))

# 静的ファイル・テンプレート
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# --- ルーター登録（後でファイルを追加していく）---
# from app.routers import public, form, admin
# app.include_router(public.router)
# app.include_router(form.router)
# app.include_router(admin.router)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("public/index.html", {"request": request})


@app.get("/health")
async def health():
    """Koyebのヘルスチェック用"""
    return {"status": "ok"}
