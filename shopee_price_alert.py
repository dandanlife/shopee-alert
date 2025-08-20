import requests
from bs4 import BeautifulSoup
import time
import os

# 1. 你的蝦皮商品網址
PRODUCT_URL = "https://tw.shp.ee/A6Wu5z3"  # ← 換成你要追蹤的商品網址

# 2. 你設定的通知價格（低於這個就會通知）
TARGET_PRICE = 39  

# 3. LINE Messaging API 的 Access Token 與你的 User ID
LINE_ACCESS_TOKEN = os.environ.get("sydVL0+IgwGHV7eO/CW/ZVRrD6KH63uV6jiL1+AZ42SNCdQkKs+LE0z4m1lzQWXL33TqqMUjUTU5XcpDiyq22HSSM7XaPE+QiMIhqrAKNiVgpNQC9gGL+u+n0w93uh/JjQFTQionITwqyw9SzmXSBwdB04t89/1O/w1cDnyilFU=")  # 從 Render 設定環境變數
USER_ID = os.environ.get("2007965855")  # 你自己的 userId

# 4. 檢查間隔時間 (秒) —— 例如 1800 = 半小時，600 = 10 分鐘
CHECK_INTERVAL = 1800  

def check_price():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(PRODUCT_URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 找商品名稱
    title = soup.find("即期-日東低咖啡因 8入").get_text(strip=True)

    # 找價格（簡單版）
    text = soup.get_text()
    price = None
    for part in text.split():
        if part.isdigit():
            price = int(part)
            break

    if price is None:
        print("❌ 沒找到價格，可能要調整解析方式")
        return

    print(f"商品：{title} | 現價：{price}")

    if price <= TARGET_PRICE:
        send_line_message(f"📢 {title} 降價啦！現在價格：{price} 元\n👉 {PRODUCT_URL}")

def send_line_message(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "to": USER_ID,
        "messages": [{"type": "text", "text": message}]
    }
    r = requests.post(url, headers=headers, json=data)
    print(f"LINE 回覆：{r.status_code}, {r.text}")

if __name__ == "__main__":
    while True:
        check_price()
        time.sleep(CHECK_INTERVAL)
