import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow

app = FastAPI()

# 這裡的資料會從 Render 的環境變數讀取，保護隱私
CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI") # 例如 https://xxx.onrender.com/auth/callback

# Google 要求的權限範圍：日曆讀寫
SCOPES = ['https://www.googleapis.com/auth/calendar']

@app.get("/")
def home():
    return {"status": "running", "msg": "請訪問 /login 開始登入流程"}

# 1. 引導使用者去 Google 登入
@app.get("/login")
def login():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    
    # access_type="offline" 才能拿到「永久鑰匙 (Refresh Token)」
    # prompt="consent" 確保每次都會跳出授權畫面
    auth_url, _ = flow.authorization_url(access_type='offline', prompt='consent')
    return RedirectResponse(auth_url)

# 2. 接收 Google 回傳的 Code 並換成 Token
@app.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    flow.fetch_token(code=code)
    
    credentials = flow.credentials
    
    # 這就是我們夢寐以求的「永久鑰匙」！
    refresh_token = credentials.refresh_token
    
    # 這裡暫時先顯示在網頁上，之後我們要把它存進資料庫
    return {
        "message": "登入成功！",
        "refresh_token": refresh_token,
        "note": "請妥善保存這串 Refresh Token，這是幫你操作日曆的鑰匙。"
    }
