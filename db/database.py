from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base  # Import the base model
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL")


# Create the database engine
engine = create_engine(DATABASE_URL)

# Create the tables from the models
def initialize_database():
    Base.metadata.create_all(engine)


# Create session factory
Session = sessionmaker(bind=engine)


# Function to get db session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
  initialize_database()
  print("Database initialized")