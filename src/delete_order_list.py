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

# Initialize LineBotApi with your channel access token
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

def delete_order(user_id):
    # 讀取訂單列表
    with open("order_list.json", "r", encoding="utf-8") as f:
        user_orders = json.load(f)
    
    # 建立快速清單按鈕，只顯示屬於特定 user_id 的訂單
    quick_reply_buttons = [
        QuickReplyButton(action=MessageAction(label=f"刪除訂單 {order_id}: {order['order_list']}", text=f"刪除訂單 {order_id}"))
        for order_id, order in user_orders.items() if order['user_id'] == user_id
    ]
    
    if not quick_reply_buttons:
        line_bot_api.push_message(
            user_id,
            TextSendMessage(text="目前沒有訂單可刪除。")
        )
        return
    
    # 建立快速清單
    quick_reply = QuickReply(items=quick_reply_buttons)
    
    # 發送快速清單訊息
    line_bot_api.push_message(
        user_id,
        TextSendMessage(text="請選擇要刪除的訂單：", quick_reply=quick_reply)
    )