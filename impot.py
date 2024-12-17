import requests
import json
import pandas as pd

# 发送HTTP GET请求
url = 'https://apis.youbike.com.tw/json/station-yb2.json'
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    data = response.json()  # 解析JSON数据
    # 以JSON格式写入文件
    with open('youbike.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print("数据已成功保存到本地")
else:
    print(f"请求失败，状态码：{response.status_code}")

# 讀取 JSON 檔案
df = pd.read_json('youbike.json')


print(df.head())


    