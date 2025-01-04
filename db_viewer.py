import sqlite3
import re  # 用於正則表達式處理資料
import csv  # 用於輸出 CSV 檔案

# 連接資料庫
conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

# 讀取資料
cursor.execute("SELECT * FROM orders")
rows = cursor.fetchall()

# 定義 CSV 檔案名稱
output_file = "processed_orders_summary.csv"

# 開啟 CSV 檔案，準備寫入
with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

    # 寫入表頭
    csv_writer.writerow(["顧客資料", "訂餐資訊", "總金額"])

    # 處理每一筆資料
    for row in rows:
        customer_data = row[1]  # 顧客資料（ID）
        order_details = row[2]  # 訂餐資訊
        total_amount = row[3]  # 總金額

        # 使用正則表達式提取幾號餐
        processed_orders = re.findall(r'(\d+號餐)', order_details)
        combined_orders = " ".join(processed_orders)  # 合併所有幾號餐成一行

        # 將處理後的結果寫入 CSV
        csv_writer.writerow([customer_data, combined_orders, f"{total_amount}元"])

# 關閉資料庫連線
conn.close()

print(f"處理完成，結果已儲存到 {output_file}")
def generate_csv():
    import sqlite3
    import re
    import csv

    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    # 讀取資料
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()

    # 定義 CSV 檔案名稱
    output_file = "processed_orders_summary.csv"

    # 開啟 CSV 檔案，準備寫入
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

        # 寫入表頭
        csv_writer.writerow(["顧客資料", "訂餐資訊", "總金額"])

        # 處理每一筆資料
        for row in rows:
            customer_data = row[1]  # 顧客資料（ID）
            order_details = row[2]  # 訂餐資訊
            total_amount = row[3]  # 總金額

            # 使用正則表達式提取幾號餐
            processed_orders = re.findall(r'(\\d+號餐)', order_details)
            combined_orders = " ".join(processed_orders)  # 合併所有幾號餐成一行

            # 將處理後的結果寫入 CSV
            csv_writer.writerow([customer_data, combined_orders, f"{total_amount}元"])

    # 關閉資料庫連線
    conn.close()