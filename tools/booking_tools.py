from typing import List, Dict, Any, Optional
from datetime import datetime, date
import uuid
from collections import defaultdict
from sqlalchemy.orm import Session
from src.database.db import SessionLocal
from src.database.models import User, Listing, Booking, BookingMetrics, Resort, UnitType

CANCELLATION_POLICY_DESCRIPTIONS = {
    "flexible": "Full refund if canceled at least 3 days before check-in.",
    "relaxed": "Full refund if canceled at least 16 days before check-in.",
    "moderate": "Full refund if canceled at least 32 days before check-in.",
    "firm": "Full refund if canceled at least 62 days before check-in.",
    "strict": "Booking is non-refundable"
}

def model_to_dict(model_instance):
    return {column.name: getattr(model_instance, column.name) for column in model_instance.__table__.columns}

def deduplicate_by_resort_id(listings):
    seen = set()
    unique_listings = []
    for listing in listings:
        if listing.resort_id not in seen:
            seen.add(listing.resort_id)
            unique_listings.append(listing)
    return unique_listings

def get_user_bookings(
    user_email: str,
    upcoming_limit: int = 3,
    past_limit: int = 3,
    year: int = None,
    month: int = None,
    day: int = None
) -> Dict[str, Any]:
    """
    Fetch bookings for a user by email, with optional filtering by year/month/day.
    If only the year is specified, show monthly counts if too many bookings.
    """
    session: Session = SessionLocal()

    try:
        today = date.today()

        bookings = (
            session.query(Booking)
            .join(User, Booking.user_id == User.id)
            .join(Listing, Booking.listing_id == Listing.id)
            .join(Resort, Listing.resort_id == Resort.id)
            .join(UnitType, Listing.unit_type_id == UnitType.id)
            .outerjoin(BookingMetrics, BookingMetrics.booking_id == Booking.id)  # safe outer join
            .filter(User.email == user_email)
            .filter(User.has_deleted == 0)
            .filter(Listing.has_deleted == 0)
            .filter(Resort.has_deleted == 0)
            .all()
        )

        filtered = []
        monthly_count = defaultdict(int)

        for booking in bookings:
            check_in_dt = booking.listing.check_in
            check_in = check_in_dt.date() if hasattr(check_in_dt, "date") else check_in_dt

            # Count per month if only year is specified
            if year and not month and not day:
                if check_in.year == year:
                    monthly_count[check_in.month] += 1
                continue

            if year and check_in.year != year:
                continue
            if month and check_in.month != month:
                continue
            if day and check_in.day != day:
                continue

            booking_data = {
                "user_email": user_email,
                "resort_name": booking.listing.resort.name,
                "resort_city": booking.listing.resort.city,
                "resort_country": booking.listing.resort.country,
                "unit_type": booking.listing.unit_type.name,
                "nights": booking.listing.nights,
                "check_in": check_in.strftime("%Y-%m-%d"),
                "check_out": booking.listing.check_out.strftime("%Y-%m-%d"),
                "reservation_no": booking.listing.reservation_no,
                "total_booking_price": f"${booking.booking_metrics.total_booking_price:.2f}" if booking.booking_metrics else "N/A",
                "listing_status": booking.listing.status,
                "check_in_obj": check_in
            }

            filtered.append(booking_data)

        # Case: Only year is provided
        if year and not month and not day:
            total_count = sum(monthly_count.values())
            if total_count > 2:
                month_map = {
                    1: "January", 2: "February", 3: "March", 4: "April",
                    5: "May", 6: "June", 7: "July", 8: "August",
                    9: "September", 10: "October", 11: "November", 12: "December"
                }
                return {
                    "message": f"Too many bookings ({total_count}) found for {year}. Please specify a month.",
                    "monthly_counts": {month_map[m]: c for m, c in sorted(monthly_count.items())}
                }

        # Separate upcoming and past
        upcoming, past = [], []
        for b in filtered:
            if b["check_in_obj"] >= today:
                upcoming.append(b)
            else:
                past.append(b)

        # Sort
        upcoming = sorted(upcoming, key=lambda b: b["check_in_obj"])
        past = sorted(past, key=lambda b: b["check_in_obj"], reverse=True)

        # Apply limits if no filters
        if not any([year, month, day]):
            upcoming = upcoming[:upcoming_limit]
            past = past[:past_limit]

        # Remove helper
        for b in upcoming + past:
            b.pop("check_in_obj", None)

        def get_month_year_summary(bookings_list, max_months_per_year=3):
            summary = defaultdict(set)
            for b in bookings_list:
                d = date.fromisoformat(b["check_in"])
                summary[d.year].add(d.strftime("%B"))
            return {
                y: sorted(list(m))[:max_months_per_year]
                for y, m in summary.items()
            }

        return {
            "upcoming_bookings": upcoming,
            "past_bookings": past,
            "summary": {
                "upcoming_months_years": get_month_year_summary(upcoming),
                "past_months_years": get_month_year_summary(past)
            }
        }

    except Exception as e:
        return {
            "upcoming_bookings": [],
            "past_bookings": [],
            "summary": {},
            "error": str(e)
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
