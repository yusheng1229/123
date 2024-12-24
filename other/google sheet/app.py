from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent, ButtonsTemplate, TemplateSendMessage
import os
import json
from flask import Flask, request, abort

app = Flask(__name__)

# LINE Bot credentials
LINE_CHANNEL_SECRET = 'Channel secret'
LINE_CHANNEL_ACCESS_TOKEN = 'n5pXYs3fgqex5NYaMCGeO8Ce5UNMQYNYawfyJs1NeqBIuZR9w+gRUPuYZ8G9M2l+VaF8FTar6T8LN0dsNd3a2D7NcGMpVBuE9+4UYILHDw8LboqabOFDaK+KCqpp2PLhLRDE4Flkm6JhjAlwfciXEQdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 處理Webhook
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print(e)
        abort(400)

    return 'OK'

# 當使用者發送訊息時觸發
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text

    # 判斷用戶是否需要新增商品
    if text.lower() == '新增商品':
        # 顯示商品新增選單
        buttons_template = ButtonsTemplate(
            title="新增商品", text="請選擇商品資訊", actions=[
                {
                    "type": "postback",
                    "label": "輸入商品名稱",
                    "data": "input_name"
                },
                {
                    "type": "postback",
                    "label": "輸入商品數量",
                    "data": "input_quantity"
                },
                {
                    "type": "postback",
                    "label": "輸入商品價格",
                    "data": "input_price"
                }
            ]
        )
        template_message = TemplateSendMessage(alt_text='新增商品選單', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    else:
        # 處理其他訊息
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入'新增商品'來開始新增商品。"))

def get_product_info(product_name_or_id):
    # 讀取商品資料表（Sheet2）
    result = service.spreadsheets().values().get(
        spreadsheetId='1kaQusbNBN4RmzzhmtYC8djQZN7w8n4TmCLZDLDeoRCE', range="菜單!A:C").execute()
    values = result.get('values', [])
    
    # 從第二行開始查找商品ID或商品名稱對應的價格
    for row in values[1:]:
        if row[1] == product_name_or_id or row[0] == product_name_or_id:
            return {"id": row[0], "name": row[1], "price": float(row[2])}
    return None  # 如果找不到對應商品，返回 None


if __name__ == "__main__":
    app.run(debug=True)
