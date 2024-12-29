from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql+psycopg2://postgres:1111@localhost:5432/postgres"
# DATABASE_URL = "postgresql+psycopg2://postgres:1111@localhost:5432/postgres"
DATABASE_URL = "postgresql+psycopg2://postgres:1111@localhost:5432/geography1_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
