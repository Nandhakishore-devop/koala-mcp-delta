from typing import List, Dict, Any, Optional
from sqlalchemy import text
from src.database.db import SessionLocal, engine
from src.database.models import User, Booking, Resort

def get_user_profile(user_email: str) -> Dict[str, Any]:
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == user_email, User.has_deleted == 0).first()
        if not user:
            return {"error": f"User {user_email} not found"}
        
        bookings_count = session.query(Booking).filter(Booking.user_id == user.id).count()
        resorts_count = session.query(Resort).filter(Resort.creator_id == user.id, Resort.has_deleted == 0).count()
        
        return {
            "name": f"{user.first_name} {user.last_name}",
            "email": user.email,
            "status": user.status,
            "total_bookings": bookings_count,
            "created_resorts": resorts_count
        }
    finally:
        session.close()

def test_database_connection() -> Dict[str, Any]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "success", "message": "Connection healthy"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
