from typing import List, Dict, Any, Optional
from datetime import datetime, date
import uuid
from sqlalchemy.orm import Session
from src.database.db import SessionLocal
from src.database.models import User, Listing, Booking, BookingMetrics, Resort

CANCELLATION_POLICY_DESCRIPTIONS = {
    "flexible": "Full refund if canceled at least 3 days before check-in.",
    "relaxed": "Full refund if canceled at least 16 days before check-in.",
    "moderate": "Full refund if canceled at least 32 days before check-in.",
    "firm": "Full refund if canceled at least 62 days before check-in.",
    "strict": "Booking is non-refundable"
}

def get_user_bookings(user_email: str, upcoming_limit: int = 3, past_limit: int = 3) -> Dict[str, Any]:
    session: Session = SessionLocal()
    try:
        today = date.today()
        bookings = (
            session.query(Booking)
            .join(User, Booking.user_id == User.id)
            .join(Listing, Booking.listing_id == Listing.id)
            .filter(User.email == user_email)
            .all()
        )

        upcoming, past = [], []
        for b in bookings:
            data = {
                "resort_name": b.listing.resort.name,
                "check_in": b.listing.check_in.strftime("%Y-%m-%d"),
                "check_out": b.listing.check_out.strftime("%Y-%m-%d"),
                "status": b.listing.status
            }
            if b.listing.check_in.date() >= today:
                upcoming.append(data)
            else:
                past.append(data)
        
        return {
            "upcoming": sorted(upcoming, key=lambda x: x["check_in"])[:upcoming_limit],
            "past": sorted(past, key=lambda x: x["check_in"], reverse=True)[:past_limit]
        }
    finally:
        session.close()

def book_resort_listing(listing_id: int, check_in: str, check_out: str, user_email: str) -> Dict[str, Any]:
    session = SessionLocal()
    try:
        listing = session.query(Listing).filter(Listing.id == listing_id, Listing.status == 'active').first()
        user = session.query(User).filter(User.email == user_email).first()
        if not listing or not user: return {"error": "Invalid listing or user"}

        booking_code = str(uuid.uuid4())[:8].upper()
        booking = Booking(
            unique_booking_code=booking_code,
            owner_id=listing.resort.creator_id,
            user_id=user.id,
            listing_id=listing_id
        )
        session.add(booking)
        session.commit()
        return {"status": "success", "booking_code": booking_code}
    except Exception as e:
        return {"error": str(e)}
    finally:
        session.close()

def get_payment_methods() -> Dict[str, Any]:
    return {
        "payment_methods": ["Credit Card", "PayPal", "Apple Pay", "Google Pay"]
    }

def get_cancellation_policy(listing_id: int = None) -> Dict[str, Any]:
    policy = "flexible" # Simplified
    return {
        "policy": policy,
        "description": CANCELLATION_POLICY_DESCRIPTIONS.get(policy)
    }
