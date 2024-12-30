from linebot import LineBotApi
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, URIAction

# 替換為您的 Channel Access Token
LINE_CHANNEL_ACCESS_TOKEN = 'ACCESS_TOKEN'
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# 建立圖文選單
rich_menu_to_create = RichMenu(
    size={"width": 2500, "height": 843},  # 圖文選單的大小
    selected=True,
    name="功能表",  # 圖文選單的名稱
    chat_bar_text="功能表",  # 用戶點擊時顯示的文字
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
            action=URIAction(label='註冊', uri='https://example.com/register')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
            action=URIAction(label='菜單', uri='https://example.com/menu')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1666, y=0, width=833, height=843),
            action=URIAction(label='查詢今日訂購', uri='https://example.com/orders')
        )
    ]
)

# 創建圖文選單
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

image_path = './rich_menu_image.jpg'
# 上傳圖文選單圖片
with open("C:\\Users\\10606\\tmp\\tmp\\rr\\123\\line bot\\rich_menu_image.png", "rb") as image_file:

    line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", image_file)

# 將圖文選單與用戶綁定
line_bot_api.set_default_rich_menu(rich_menu_id)