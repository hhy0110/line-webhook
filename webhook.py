from flask import Flask, request
import requests
import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

REPLY_MESSAGE = """哈囉
很開心你又回來紀錄情緒啦～
來說說現在的心情如何吧～

基本情緒：喜悅/悲傷/憤怒/恐懼/厭惡/驚訝
復合情緒：樂觀/幸福/服從/失望/鄙視/自責/羞愧/羨慕/嫉妒/懷舊/同情/焦慮/挫折/寂寞/自豪/內疚/安心/輕鬆/興奮/無聊/感激/愧疚/敬畏/開心/平淡/其他(pointing)

通過上面的參考來做選擇吧～如果沒有符合你的需求 那就選擇其他 讓我們來為你補充新選擇吧～"""

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json
    print("🔔 Webhook received:", body)

    events = body.get("events", [])
    for event in events:
        if event.get("type") == "message":
            reply_token = event["replyToken"]
            send_reply(reply_token, REPLY_MESSAGE)

    return "OK", 200

def send_reply(reply_token, message):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    body = {
        "replyToken": reply_token,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }
    response = requests.post(url, headers=headers, json=body)
    print("🔁 LINE 回應狀態碼:", response.status_code)
    print("🔁 回應內容:", response.text)

if __name__ == "__main__":
    app.run()
