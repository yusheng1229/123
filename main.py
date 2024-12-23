from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

# 設定你的 Channel Secret 和 Access Token
LINE_CHANNEL_SECRET = '32c2c2003471e525f684fadf8f2e7966'
LINE_CHANNEL_ACCESS_TOKEN = '7gY9E2XoQ+4NnI2m7FTKRAH5O7imSfGbwoOrxqP2v9kRWDq6ULI+sVdNA0r3yWdeF9n5R17Y/51Zuhm8oGRW38kEN6pmBu+pgHZrvI4yaEdmQmtkCTW3WGgjX+u4iHd71MtCPfsuHCY/yAOtt37PoQdB04t89/1O/w1cDnyilFU='

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 替換成您的圖片直接 URL
MENU_IMAGE_URL = "https://i.imgur.com/Q1Tm4l6.png"

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
        # 回傳菜單圖片
        image_message = ImageSendMessage(
            original_content_url=MENU_IMAGE_URL,
            preview_image_url=MENU_IMAGE_URL
        )
        line_bot_api.reply_message(event.reply_token, image_message)
    else:
        reply = "請輸入 '菜單' 查看今天的菜單！"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )

if __name__ == "__main__":
    app.run(port=5000)
