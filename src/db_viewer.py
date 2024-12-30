import sqlite3

conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

# 刪除單筆資料
def delete_order_by_user_id(user_id):
    try:
        cursor.execute("DELETE FROM orders WHERE user_id = ?", (user_id,))
        conn.commit()  # 提交變更
        print(f"已刪除 user_id 為 '{user_id}' 的資料")
    except sqlite3.Error as e:
        print(f"刪除資料時發生錯誤: {e}")

# 讀取資料(方便查看資料)
cursor.execute("SELECT * FROM orders")
rows = cursor.fetchall()
for row in rows:
    print(row)


#刪除&查看資料
# 測試刪除，先用使用者ID為 "user123" 測試
# delete_order_by_user_id("U7e8deabe3ab7de7c661b9f662b281832")

# 讀取資料(方便查看是否刪除成功)
# cursor.execute("SELECT * FROM orders")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)


conn.close()