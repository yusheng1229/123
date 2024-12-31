import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from linebot.models import (
    TextSendMessage, QuickReply, QuickReplyButton, MessageAction
)
from db import utils  # from db import utils 放在這裡   

# 餐點選項 (可獨立放在一個設定檔或資料庫)
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
    "13號餐 赤肉麵線羹 + 豬肉可樂餅 + 26元飲料 82 元",
    "14號餐 香檸吉司豬排堡 + 香酥米糕 + 26元飲料 99 元",
]

# 儲存用戶點餐資訊，key為用戶id, value為 list of str (選的餐點)
user_orders = {}

def handle_order(event, line_bot_api):
    user_message = event.message.text.strip()
    user_id = event.source.user_id

    if user_message.startswith("點餐"):
        # 確定頁數，預設為第一頁
        try:
            page = int(user_message.split()[1]) if len(user_message.split()) > 1 else 1
        except ValueError:
            page = 1

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
                    action=MessageAction(label="下一頁", text=f"點餐 {page + 1}")
                )
            )

        # 如果有上一頁，加入 "上一頁" 按鈕
        if page > 1:
            quick_reply_items.append(
                QuickReplyButton(
                    action=MessageAction(label="上一頁", text=f"點餐 {page - 1}")
                )
            )

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="請選擇餐點：",
                quick_reply=QuickReply(items=quick_reply_items)
            )
        )
    elif any(menu_item.startswith(user_message) for menu_item in menu_options):  # 檢查是否點餐
        # 點餐處理
        if user_id not in user_orders:
            user_orders[user_id] = []
        user_orders[user_id].append(user_message)
        reply = f"您選擇了: {user_message} \n已加入您的點餐清單，您還可以繼續點餐，或者輸入'確認' 結算"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
    elif user_message == "確認":
        on_order_confirm(event, line_bot_api, user_orders)

def on_order_confirm(event, line_bot_api, user_orders):
    print("on_order_confirm is called")
    from db import utils  # 確認有導入 utils
    user_id = event.source.user_id
    order_list = "\n".join(user_orders[user_id])
    total_price = sum(int(menu_item.split()[-2]) for menu_item in user_orders[user_id])
    utils.save_order(user_id, order_list, total_price)
    del user_orders[user_id] #清空購物車
    reply = f"您的訂單如下:\n{order_list}\n總金額：{total_price} 元\n感謝您的訂購!"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )