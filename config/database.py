import os
import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

engine = None
SessionLocal = None


def connect_db():
    global engine, SessionLocal

    dsn = (
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME')}"
    )

    max_retries = 5
    for i in range(1, max_retries + 1):
        try:
            engine = create_engine(dsn, pool_size=25, max_overflow=0, pool_recycle=300)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logging.info("✅ Database connected successfully")
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            return
        except Exception as e:
            logging.error(f"❌ Failed to connect to DB (attempt {i}/{max_retries}): {e}")
            time.sleep(2)

    raise RuntimeError("🚨 Could not connect to database after retries")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
