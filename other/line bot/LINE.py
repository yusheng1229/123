from linebot import LineBotApi
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, RichMenuSize, URIAction

# 初始化 LineBotApi
line_bot_api = LineBotApi('n5pXYs3fgqex5NYaMCGeO8Ce5UNMQYNYawfyJs1NeqBIuZR9w+gRUPuYZ8G9M2l+VaF8FTar6T8LN0dsNd3a2D7NcGMpVBuE9+4UYILHDw8LboqabOFDaK+KCqpp2PLhLRDE4Flkm6JhjAlwfciXEQdB04t89/1O/w1cDnyilFU=')

# Step 1: 定義圖文選單
rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=2500, height=843),  # 圖文選單的尺寸
    selected=False,  # 預設是否啟用
    name="功能表",  # 功能表名稱
    chat_bar_text="點擊開啟選單",  # 顯示於聊天視窗下方的文字
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=281),  # 第一個按鈕範圍
            action=URIAction(label='註冊', uri='https://example.com/register')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=281, width=2500, height=562),  # 第二個按鈕範圍
            action=URIAction(label='菜單', uri='https://example.com/menu')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=562, width=2500, height=843),  # 第三個按鈕範圍
            action=URIAction(label='線上取餐', uri='https://example.com/order')
        ),
    ]
)

# 創建圖文選單
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
print("Rich Menu ID:", rich_menu_id)

# Step 2: 上傳圖片作為功能表背景
image_path = '/mnt/data/前端line bot 功能表圖片.png'  # 替換為您上傳的圖片路徑
with open(image_path, 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

print("圖片已成功上傳到圖文選單！")
