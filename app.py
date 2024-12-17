from flask import Flask, request, abort, send_from_directory
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage
import os
import tempfile

# 初始化 Flask 應用程式
app = Flask(__name__)

# 設定你的 LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = 'n5pXYs3fgqex5NYaMCGeO8Ce5UNMQYNYawfyJs1NeqBIuZR9w+gRUPuYZ8G9M2l+VaF8FTar6T8LN0dsNd3a2D7NcGMpVBuE9+4UYILHDw8LboqabOFDaK+KCqpp2PLhLRDE4Flkm6JhjAlwfciXEQdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '486f2ddeeb70a4bad71b59751df80250'

# 初始化 LineBotApi 和 WebhookHandler，這些是用來處理來自 LINE 的訊息
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 設定圖像存放的資料夾
IMAGE_FOLDER = 'images'  # 設定存放上傳圖片的資料夾名稱

# 處理來自 LINE 平台的請求
@app.route("/callback", methods=['POST'])
def callback():
    # 確認請求來自 LINE 平台，並從請求的標頭取得簽名
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)  # 輸出請求的訊息

    try:
        # 驗證簽名，確保請求來自 LINE
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 如果簽名無效，回應錯誤
        abort(400)

    return 'OK'  # 請求成功時回應 'OK'

# 處理圖片請求，回傳儲存在 server 上的圖片
@app.route('/images/<filename>')
def send_image(filename):
    # 使用 Flask 的 send_from_directory 函數將圖片回傳給使用者
    return send_from_directory(IMAGE_FOLDER, filename)

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # 回傳相同的文字訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)  # 會回傳使用者發送的相同文字訊息
    )

# 處理圖片訊息
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # 取得圖片訊息的內容，這會回傳圖片的原始資料
    message_content = line_bot_api.get_message_content(event.message.id)
    
    # 將接收到的圖片儲存在暫時檔案中
    with tempfile.NamedTemporaryFile(dir=IMAGE_FOLDER, delete=False, suffix='.jpg') as tf:
        # 儲存圖片的內容到暫存檔案
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name  # 獲得儲存的檔案路徑

    # 建立圖片的 URL，這是使用 ngrok 的 URL
    image_url = f' https://8363-2402-7500-a60-c19e-d04c-8186-59d1-2afb.ngrok-free.app/images/{os.path.basename(tempfile_path)}'
    
    # 回傳相同的圖片訊息
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(
            original_content_url=image_url,  # 設定圖片的原始 URL
            preview_image_url=image_url  # 設定預覽圖片的 URL
        )
    )

# 主程式，啟動 Flask 伺服器
if __name__ == "__main__":
    # 如果 'images' 資料夾不存在，則創建它
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)
    
    # 啟動 Flask 伺服器，預設在 5000 端口上運行
    app.run()