from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base  # Импортируйте вашу базу, которая содержит все модели

# Укажите правильный URL для подключения к вашей базе данных
DATABASE_URL = "postgresql+psycopg2://postgres:1111@localhost:5432/geography1_db"

# Создание движка для подключения к базе данных
engine = create_engine(DATABASE_URL)

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

print("Все таблицы успешно созданы!")
