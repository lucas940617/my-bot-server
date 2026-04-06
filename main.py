from fastapi import FastAPI

# 建立一個 FastAPI 應用程式實例
app = FastAPI()

# 建立一個讓 UptimeRobot 每 10 分鐘來敲門的「根目錄」網址
@app.get("/")
def read_root():
    return {"status": "成功！", "message": "機器人伺服器已清醒，隨時準備接單！"}

# 預留給聊天軟體 (Telegram/Discord) 傳送訊息過來的 Webhook 接收器
@app.post("/webhook")
def receive_message():
    # 之後我們會在這裡寫入接收訊息與驗證的邏輯
    return {"message": "已收到 Webhook 訊號"}