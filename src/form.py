import os
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 引入 order_handler 中的处理函数，如果需要
# from src.order_handler import process_order

import requests
from googleapiclient.discovery import build

# 从 .env 文件中加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 初始化 Flask 应用
app = Flask(__name__)

# 从环境变量中获取 Line Bot 的 Channel Access Token 和 Channel Secret
line_channel_access_token = os.environ.get("7gY9E2XoQ+4NnI2m7FTKRAH5O7imSfGbwoOrxqP2v9kRWDq6ULI+sVdNA0r3yWdeF9n5R17Y/51Zuhm8oGRW38kEN6pmcm QdB04t89/1O/w1cDnyilFU=")
line_channel_secret = os.environ.get("32c2c2003471e525f684fadf8f2e7966")

# 初始化 LineBotApi 和 WebhookHandler
if line_channel_access_token is None or line_channel_secret is None:
   print("ERROR! Missing the linebot tokens")
   exit()
line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)

# 配置 Google 表单的链接
# 如果需要从后台获取数据，请配置 Google API
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSePtdHuG2e8dwlzwcBakUnZ9SKRZHV7lbmfZF8urE49lAIXgg/viewform?usp=dialog"

GOOGLE_API_KEY = os.environ.get("AIzaSyCW8hz35BYMDlxxsp96X5K-4XBjN7XvQtw")
GOOGLE_API_DISCOVERY_URL = (
    "https://forms.googleapis.com/$discovery/rest?version=v1"
)

# 如果需要从后台获取数据
# 初始化 Google Form API
if GOOGLE_API_KEY is None:
    print("ERROR! Missing google api key")
    service = None
else:
    service = build(
        "forms",
        "v1",
        discoveryServiceUrl=GOOGLE_API_DISCOVERY_URL,
        developerKey=GOOGLE_API_KEY,
    )



@app.route("/callback", methods=['POST'])
def callback():
    # 获取 X-Line-Signature 头信息
    signature = request.headers['X-Line-Signature']
    # 获取请求体
    body = request.get_data(as_text=True)

    # 处理签名验证和消息
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # 在这里处理用户输入
    if user_message.startswith("提交订单"):
        # 调用Google表单API处理订单信息
        try:
            # 在这里模拟从 Google 表单获取数据
            form_data = fetch_google_form_data()
            
            # 解析表单数据，提取所需的信息
            # 如果使用google-api-python-client, 请参考google api文档
            
            # 使用 order_handler 中的函数处理订单（如果使用方案一）
            # order_data = process_order(user_message, form_data)
            
            # 构造回复消息
            reply_message = f"订单已提交，信息： {form_data}"
            
        except Exception as e:
           reply_message = f"提交订单失败，请稍后再试. error: {e}"
           
    
    else:
        reply_message = "您好，请使用\"提交订单\"指令进行订单提交"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

def fetch_google_form_data():
     #  使用requests库向 Google 表单的 URL 发送 POST 请求。
     # 你需要解析 Google 表单的数据，获取需要的字段信息。
     # 返回的数据类型根据情况而定，可以是字典、列表等等
    
     # 以下是示例
     form_data = {
        "item1": "example item",
        "item2": "example item2",
        "address": "example address"
     }
     
     # 如果使用 google-api-python-client，可以使用下面的例子
     # if service is not None:
     #   forms = service.forms().get(formId=GOOGLE_FORM_ID).execute()
     #   response = service.forms().responses().list(formId=GOOGLE_FORM_ID).execute()

     return form_data

if __name__ == "__main__":
    app.run(debug=True, port=5000)