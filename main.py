from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 設定你的 Channel Secret 和 Access Token
LINE_CHANNEL_SECRET = 'd86079957d0f6e52a7b062828fa323cf'
LINE_CHANNEL_ACCESS_TOKEN = 'QpmfjEvMXdnw/kZYGXJU7FwbWidXvlRU6+a0zZVjKv8WVQP6XcpA0J7t22a60yWibLH4FEeHkegUC4uBgGh6Rl2ty73UuEshd2v7Vrt+feN3RNyp6pYxKPHgDv5IRjcL+++teLbqBAjfreeICke6JgdB04t89/1O/w1cDnyilFU='

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 定義菜單
MENU = {
    "1": "宮保雞丁",
    "2": "紅燒牛肉麵",
    "3": "清炒時蔬",
    "4": "麻婆豆腐",
    "5": "蒜泥白肉"
}

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 HTTP 請求中的簽名
    signature = request.headers['X-Line-Signature']

    # 獲取請求內容
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # 驗證簽名
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return jsonify({"message": "Invalid signature"}), 400

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()

    if user_message == "菜單":
        menu_text = "\n".join([f"{key}: {value}" for key, value in MENU.items()])
        reply = f"今天的菜單:\n{menu_text}\n請輸入編號選擇！"
    elif user_message in MENU:
        reply = f"你選擇的是{MENU[user_message]}，祝你用餐愉快！"
    else:
        reply = "請輸入 '菜單' 查看選項，或輸入正確的編號選擇菜色。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run(port=5000)
