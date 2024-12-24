from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 替換為您的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = 'n5pXYs3fgqex5NYaMCGeO8Ce5UNMQYNYawfyJs1NeqBIuZR9w+gRUPuYZ8G9M2l+VaF8FTar6T8LN0dsNd3a2D7NcGMpVBuE9+4UYILHDw8LboqabOFDaK+KCqpp2PLhLRDE4Flkm6JhjAlwfciXEQdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '486f2ddeeb70a4bad71b59751df80250'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # 確認請求來自 LINE 平台
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    if event.message.text == "註冊":
        reply_text = "請提供以下註冊資料：\n1. 姓名:\n2. 電話:\n3. 電子郵件:"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入 '註冊' 來進行註冊")
        )

if __name__ == "__main__":
    app.run()