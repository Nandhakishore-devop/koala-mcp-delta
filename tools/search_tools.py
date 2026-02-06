import re
import calendar
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, cast, Numeric, extract, asc, desc
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

def slugify_resort_name(name: str) -> str:
    return (
        name.lower()
        .replace("’", "")
        .replace("'", "")
        .replace("&", "and")
        .replace(",", "")
        .replace(".", "")
        .replace("(", "")
        .replace(")", "")
        .replace(" ", "-")
    )

def normalize_future_dates(check_in_str: str, check_out_str: str):
    """Ensure dates are always in the future relative to today."""
    today = datetime.today()
    ci = datetime.strptime(check_in_str, "%Y-%m-%d")
    co = datetime.strptime(check_out_str, "%Y-%m-%d")
    while co < today:
        ci = ci.replace(year=ci.year + 1)
        co = co.replace(year=co.year + 1)
    return ci.strftime("%Y-%m-%d"), co.strftime("%Y-%m-%d")

def get_month_year_range(month_input: str, year_input: int = None):
    """Get first and last day of the month, ensuring future dates."""
    today = datetime.today()
    month_str = str(month_input).strip().lower()
    try:
        month_num = int(month_str) if month_str.isdigit() else datetime.strptime(month_str[:3], "%b").month
    except ValueError:
        raise ValueError(f"Invalid month: {month_input}")
    year = year_input if year_input else today.year
    if not year_input and month_num < today.month:
        year += 1
    first_day = datetime(year, month_num, 1)
    last_day = datetime(year, month_num, calendar.monthrange(year, month_num)[1])
    ci_str, co_str = normalize_future_dates(first_day.strftime("%Y-%m-%d"), last_day.strftime("%Y-%m-%d"))
    return ci_str, co_str

def search_available_future_listings_merged(**filters) -> Dict[str, Any]:
    session = SessionLocal()
    try:
        # ---------------- Base query ----------------
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
                UnitType.name.label("unit_type_name_fallback"),
                UnitType.id.label("unit_type_id"),
            )
            .join(UnitType, PtRtListing.unit_type_id == UnitType.id)
            .distinct()
        )

        filter_conditions = []

        # ---------------- Resort name filter ----------------
        resort_name = filters.get("resort_name")
        if resort_name:
            if isinstance(resort_name, str):
                filter_conditions.append(PtRtListing.resort_name.ilike(f"%{resort_name.strip()}%"))
            else:
                filter_conditions.append(PtRtListing.resort_name == resort_name)

        # ---------------- Total count listings with filter ----------------
        total_count_listings = (
            session.query(
                PtRtListing.resort_id,
                func.count(PtRtListing.id).label("count")
            )
            .filter(*filter_conditions)
            .group_by(PtRtListing.resort_id)
            .all()
        )

        # ---------------- Non-date filters ----------------
        skip_fields = {
            "year", "month", "day", "listing_check_in", "listing_check_out",
            "price_sort", "limit", "update_fields", "min_guests",
            "resort_name", "unit_type_name", "check_in", "check_out", "min_nights"
        }
        for field_name, value in filters.items():
            if value is not None and hasattr(PtRtListing, field_name) and field_name not in skip_fields:
                column = getattr(PtRtListing, field_name)
                filter_conditions.append(
                    column.ilike(f"%{value.strip()}%") if isinstance(value, str) else column == value
                )

        # ---------------- Date filters ----------------
        today = datetime.combine(datetime.today().date(), datetime.min.time())
        ninety_days = today + timedelta(days=90)

        check_in = filters.get("check_in")
        check_out = filters.get("check_out")
        check_in_str = filters.get("listing_check_in")
        check_out_str = filters.get("listing_check_out")
        year = filters.get("year")
        month = filters.get("month")
        day = filters.get("day")
        unit_type_name = filters.get("unit_type_name")

        date_conditions = []
        date_filters_applied = False

        try:
            if check_in and check_out:
                ci_date = datetime.strptime(check_in, "%Y-%m-%d")
                co_date = datetime.strptime(check_out, "%Y-%m-%d")
                date_conditions.append(PtRtListing.listing_check_in.between(ci_date, co_date))
                date_filters_applied = True

            elif check_in_str and check_out_str:
                ci_str, co_str = normalize_future_dates(check_in_str, check_out_str)
                check_in_date = datetime.strptime(ci_str, "%Y-%m-%d")
                check_out_date = datetime.strptime(co_str, "%Y-%m-%d")
                date_conditions += [
                    PtRtListing.listing_check_in == check_in_date,
                    PtRtListing.listing_check_out == check_out_date,
                ]
                date_filters_applied = True

            elif month and year:
                ci_str, co_str = get_month_year_range(month, year)
                check_in_start = datetime.strptime(ci_str, "%Y-%m-%d")
                check_in_end = datetime.strptime(co_str, "%Y-%m-%d")
                if day:
                    specific_date = datetime(int(year), int(month), int(day))
                    date_conditions += [
                        PtRtListing.listing_check_in == specific_date,
                        PtRtListing.listing_check_out == specific_date,
                    ]
                else:
                    date_conditions += [
                        PtRtListing.listing_check_in >= check_in_start,
                        PtRtListing.listing_check_in <= check_in_end,
                    ]
                date_filters_applied = True

            elif year or month or day:
                col = PtRtListing.listing_check_in
                conditions = []
                if year: conditions.append(extract("year", col) == int(year))
                if month: conditions.append(extract("month", col) == int(month))
                if day: conditions.append(extract("day", col) == int(day))
                if conditions:
                    date_conditions.append(and_(*conditions))
                    date_filters_applied = True

            # ---------------- Default/Fallback Date Logic ----------------
            ninety_days = today + timedelta(days=90)
            two_eighty_days = today + timedelta(days=280)

            if not date_filters_applied:
                # Case A: User never gave a date -> always default 0–90 days first
                date_conditions.append(PtRtListing.listing_check_in.between(today, ninety_days))

            # ---------------- Preview results ----------------
            preview_query = base_query.filter(and_(*filter_conditions), and_(*date_conditions))

            if unit_type_name:
                preview_query = preview_query.filter(PtRtListing.unit_type_name.ilike(f"%{unit_type_name}%"))
            if resort_name:
                preview_query = preview_query.filter(PtRtListing.resort_name.ilike(f"%{resort_name}%"))

            preview_results = preview_query.limit(1).all()

            # ---------------- Fallback if no data ----------------
            if not preview_results:
                if not date_filters_applied:
                    # Case B: No date given, first 90 days failed -> fallback to 0–280 days
                    date_conditions = [PtRtListing.listing_check_in.between(today, two_eighty_days)]
                else:
                    # Case C: User gave month/year/date but no data found -> fallback to 0–90 days
                    date_conditions = [PtRtListing.listing_check_in.between(today, ninety_days)]

        except ValueError:
             pass

        # ---------------- Guests filter ----------------
        min_guests = filters.get("min_guests")
        if min_guests:
            try:
                min_guests = int(min_guests)
                filter_conditions.append(func.abs(UnitType.sleeps) >= min_guests)
            except ValueError:
                pass

         # --------------nights stays filter ---------------
        min_nights = filters.get("min_nights")
        if min_nights:
            try:
                min_nights = int(min_nights)
                filter_conditions.append(func.abs(PtRtListing.listing_nights) >= min_nights)
            except ValueError:
                pass

        # ---------------- Unit type filter ----------------
        if unit_type_name:
            filter_conditions.append(PtRtListing.unit_type_name.ilike(f"%{str(unit_type_name).strip()}%"))

        # ---------------- Final query ----------------
        query = base_query.filter(and_(*filter_conditions), and_(*date_conditions))

        # ---------------- Price sorting ----------------
        price_sort = filters.get("price_sort", "asc")
        price_col_numeric = cast(PtRtListing.listing_price_night, Numeric)
        default_limit = 80

        if price_sort == "asc":
            query = query.order_by(asc(func.abs(price_col_numeric)))
        elif price_sort == "desc":
            query = query.order_by(desc(func.abs(price_col_numeric)))
            default_limit = 85
        elif price_sort == "cheapest":
            query = query.filter(func.abs(price_col_numeric) <= 333).order_by(asc(func.abs(price_col_numeric)))
        elif price_sort == "average":
            query = query.filter(func.abs(price_col_numeric).between(334, 666)).order_by(asc(func.abs(price_col_numeric)))
        elif price_sort == "highest":
            query = query.filter(func.abs(price_col_numeric) >= 667).order_by(desc(func.abs(price_col_numeric)))
            default_limit = 85

        # ---------------- Limit ----------------
        limit = int(filters.get("limit", default_limit))
        results = query.limit(limit).all()

        # ---------------- Build structured results ----------------
        results_list = []
        for row in results:
            cancel_date_raw = row.listing_cancelation_date
            cancel_date = (
                str(cancel_date_raw).split(" ")[0]
                if cancel_date_raw and cancel_date_raw not in ["0000-00-00", "0000-00-00 00:00:00", None, ""]
                else "Date not specified"
            )
            policy_desc = CANCELLATION_POLICY_DESCRIPTIONS.get(row.listing_cancelation_policy_option, "Policy not specified")
            slug = row.resort_slug or slugify_resort_name(row.resort_name) if row.resort_name else None
            resort_url = f"{BASE_LIST_URL}{slug}?startD=&endD=&adults=0&months=&dateOption=7" if slug else None
            booking_url = None
            if slug and row.id and row.listing_check_in and row.listing_check_out:
                booking_url = (
                    f"{BASE_LIST_URL}{slug}"
                    f"?startD={row.listing_check_in.strftime('%Y-%m-%d')}"
                    f"&endD={row.listing_check_out.strftime('%Y-%m-%d')}"
                    f"&adults=0&months=&dateOption=7"
                )

            display_price = f"from ${row.listing_price_night} per night" if row.listing_price_night else "Price not available"

            results_list.append({
                "id": row.id,
                "resort_id": row.resort_id,
                "resort_name": row.resort_name,
                "unit_type": row.unit_type_name or row.unit_type_name_fallback,
                "sleeps": int(row.sleeps) if row.sleeps is not None else None,
                "check_in": row.listing_check_in.strftime("%Y-%m-%d") if row.listing_check_in else None,
                "check_out": row.listing_check_out.strftime("%Y-%m-%d") if row.listing_check_out else None,
                "price": display_price,
                "cancellation_policy_description": policy_desc,
                "listing_cancelation_date": cancel_date,
                "cancellation_info": f"{policy_desc} (By {cancel_date})",
                "resort_url": resort_url,
                "url": booking_url,
            })

        # ---------------- Totals ----------------
        total_listings_for_resort = 0
        if results_list:
            first_resort_id = results_list[0]['resort_id']
            total_listings_for_resort = next(
                (item.count for item in total_count_listings if item.resort_id == first_resort_id), 0
            )

        return {
            "results": results_list,
            "total_listings_for_resort": total_listings_for_resort,
        }

    except Exception as e:
        session.rollback()
        return {"results": [], "error": str(e)}

    finally:
        session.close()
