from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
)

# 設定你的 Channel Secret 和 Access Token
LINE_CHANNEL_SECRET = 'd86079957d0f6e52a7b062828fa323cf'
LINE_CHANNEL_ACCESS_TOKEN = 'QpmfjEvMXdnw/kZYGXJU7FwbWidXvlRU6+a0zZVjKv8WVQP6XcpA0J7t22a60yWibLH4FEeHkegUC4uBgGh6Rl2ty73UuEshd2v7Vrt+feN3RNyp6pYxKPHgDv5IRjcL+++teLbqBAjfreeICke6JgdB04t89/1O/w1cDnyilFU='

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
        # 提示用戶輸入 "我要點餐"
        reply = "輸入 '我要點餐' 查看餐點選項！"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
    elif user_message.startswith("我要點餐"):
        # 確定頁數，預設為第一頁
        try:
            page = int(user_message.split()[1]) if len(user_message.split()) > 1 else 1
        except ValueError:
            page = 1

        # 餐點選項
        menu_options = [
            "1號餐 赤肉麵線羹 + 脆皮炸雞 + 26元飲料 104 元",
            "2號餐 五穀瘦肉粥 + 無骨雞塊 + 26元飲料 97 元",
            "3號餐 鮮酥雞肉羹 + 黃金鮮酥雞 + 26元飲料 97 元",
            "4號餐 五穀瘦肉粥 + 脆皮炸雞 + 26元飲料 104 元",
            "5號餐 鮮脆雞腿堡 + 玉米濃湯 + 26元飲料 99 元",
            "6號餐 鮮酥雞肉羹 + 烤醬雞堡 + 26元飲料 103 元",
            "7號餐 烤醬雞堡 + 脆皮炸雞 + 26元飲料 107 元",
            "8號餐 香檸吉司豬排堡 + 脆皮炸雞 + 26元飲料 114 元",
            "9號餐 赤肉麵線羹 + 鮮脆雞腿堡 + 26元飲料 114 元",
            "10號餐 兩塊脆皮炸雞(腿/雞塊任選) + 26元飲料 108 元",
            "11號餐 香檸吉司豬排堡 + 無骨雞塊(5入) + 26元飲料 107 元",
            "12號餐 五穀瘦肉粥 + 黃金鮮酥雞 + 26元飲料 94 元",
            "13號餐 赤肉麵線羹 + 豬肉可樂餅 82 元",
            "14號餐 香檸吉司豬排堡 + 香酥米糕 99 元",
        ]

        # 分頁顯示，每頁最多顯示 7 個選項
        items_per_page = 7
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        menu_group = menu_options[start_idx:end_idx]

        # 建立 QuickReply 按鈕
        quick_reply_items = []
        for option in menu_group:
            quick_reply_items.append(
                QuickReplyButton(
                    action=MessageAction(label=option.split()[0], text=option)
                )
            )

        # 如果還有下一頁，加入 "下一頁" 按鈕
        if end_idx < len(menu_options):
            quick_reply_items.append(
                QuickReplyButton(
                    action=MessageAction(label="下一頁", text=f"我要點餐 {page + 1}")
                )
            )

        # 如果有上一頁，加入 "上一頁" 按鈕
        if page > 1:
            quick_reply_items.append(
                QuickReplyButton(
                    action=MessageAction(label="上一頁", text=f"我要點餐 {page - 1}")
                )
            )

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="請選擇餐點：",
                quick_reply=QuickReply(items=quick_reply_items)
            )
        )
    else:
        reply = "請輸入 '菜單' 或 '我要點餐' 查看選項！"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )

if __name__ == "__main__":
    app.run(port=5000)