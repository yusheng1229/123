from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# 1. 設定憑證檔案路徑
SERVICE_ACCOUNT_FILE = 'googlesheet金鑰/ace-well-445415-m5-ba9b887e2759.json'  # 替換成你的 JSON 檔案名稱
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# 2. 建立憑證
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# 3. 連接 Google Sheets API
service = build('sheets', 'v4', credentials=creds)

# 4. Google Sheets 文件 ID
SPREADSHEET_ID = '1kaQusbNBN4RmzzhmtYC8djQZN7w8n4TmCLZDLDeoRCE'  # 替換成你的 Google Sheets 文件 ID
RANGE_NAME = '訂單!A1:F2'  # 替換成目標範圍

# 5. 讀取數據
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

if not values:
    print('No data found.')
else:
    print('Data from Google Sheets:')
    for row in values:
        print(row)

# 6. 寫入數據
write_body = {
    'values': [
        ['D02', '小華', '炸雞', '3', '210', '未處理'],
        ['D03', '小明', '薯條', '2', '80', '已處理']
    ]
}
service.spreadsheets().values().append(
    spreadsheetId=SPREADSHEET_ID,
    range='訂單!A3:F2',
    valueInputOption='RAW',
    body=write_body
).execute()
print('Data written successfully.')
