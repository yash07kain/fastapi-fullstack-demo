from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 'engine' connects SQLAlchemy to the actual PostgreSQL database. 
# It opens connections, manages them, and sends SQL queries to the database.

db_url = "postgresql://postgres:root%401234@localhost:5432/invotrac"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
