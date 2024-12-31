from linebot import LineBotApi
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, URIAction

# 替換為您的 Channel Access Token
LINE_CHANNEL_ACCESS_TOKEN = 'n5pXYs3fgqex5NYaMCGeO8Ce5UNMQYNYawfyJs1NeqBIuZR9w+gRUPuYZ8G9M2l+VaF8FTar6T8LN0dsNd3a2D7NcGMpVBuE9+4UYILHDw8LboqabOFDaK+KCqpp2PLhLRDE4Flkm6JhjAlwfciXEQdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# 建立圖文選單
rich_menu_to_create = RichMenu(
    size={"width": 2500, "height": 843},  # 圖文選單的大小
    selected=True,
    name="功能表",  # 圖文選單的名稱
    chat_bar_text="功能表",  # 用戶點擊時顯示的文字
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=833, height=562),
            action=URIAction(label='註冊', text='請輸入班級暱稱(ex.智商二甲 小明):')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=833, y=0, width=834, height=562),
            action=URIAction(label='菜單',text='請查收今日菜單！')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1667, y=0, width=833, height=562),
            action=URIAction(label='查詢今日訂購',text='開發中...')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=562, width=2500, height=281),
            action=URIAction(label='意見回饋',uri='https://forms.gle/your-google-form-link')
        )
    ]
)

# 創建圖文選單
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

image_path = './rich_menu_image.jpg'
# 上傳圖文選單圖片
with open("C:/Users/VivoBook/123/line bot/photo.png", "rb") as image_file:

    line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", image_file)

# 將圖文選單與用戶綁定
line_bot_api.set_default_rich_menu(rich_menu_id)