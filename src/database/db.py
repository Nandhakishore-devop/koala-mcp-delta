import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

def get_database_url():
    """Get database URL from environment variables."""
    host = os.getenv("MYSQL_HOST", "localhost")
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "koala_dev")
    
    if password:
        return f"mysql+pymysql://{user}:{password}@{host}/{database}"
    else:
        return f"mysql+pymysql://{user}@{host}/{database}"

DATABASE_URL = get_database_url()
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_recycle=3600,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def initialize_database():
    """Run once at startup to verify DB connection."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False
