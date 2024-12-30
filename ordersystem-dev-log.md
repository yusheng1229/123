# LINE Bot 訂餐系統開發日誌

這是一個使用 Python 開發的 LINE Bot 訂餐系統，可以讓使用者透過 LINE 聊天機器人查看菜單、點餐、確認訂單。

## 2024-12-24
*   ### 修改專案架構
    * 修改專案結構。
## 2024-12-24
*   ### 製作圖文表單的圖片
    * 製作三個功能表單的按鈕
    * 放到的line bot的程式碼上傳到機器人

## 2024-12-29
*   ### 點餐功能遷移
    * 將點餐功能從 main 移至 order_handler。
    * 建立 db 資料夾。
## 2024-12-29
*   ### 修改圖文表單的圖片
    * 修改之前的圖片
    * 更改按鈕的排版以及尺寸
    * 嘗試上傳到機器人

## 2024-12-30
*   ### 資料庫系統
    *  建立資料庫系統，建立資料庫檔案( orders.db )
    *  建立 `db/models.py` 資料庫模型檔案。
    *  建立 `db/utils.py` 資料庫存取函數檔案。
    *  使用 `python-dotenv` 讀取環境變數。
    *   ### 程式碼修改
    *  修改 `order_handler.py`，使訂單資料可以儲存到資料庫。
    *  解決 `NameError: name 'order_handler' is not defined`
    *  解決 `ModuleNotFoundError: No module named 'db'` ，使用 `__init__.py` 檔案使 Python 正確讀取。
    *  解決 `ModuleNotFoundError: No module named 'db'`， 使用 `sys.path.append()` 強制加入搜尋路徑。
    *  ### 環境設定
    *  使用 Windows 的虛擬環境啟動指令 `venv\Scripts\activate`。
    * 使用 `Set-ExecutionPolicy` 確保 PowerShell 執行權限正確。
*  ### 資料庫操作
    * 撰寫資料庫查看程式碼 `db_viewer.py`
    * 使用 `db_viewer.py` 來檢查、驗證、刪除資料。
*  ### GitHub 設定
    * 設定 `.gitignore` 檔案，忽略敏感資料。
## 2024-12-31
 *   修正錯誤。
 *   確認程式碼可正常運行。


## 遇到的問題和解決方案：
 *   **2024-12-29**
    *  問題：出現 `NameError: name 'order_handler' is not defined` 的錯誤。
    *  解決方案： 在 `main.py` 中，正確導入了 `menu_options`。
    *  問題:圖片上傳不成功，訊息顯示找不到路徑
    *  解決方案:重改路徑，將此路徑`path/to/your/rich_menu_image.jpg"更改成"C:/Users/10606/Pictures/rich_menu_image.jpg`, `rb`
       並且確保程式擁有檔案的讀取權限。 
*   **2024-12-30**
    *  問題：出現 `ModuleNotFoundError: No module named 'db'` 的錯誤。
*   解決方案： 在 `db` 資料夾中建立了 `__init__.py` 檔案。
    * 問題:圖片在圖文選單裡，按鈕的比例怪
    * 解決方案:更改按鈕比例，也修改圖文選單尺寸大小。
      
*  **2024-12-31**
    *  問題：出現 `ModuleNotFoundError: No module named 'db'` 的錯誤，即使建立了 `__init__.py`。
    *  解決方案： 使用 `sys.path.append()` 強制加入搜尋路徑。
    *  問題：PowerShell 無法辨識 `source venv/bin/activate` 指令，無法啟動虛擬環境
    * 解決方案：設定 PowerShell 的執行原則，使用 Windows 版本的虛擬環境啟動指令 `venv\Scripts\activate`。
    
      

    
      

* **其他問題**
    * 問題：
    * 解決方案：

## 未來規劃：
*   加入錯誤處理。
*   加入取消訂單功能。
*   加入圖文訊息介面。
*   部署到雲端。
