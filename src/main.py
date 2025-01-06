from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction,
    ImageSendMessage
)
from order_handler import handle_order, menu_options  # 導入 handle_order 和 menu_options
import os
import json
import re


# 設定你的 Channel Secret 和 Access Token
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
image_url = os.getenv("IMAGE_URL")

#初始化 Flask 和 Line Bot API：
app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

#定義 /callback 端點：
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
#定義 /delete_order 端點：
@app.route("/delete_order", methods=['POST'])
def delete_order():
    try:
        user_id = request.json.get("user_id")
        if not user_id:
            return jsonify({"message": "User ID is required."}), 400

        # 刪除訂單
        from db import utils
        utils.delete_order(user_id)

        # 重新生成 CSV 文件
        from db_viewer import generate_csv
        generate_csv()

        return jsonify({"message": "Order deleted successfully."}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
#處理 Line Bot 訊息：
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()

    if user_message == "菜單":
        # 回傳圖片訊息  # 直接使用圖片網址
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
    elif user_message == "取消訂餐":
        try:
            user_id = event.source.user_id
            # 讀取訂單列表
            with open("order_list.json", "r", encoding="utf-8") as f:
                user_orders = json.load(f)
            print(user_orders)
            # 建立快速清單按鈕，只顯示屬於特定 user_id 的訂單
            quick_reply_buttons = [
            QuickReplyButton(action=MessageAction(label=f"刪除訂單 {order_id}", text=f"刪除訂單 {order_id}"))
            for order_id, order in user_orders.items() if order['user_id'] == user_id
            ]
            quick_reply_buttons.append(
                QuickReplyButton(action=MessageAction(label="取消", text="取消"))
            )
            # 建立快速清單
            quick_reply = QuickReply(items=quick_reply_buttons)
            text = "您的訂單如下：\n"
            for order_id, order in user_orders.items():
                if order['user_id'] != user_id:
                    continue
                else:
                    text += f"訂單編號：{order_id}\n訂單內容：{order['order_list']}\n總金額：{order['total_amount']} 元\n"
                    text += "-" * 20 + "\n"
            # 發送快速清單訊息
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"{text}請選擇要刪除的訂單：", quick_reply=quick_reply)
            )
            # # 刪除訂單邏輯
            # from db import utils
            # utils.delete_order(user_id)

            # # 重新生成 CSV 文件
            # from db_viewer import generate_csv
            # generate_csv()
            # reply = "您的訂單已刪除，感謝使用！"
            # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        except Exception as e:
            reply = f"刪除訂單失敗：{str(e)}"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
    elif re.match(r"刪除訂單 \d+", user_message):
        try:
            with open("order_list.json", "r", encoding="utf-8") as f:
                user_orders = json.load(f)
            order_id = int(user_message.split()[-1])
            order_id = str(order_id)
            del user_orders[order_id]
            with open("order_list.json", "w", encoding="utf-8") as f:
                json.dump(user_orders, f, ensure_ascii=False, indent=4)
            text = f"{user_message} 成功！"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        except Exception as e:
            reply = f"刪除訂單失敗：{str(e)}"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
    elif user_message == "取消":
        reply = "取消刪除訂單！"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
    else:
        reply = "請輸入 '菜單' 或 '點餐' 查看選項！"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    app.run(port=5000)