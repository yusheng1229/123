from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base  # 導入模型

# 讀取環境變數 (使用 python-dotenv)
import os
from dotenv import load_dotenv
load_dotenv()

# 資料庫連線資訊(使用 SQLite)
DATABASE_URL = os.getenv("DATABASE_URL")  # 讀取環境變數

engine = create_engine(DATABASE_URL)

# 建立資料表
Base.metadata.create_all(engine)

# 使用 session 存取資料庫
Session = sessionmaker(bind=engine)

def get_db(): # 用於建立資料庫連線，透過 with 可以自動關閉連線
    db = Session()
    try:
        yield db
    finally:
        db.close()