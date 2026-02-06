from typing import List, Dict, Any, Optional
from sqlalchemy import text
from src.database.db import SessionLocal, engine

def test_database_connection() -> Dict[str, Any]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "success", "message": "Connection healthy"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
