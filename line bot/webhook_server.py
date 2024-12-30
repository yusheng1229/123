from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 替換為您的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('hupMUv7FAv7HW0mIm+CzvQtCB7t10ZFi+JMQAubqklCZnTtZoIxA1wudSacAgiHBF9v98j6BKObZMffLKRlheKDV0SPDL56KiEXji2he83zKS+TVQgEflZOLTwuvVIGimPKCItVEbM9y1ZHA/e+SJwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4152e6ede6c93c0d8f68280c67149709')

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 X-Line-Signature
    signature = request.headers['X-Line-Signature']

    # 獲取請求體
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text

    if "請輸入班級暱稱(ex.智商二甲 小明):" in user_input:
        # 用戶輸入後的處理邏輯
        reply_text = f"收到！您的註冊資料是：{user_input}"
        print(f"用戶註冊資料：{user_input}")  # 在終端機顯示
        # 傳回確認訊息給用戶
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
    else:
        # 處理其他訊息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請點選功能表上的選項進行操作！")
        )

if __name__ == "__main__":
    app.run(port=8000)
