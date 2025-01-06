# 訂餐系統 (Order System)

## 簡介

這個專案是一個基於 Python 的訂餐系統，它透過 Line Bot 介面與使用者互動，讓使用者可以方便地點餐、查看訂單和取消訂單。

## 主要功能

*   **菜單瀏覽**: 使用者可以透過 Line Bot 輸入 "菜單" 來查看餐點圖片。
*   **點餐功能**: 使用者可以輸入 "點餐" 開始點餐，並瀏覽分頁的餐點選項。
*   **訂單確認**: 使用者可以選擇餐點後輸入 "確認" 來完成訂單。
*   **訂單取消**: 使用者可以輸入 "取消訂餐" 來刪除指定訂單。
*   **訂單管理**: 使用者可以查看自己的訂單列表並選擇要刪除的訂單。
*   **訂單資料輸出**: 管理者可以透過執行 `db_viewer.py` 腳本將訂單資料匯出到 CSV 檔案。

## 技術棧

*   **程式語言**: Python
*   **Web 框架**: Flask
*   **Line Bot API**: 使用 Line Bot SDK 與 Line Bot 互動
*   **資料庫**: SQLite (使用 SQLAlchemy ORM)
*   **JSON**: 使用 JSON 檔案儲存訂單列表

## 專案架構
123/  
├── .git/  
├── db/  
│ ├── init.py  
│ ├── database.py  
│ ├── models.py  
│ └── utils.py  
├── docs/  
├── line bot/  
├── other/  
├── src/  
│ ├── pycache/  
│ ├── main.py   
│ ├── order_handler.py  
│ └── utils.py     
├── venv/       
├── .env        
├── .env.example      
├── .gitignore      
├── db_viewer.py        
├── delete_order_list.py     
├── order_list.json     
├── orders.db   
├── ordersystem-dev-log.md  
├── q.txt   
├── README.md   
└── requirements.txt    

*   `db/`: 包含資料庫相關程式碼。
    *   `database.py`: 資料庫連線設定、session 管理。
    *   `models.py`: 資料庫模型 (Order)。
    *   `utils.py`: 資料庫操作函式 (CRUD)。
*   `src/`: 包含主要程式碼。
    *   `main.py`: Flask 應用程式入口點，Line Bot webhook 處理。
    *   `order_handler.py`: 處理訂餐邏輯。
    *   `utils.py`: 共用的工具函式。
*   `db_viewer.py`: 將訂單資料匯出到 CSV 檔案。
*   `order_list.json`: 儲存訂單列表。
*   `orders.db`: SQLite 資料庫檔案。
*   `requirements.txt`: 專案套件列表。
*   `.env`: 環境變數檔案。
*   `.env.example`: 環境變數範例。

## 環境設定

1.  **安裝 Python 和 Pip**: 確保你的電腦安裝了 Python 和 Pip。
2.  **建立虛擬環境**: 建議使用虛擬環境來管理專案套件。

    ```bash
    python -m venv venv
    ```

3.  **啟用虛擬環境**:
    *   **Windows**:

        ```bash
        venv\Scripts\activate
        ```
    *   **macOS/Linux**:

        ```bash
        source venv/bin/activate
        ```

4.  **安裝套件**: 使用 pip 安裝專案需要的套件。

    ```bash
    pip install -r requirements.txt
    ```

5.  **設定環境變數**: 建立 `.env` 檔案，並設定以下環境變數：

    ```env
    LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
    LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN
    image_url=YOUR_MENU_IMAGE_URL
    DATABASE_URL=sqlite:///orders.db
    ```

    *   `LINE_CHANNEL_SECRET`: Line Bot 的 Channel Secret。
    *   `LINE_CHANNEL_ACCESS_TOKEN`: Line Bot 的 Channel Access Token。
    *   `image_url`: 菜單圖片的 URL。
    *   `DATABASE_URL`: SQLite 資料庫的路徑。

## 如何執行

1.  **啟動 Flask 應用程式**:

    ```bash
    python src/main.py
    ```

2.  **設定 Line Bot webhook**: 將 Line Bot 的 webhook 設定為你的應用程式的 `/callback` 端點。
3.  **開始使用**: 在 Line App 中與你的 Line Bot 互動。

## 開發輔助工具

*   **GitHub**: 用於版本控制和協作。
*   **PowerShell**: 用於執行命令和指令碼。

## 注意事項

*   這個專案使用 SQLite 資料庫，資料會儲存在 `orders.db` 檔案中。
*   請確保你的 Line Bot 設定正確，且 webhook 設定正確。

## 貢獻

魚湯、星辰、yusheng、韶、宣妤


