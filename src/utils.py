import sqlite3

def delete_order(user_id):
    import sqlite3

    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    # 刪除訂單
    cursor.execute("DELETE FROM orders WHERE user_id = ?", (user_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise Exception("該用戶沒有任何訂單可刪除。")

    conn.commit()
    conn.close()