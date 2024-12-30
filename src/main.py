from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction,
    ImageSendMessage
)
from order_handler import handle_order, menu_options  # 導入 handle_order 和 menu_options

# 設定你的 Channel Secret 和 Access Token
LINE_CHANNEL_SECRET = '32c2c2003471e525f684fadf8f2e7966'
LINE_CHANNEL_ACCESS_TOKEN = '7gY9E2XoQ+4NnI2m7FTKRAH5O7imSfGbwoOrxqP2v9kRWDq6ULI+sVdNA0r3yWdeF9n5R17Y/51Zuhm8oGRW38kEN6pmBu+pgHZrvI4yaEdmQmtkCTW3WGgjX+u4iHd71MtCPfsuHCY/yAOtt37PoQdB04t89/1O/w1cDnyilFU='

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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
        # 回傳圖片訊息
        image_url = "https://i.imgur.com/Q1Tm4l6.jpeg"  # 直接使用圖片網址
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
        )
    elif (
        user_message.startswith("點餐")
        or any(menu_item.startswith(user_message) for menu_item in menu_options)
        or user_message == "確認"
    ):
        # 將點餐相關的訊息轉交給 order_handler
        handle_order(event, line_bot_api)
    else:
        reply = "請輸入 '菜單' 或 '點餐' 查看選項！"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    app.run(port=5000)