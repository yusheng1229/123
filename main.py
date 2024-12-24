from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction

# 設定你的 Channel Secret 和 Access Token
LINE_CHANNEL_SECRET = '32c2c2003471e525f684fadf8f2e7966'
LINE_CHANNEL_ACCESS_TOKEN = '7gY9E2XoQ+4NnI2m7FTKRAH5O7imSfGbwoOrxqP2v9kRWDq6ULI+sVdNA0r3yWdeF9n5R17Y/51Zuhm8oGRW38kEN6pmBu+pgHZrvI4yaEdmQmtkCTW3WGgjX+u4iHd71MtCPfsuHCY/yAOtt37PoQdB04t89/1O/w1cDnyilFU='

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 替換成您的圖片直接 URL
MENU_IMAGE_URL = "https://i.imgur.com/Q1Tm4l6.png"

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
        # 回傳菜單圖片
        image_message = ImageSendMessage(
            original_content_url=MENU_IMAGE_URL,
            preview_image_url=MENU_IMAGE_URL
        )
        line_bot_api.reply_message(event.reply_token, image_message)
    elif user_message == "我要點餐":
        sendButton(event)
    else:
        reply = "請輸入 '菜單' 查看今天的菜單！"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )

def sendButton(event):
    try:
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url="https://raw.githubusercontent.com/shakuneko/pic0412/main/%E6%88%91%E8%A6%81%E8%8F%9C%E5%96%AE.JPG",
                title='Menu',
                text='請問要選擇哪個套餐？',
                actions=[
                    PostbackTemplateAction(
                        label='1號餐 (赤肉麵線羹 + 脆皮炸雞 + 26元飲料) - $104',
                        text='1號餐',
                        data='action=1號餐'
                    ),
                    PostbackTemplateAction(
                        label='2號餐 (五穀瘦肉粥 + 無骨雞塊 + 26元飲料) - $97',
                        text='2號餐',
                        data='action=2號餐'
                    ),
                    PostbackTemplateAction(
                        label='3號餐 (鮮酥雞肉羹 + 黃金鮮酥雞 + 26元飲料) - $97',
                        text='3號餐',
                        data='action=3號餐'
                    ),
                    PostbackTemplateAction(
                        label='4號餐 (五穀瘦肉粥 + 脆皮炸雞 + 26元飲料) - $104',
                        text='4號餐',
                        data='action=4號餐'
                    ),
                    PostbackTemplateAction(
                        label='5號餐 (鮮脆雞腿堡 + 玉米濃湯 + 26元飲料) - $99',
                        text='5號餐',
                        data='action=5號餐'
                    ),
                    PostbackTemplateAction(
                        label='6號餐 (鮮酥雞肉羹 + 烤醬雞堡 + 26元飲料) - $103',
                        text='6號餐',
                        data='action=6號餐'
                    ),
                    PostbackTemplateAction(
                        label='7號餐 (烤醬雞堡 + 脆皮炸雞 + 26元飲料) - $107',
                        text='7號餐',
                        data='action=7號餐'
                    ),
                    PostbackTemplateAction(
                        label='8號餐 (香檸吉司豬排堡 + 脆皮炸雞 + 26元飲料) - $114',
                        text='8號餐',
                        data='action=8號餐'
                    ),
                    PostbackTemplateAction(
                        label='9號餐 (赤肉麵線羹 + 鮮脆雞腿堡 + 26元飲料) - $114',
                        text='9號餐',
                        data='action=9號餐'
                    ),
                    PostbackTemplateAction(
                        label='10號餐 (兩塊脆皮炸雞 + 26元飲料) - $108',
                        text='10號餐',
                        data='action=10號餐'
                    ),
                    PostbackTemplateAction(
                        label='11號餐 (香檸吉司豬排堡 + 無骨雞塊 + 26元飲料) - $107',
                        text='11號餐',
                        data='action=11號餐'
                    ),
                    PostbackTemplateAction(
                        label='12號餐 (五穀瘦肉粥 + 黃金鮮酥雞 + 26元飲料) - $94',
                        text='12號餐',
                        data='action=12號餐'
                    ),
                    PostbackTemplateAction(
                        label='13號餐 (赤肉麵線羹 + 豬肉可樂餅) - $82',
                        text='13號餐',
                        data='action=13號餐'
                    ),
                    PostbackTemplateAction(
                        label='14號餐 (香檸吉司豬排堡 + 香酥米糕) - $99',
                        text='14號餐',
                        data='action=14號餐'
                    )
                ]
            )
        )

        line_bot_api.reply_message(event.reply_token, message)

    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'錯誤: {str(e)}'))

if __name__ == "__main__":
    app.run(port=5000)
