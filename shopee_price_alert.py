import requests
from bs4 import BeautifulSoup
import os

# 1. 你的蝦皮商品網址
PRODUCT_URL = "https://tw.shp.ee/bLpZ7A6"  # ← 換成你要追蹤的商品網址

# 2. 你設定的通知價格（低於這個就會通知）
TARGET_PRICE = 39

# 3. LINE Notify Token（要先去 LINE Notify 網站申請）
LINE_NOTIFY_TOKEN = os.environ.get("LINE_NOTIFY_TOKEN")

def check_price():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(PRODUCT_URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 找商品名稱
    title = soup.find("即期-日東咖啡因 8入").get_text(strip=True)

    # 找價格（蝦皮網頁可能會變動，這裡用簡單範例，之後可調整）
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
        send_line_notify(f"📢 {title} 降價啦！現在價格：{price} 元\n👉 {PRODUCT_URL}")

def send_line_notify(message):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    data = {"message": message}
    requests.post(url, headers=headers, data=data)

if __name__ == "__main__":
    check_price()
