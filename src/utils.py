import sqlite3
from db.database import get_connection

def create_user(user_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (user_id, name, email, phone) VALUES (?, ?, ?, ?)",
        (user_data['user_id'], user_data['name'], user_data['email'], user_data['phone'])
    )
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return dict(user)
    else:
        return None

def delete_order(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE user_id = ?", (user_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise Exception("該用戶沒有任何訂單可刪除。")
    
    conn.commit()
    conn.close()