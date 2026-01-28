from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, cast, Numeric, extract
from src.database.db import SessionLocal
from src.database.models import PtRtListing, UnitType, Resort

CANCELLATION_POLICY_DESCRIPTIONS = {
    "flexible": "Full refund if canceled at least 3 days before check-in.",
    "relaxed": "Full refund if canceled at least 16 days before check-in.",
    "moderate": "Full refund if canceled at least 32 days before check-in.",
    "firm": "Full refund if canceled at least 62 days before check-in.",
    "strict": "Booking is non-refundable"
}

BASE_LIST_URL = "https://www.go-koala.com/resort/"

def normalize_future_dates(check_in_str: str, check_out_str: str):
    today = datetime.today()
    ci = datetime.strptime(check_in_str, "%Y-%m-%d")
    co = datetime.strptime(check_out_str, "%Y-%m-%d")
    while co < today:
        ci = ci.replace(year=ci.year + 1)
        co = co.replace(year=co.year + 1)
    return ci.strftime("%Y-%m-%d"), co.strftime("%Y-%m-%d")

def search_available_future_listings_merged(
    resort_name: Optional[str] = None, 
    resort_id: Optional[int] = None,
    listing_check_in: Optional[str] = None, 
    listing_check_out: Optional[str] = None, 
    limit: int = 10,
    price_sort: str = "asc"
) -> Dict[str, Any]:
    """
    Search for available resort listings with date and price filters.
    
    :param resort_name: Optional name of the resort to filter by.
    :param resort_id: Optional ID of the resort to filter by.
    :param listing_check_in: Optional check-in date (YYYY-MM-DD).
    :param listing_check_out: Optional check-out date (YYYY-MM-DD).
    :param limit: Maximum number of results to return (default 10).
    :param price_sort: Sort by price, 'asc' (default) or 'desc'.
    """
    session = SessionLocal()
    try:
        base_query = (
            session.query(
                PtRtListing.id,
                PtRtListing.resort_id,
                PtRtListing.resort_name,
                PtRtListing.resort_slug,
                PtRtListing.listing_check_in,
                PtRtListing.listing_check_out,
                PtRtListing.listing_price_night,
                PtRtListing.listing_cancelation_policy_option,
                PtRtListing.listing_cancelation_date,
                PtRtListing.unit_type_name,
                UnitType.sleeps,
                UnitType.name.label("unit_type_name_fallback")
            )
            .join(UnitType, PtRtListing.unit_type_id == UnitType.id)
        )

        filter_conditions = []
        if resort_name:
            filter_conditions.append(PtRtListing.resort_name.ilike(f"%{resort_name.strip()}%"))
        
        if resort_id:
            try:
                rid = int(resort_id)
                filter_conditions.append(PtRtListing.resort_id == rid)
            except (ValueError, TypeError):
                pass

        today = datetime.combine(datetime.today().date(), datetime.min.time())
        ninety_days = today + timedelta(days=90)
        
        # Simplified date logic for MCP
        if listing_check_in and listing_check_out:
            try:
                ci_str, co_str = normalize_future_dates(listing_check_in, listing_check_out)
                ci_date = datetime.strptime(ci_str, "%Y-%m-%d")
                co_date = datetime.strptime(co_str, "%Y-%m-%d")
                filter_conditions += [
                    PtRtListing.listing_check_in == ci_date,
                    PtRtListing.listing_check_out == co_date
                ]
            except Exception:
                # If date parsing fails, fall back to future window or just skip date filter
                filter_conditions.append(PtRtListing.listing_check_in >= today)
        else:
            filter_conditions.append(PtRtListing.listing_check_in.between(today, ninety_days))

        query = base_query.filter(and_(*filter_conditions))
        
        price_col = cast(PtRtListing.listing_price_night, Numeric)
        if price_sort == "desc":
            query = query.order_by(price_col.desc())
        else:
            query = query.order_by(price_col.asc())

        results = query.limit(limit).all()

        results_list = []
        for row in results:
            slug = row.resort_slug or row.resort_name.lower().replace(" ", "-")
            results_list.append({
                "resort_id": row.resort_id,
                "resort_name": row.resort_name,
                "unit_type": row.unit_type_name or row.unit_type_name_fallback,
                "sleeps": row.sleeps,
                "check_in": row.listing_check_in.strftime("%Y-%m-%d"),
                "check_out": row.listing_check_out.strftime("%Y-%m-%d"),
                "price": f"${row.listing_price_night}",
                "url": f"{BASE_LIST_URL}{slug}"
            })

        return {"results": results_list}
    finally:
        session.close()
