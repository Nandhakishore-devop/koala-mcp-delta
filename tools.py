"""
Fixed Tool functions for resort booking system using SQLAlchemy with MySQL.
"""
from typing import List, Dict, Any, Optional,Union
from sqlalchemy import create_engine, Column, Integer,BigInteger, String, DateTime, ForeignKey, Text, Float, Boolean, and_, asc, desc ,extract, or_, func,cast, Numeric
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, DateTime, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import json
import os
from datetime import datetime, timedelta ,date 
from dotenv import load_dotenv
from collections import Counter, defaultdict
import calendar
from calendar import monthrange
from sqlalchemy.orm import Session
from sqlalchemy import text
import random
from sqlalchemy import case


# Load environment variables
load_dotenv()


# Database models
Base = declarative_base()
# print("ruban_db",Base)


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20))
    has_deleted = Column(Integer, default=0)  # 0 = active, 1 = deleted
    status = Column(String(20), default='active')
    
    # Relationships - Fixed to avoid circular references
    created_resorts = relationship("Resort", foreign_keys="Resort.creator_id", back_populates="creator")
    owned_bookings = relationship("Booking", foreign_keys="Booking.owner_id", back_populates="owner")
    user_bookings = relationship("Booking", foreign_keys="Booking.user_id", back_populates="user")


class Listing(Base):
    __tablename__ = 'listings'
    
    id = Column(Integer, primary_key=True)
    resort_id = Column(Integer, ForeignKey('resorts.id'), nullable=False)
    unit_type_id = Column(Integer, ForeignKey('unit_types.id'), nullable=False)
    nights = Column(Integer, nullable=False)
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    has_deleted = Column(Integer, default=0)  # 0 = active, 1 = deleted
    status = Column(String(30), default='active')
    reservation_no = Column(String(30),nullable=False)
    
    # Relationships
    resort = relationship("Resort", back_populates="listings")
    unit_type = relationship("UnitType", back_populates="listings")
    bookings = relationship("Booking", back_populates="listing")
   

class Amenity(Base):
    __tablename__ = 'amenities'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    vrbo_name = Column(Text)
    slug = Column(String(255))
    image = Column(String(255))
    status = Column(String(255), default='active')
    is_key_amenity = Column(Integer, default=0)
    # Relationships
    resort_amenities = relationship("ResortAmenity", back_populates="amenity")

class ResortMigration(Base):
    __tablename__ = 'resort_migration'

    id = Column(BigInteger, primary_key=True)
    pt_rt_id = Column(Integer, nullable=False)
    listing_id = Column(Integer)
    resort_id = Column(Integer, default=0)  # This is just an identifier, not a foreign key
    resort_slug = Column(String(255))
    resort_name = Column(String(255))
    distance = Column(String(255))
    address = Column(String(255))
    location_types = Column(String(255))
    resort_has_deleted = Column(Integer, default=0)
    country = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    zip = Column(String(255))
    is_featured = Column(Integer, default=0)
    unit_has_deleted = Column(Integer, default=0) 
    resort_google_rating = Column(Integer, default=0)
    resort_status = Column(String(50))

    # listing_check_in = Column(DateTime)
    # listing_check_out = Column(DateTime)
    # listing_cancelation_date = Column(DateTime)
    # listing_price_night = Column(String(50))
    # listing_nights = Column(Integer)
    # listing_publish_type = Column(String(50))
    # listing_has_deleted = Column(Integer, default=0)
    # listing_status = Column(String(50))
    # listing_currency_id = Column(Integer, default=0)
    # listing_currency_code = Column(String(255))
    # has_weekend = Column(Integer, default=0)
    # listing_owner_id = Column(Integer, default=0)  # Remove ForeignKey to avoid issues
    # listing_count = Column(Integer, default=0)
    # unit_type_id = Column(Integer, default=0)  # Remove ForeignKey to avoid issues
    # available_count = Column(String(255))
    # exactlisting_listing_count = Column(String(255))
    # unit_type_slug = Column(String(255))
    # unit_type_name = Column(String(255))
    # unit_bedrooms = Column(String(5))
    # unit_bathrooms = Column(String(7))
    # unit_sleeps = Column(Integer, default=0)
    # unit_kitchenate = Column(String(255))
   
    # unit_type_images = Column(Text)  # JSON
    # featured_amenities = Column(String(150))
    # unit_status = Column(String(255))
    # unit_cancelation_policy_option = Column(String(255))
    # lattitude = Column(String(255))
    # longitude = Column(String(255))
    # county = Column(String(255))

    # popular = Column(Integer, default=0)
    # is_fitness_center = Column(Integer, default=0)
    # is_free_wifi = Column(Integer, default=0)
    # is_restaurant = Column(Integer, default=0)
    # is_swimming_pool = Column(Integer, default=0)
    # hotel_star = Column(Integer, default=0)
    # top_21_resort = Column(Integer, default=0)
    # resort_amenities = Column(Text)  # JSON
    # reslrt_updated_at = Column(DateTime)
    
    
   
    # google_rating = Column(Integer, default=0)
    # user_ratings_total = Column(Integer, default=0)
    # google_rating_default = Column(String(8))
    # pets_friendly = Column(Integer, default=0)
    # unit_rates_price = Column(String(50))
    # offer = Column(String(255))
    # offer_price = Column(String(255))
    # offer_popup = Column(String(255))
    # drivetime = Column(String(255))
    # image = Column(String(255))
    # images = Column(Text)  # JSON
    # resort_images = Column(Text)  # JSON
    # resort_aminities = Column(Text)  # JSON
    # amenities = Column(Text)  # JSON
    # highlight_quote = Column(String(255))
    # hotelStar = Column(String(255))
    # is_open_availability = Column(String(255))
    # brand_id = Column(Integer, default=0)
    # brand_name = Column(String(255))
    # brand_slug = Column(String(255))
    # brand_order = Column(String(255))
    # unit_rate_id = Column(Integer, default=0)
    # unit_rate_start_date = Column(DateTime)
    # unit_rate_availability = Column(String(255))
    # unit_rate_number_available = Column(String(255))
    # unit_rate_nightly_price = Column(String(255))
    # unit_rates_count = Column(String(255))
    # created_at = Column(DateTime)
    # updated_at = Column(DateTime)




class Resort(Base):
    __tablename__ = 'resorts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    address = Column(Text)
    has_deleted = Column(Integer, default=0)  # 0 = active, 1 = deleted
    status = Column(String(20), default='active')  # active/pending
    lattitude = Column(String(255))  # Note: keeping original spelling
    longitude = Column(String(255))
    country = Column(String(100))
    city = Column(String(100))
    state = Column(String(100))
    zip = Column(String(20))
    county = Column(String(100))
    highlight_quote = Column(Text)
    description = Column(Text)
    
    # Relationships
    creator = relationship("User", foreign_keys=[creator_id], back_populates="created_resorts")
    unit_types = relationship("UnitType", back_populates="resort")
    listings = relationship("Listing", back_populates="resort")
    images = relationship("ResortImage",back_populates="resort")
    resort_amenities = relationship("ResortAmenity", back_populates="resort")
    reviews = relationship("ResortReview", back_populates="resort", cascade="all, delete-orphan")
    
    # New relationship for location types
    location_types = relationship("LocationType", back_populates="resort", cascade="all, delete-orphan")
    


class PtRtListing(Base):
    __tablename__ = 'pt_rt_listings'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_by = Column(Integer, default=0)
    updated_by = Column(Integer, default=0)
    listing_id = Column(Integer)
    redweek_id = Column(String(255), default='0')
    listing_unique_hash = Column(String(255))
    listing_unique_listing_code = Column(String(255))
    listing_price_night = Column(String(50))
    vrbo_markup_commission = Column(String(10))
    listing_rw_commission = Column(String(255), default='0')
    listing_rw_verified = Column(String(255), default='0')
    listing_rw_redweek_id = Column(String(255), default='0')
    listing_publish_type = Column(String(50))
    listing_dvc_id = Column(Integer, default=0)
    listing_hawaii_id = Column(Integer, default=0)
    listing_currency_id = Column(Integer, default=0)
    listing_currency_code = Column(String(255))
    listing_owner_id = Column(Integer, default=0)
    listing_nights = Column(Integer, default=0)
    listing_check_in = Column(DateTime)
    listing_check_out = Column(DateTime)
    has_weekend = Column(Integer, default=0)
    exclusive = Column(Boolean, default=False)
    vip_featured_old = Column(Integer, default=0)
    hot_deals = Column(Boolean, default=False)
    hotdeal_toggled_at = Column(DateTime)
    l_home_featured = Column(Boolean, default=False)
    l_destination_featured = Column(Boolean, default=False)
    l_vip_featured = Column(Boolean, default=False)
    listing_cancelation_policy_option = Column(String(50))
    l_booking_type = Column(String(50))
    l_custom_days = Column(String(5))
    l_refund_before = Column(String(5))
    l_refund_after = Column(String(5))
    listing_cancelation_date = Column(DateTime)
    listing_has_deleted = Column(Integer, default=0)
    listing_status = Column(String(50))
    listing_type = Column(String(255), default='prebook')
    availability_request = Column(Boolean, default=False)
    l_created_at = Column(DateTime)
    l_updated_at = Column(DateTime)
    l_last_activated_at = Column(DateTime)
    pt_or_rt = Column(String(10))
    unit_rate_id = Column(Integer, default=0)
    unit_type_id = Column(Integer, ForeignKey('unit_types.id'), nullable=True)
    # pro_unit_type_id = Column(Integer, default=0)
    # unit_has_deleted = Column(Integer, default=0)
    unit_type_slug = Column(String(255))
    unit_type_name = Column(String(255))
    # unit_kitchenate = Column(String(255))
    # unit_status = Column(String(255))
    unit_sleeps = Column(String(50))  # Changed to String to match possible formats
    resort_id = Column(Integer, default=0)  # This is NOT a foreign key - it's just data
    resort_lattitude = Column(String(255))
    resort_longitude = Column(String(255))
    resort_slug = Column(String(255))
    resort_name = Column(String(255))
    resort_has_deleted = Column(Integer, default=0)
    resort_status = Column(String(50))
    resort_is_featured = Column(Integer, default=0)
    resort_location_types = Column(Text)
    resort_amenity_ids = Column(String(255))
    resort_pets_friendly = Column(String(255))
    resort_brand_id = Column(Integer, default=0)
    resort_brand_name = Column(String(255))
    resort_address = Column(String(255))
    resort_city = Column(String(100))
    resort_country = Column(String(100))
    resort_state = Column(String(100))
    resort_zip = Column(String(10))
    resort_county = Column(String(100))
    resort_google_rating = Column(Integer, default=0)
    resort_google_rating_default = Column(String(8))
    r_featured_amenities = Column(String(600))
    resort_updated_at = Column(DateTime)
   
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Relationships
    unit_type = relationship("UnitType", back_populates="pt_rt_listings")
    # In PtRtListing

  
    # Remove the problematic relationships since resort_id is not a real foreign key
    # If you need to join with Resort table, do it manually in queries


class UnitType(Base):
    __tablename__ = 'unit_types'
    
    id = Column(Integer, primary_key=True)
    resort_id = Column(Integer, ForeignKey('resorts.id'), nullable=False)
    name = Column(String(200), nullable=False)
    has_deleted = Column(Integer, default=0)  # 0 = active, 1 = deleted
    status = Column(String(20), default='active')  # active/pending
    sleeps = Column(String(50))  # Changed to String to match possible formats

    # Relationships
    resort = relationship("Resort", back_populates="unit_types")
    listings = relationship("Listing", back_populates="unit_type")
    # pt_rt_listings = relationship("PtRtListing", back_populates="unit_type")

    pt_rt_listings = relationship(
        "PtRtListing",
        primaryjoin="UnitType.resort_id == foreign(PtRtListing.resort_id)",
        back_populates="unit_type"
    )

    # Remove pt_rt_listings relationship


class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True)
    unique_booking_code = Column(String(50), unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Owner of the listing
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)   # Booker/traveller
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)

    # Relationships
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_bookings")
    user = relationship("User", foreign_keys=[user_id], back_populates="user_bookings")
    listing = relationship("Listing", back_populates="bookings")  
    booking_metrics = relationship("BookingMetrics", back_populates="booking", uselist=False)  # ✅ one-to-one


class BookingMetrics(Base):
    __tablename__ = 'booking_metrics'
    
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=False)
    total_listing_price = Column(Float, nullable=False)
    total_booking_price = Column(Float, nullable=False)

    booking = relationship("Booking", back_populates="booking_metrics")  # ✅


class ResortImage(Base):
    __tablename__ = 'resort_images'

    id = Column(Integer, primary_key=True)
    resort_id = Column(Integer, ForeignKey('resorts.id'), nullable=False)
    image = Column(String(255), nullable=False)
    height = Column(Integer)
    width = Column(Integer)
    aspect_ratio = Column(String(50))
    image_order = Column(Integer, default=0)
    
    resort = relationship("Resort", back_populates="images")


class ResortAmenity(Base):
    __tablename__ = "resort_amenities"

    id = Column(Integer, primary_key=True)
    resort_id = Column(Integer, ForeignKey("resorts.id"), nullable=False)
    amenity_id = Column(Integer, ForeignKey("amenities.id"), nullable=False)
    has_deleted = Column(Integer, default=0)
    # Relationships
    resort = relationship("Resort", back_populates="resort_amenities")
    amenity = relationship("Amenity", back_populates="resort_amenities")


class EsPlaceOfInterests(Base):
    __tablename__ = "es_place_of_interests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    es_poi_location_id = Column(
        Integer, ForeignKey("es_poi_locations.id"), nullable=False
    )
    location_category_id = Column(Integer)  # add FK if you also join categories
    term = Column(String(255))
    full_term = Column(String(255))
    image = Column(String(255))
    price = Column(String(255))
    type = Column(String(255))
    lattitude = Column(String(255))   # spelling matches DB
    longitude = Column(String(255))
    radius = Column(String(255))
    country = Column(String(255))
    state = Column(String(255))
    city = Column(String(255))
    description = Column(Text)
    url = Column(String(300))

    # 🔗 Relationship back to EsPoiLocations
    location = relationship("EsPoiLocations", back_populates="place_of_interests")


class EsPoiLocations(Base):
    __tablename__ = "es_poi_locations"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    full_name = Column(String(255))
    name = Column(String(255))
    description = Column(Text)
    radius = Column(Integer, default=0)
    country = Column(String(255))
    state = Column(String(255))
    county = Column(String(255))
    city = Column(String(255))
    lattitude = Column(String(255))
    longitude = Column(String(255))
    has_deleted = Column(Integer, nullable=False, default=0)

    # 🔗 Relationship to EsPlaceOfInterests
    place_of_interests = relationship(
        "EsPlaceOfInterests", back_populates="location", cascade="all, delete-orphan"
    )


class LocationType(Base):
    __tablename__ = "location_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resort_id = Column(Integer, ForeignKey("resorts.id"), nullable=False)
    resort_location_master_id = Column(Integer, ForeignKey("resort_location_master.id"), nullable=False)
    types = Column(String(255), nullable=False)
    status = Column(Integer, default=1, nullable=False)

    # Relationships
    resort = relationship("Resort", back_populates="location_types")
   


class ResortReview(Base):
    __tablename__ = "resort_reviews"   # replace with your actual table name

    id = Column(Integer, primary_key=True, autoincrement=True)
    resort_id = Column(Integer, ForeignKey("resorts.id"), nullable=False)  # assumes table is `resorts`

    author_name = Column(String(255))
    author_url = Column(String(255))
    language = Column(String(255))
    profile_photo_url = Column(String(600))
    rating = Column(String(10))
    relative_time_description = Column(String(255))
    text = Column(Text)
    time = Column(String(255))
    

    # Relationship back to Resort
    resort = relationship("Resort", back_populates="reviews")

# Database setup
def get_database_url():
    """Get database URL from environment variables."""
    host = os.getenv("MYSQL_HOST", "localhost")
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "koala_dev")
    # print("host",host)
    # print("user",user)
    # print("password",password)
    # print("database",database)
    
    # Build MySQL URL
    if password:
        return f"mysql+pymysql://{user}:{password}@{host}/{database}"
    else:
        return f"mysql+pymysql://{user}@{host}/{database}"

DATABASE_URL = get_database_url()
engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_recycle=3600,      # Recycle connections every 60 minutes
    pool_pre_ping=True      # Check connection before using
)
print("DATABASE_check",DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# print("engine",engine)
# print("se_db",SessionLocal)


def initialize_database():
    """Run once at startup to verify DB connection."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False


# rubi _ tools

CATEGORY_MAPPING = {
    "Top Sights": 1,
    "Restaurants": 2,
    "Airport": 3,
    "Transit": 4
}

def get_city_from_resort(resort_name: str, categories: List[str] = None) -> Dict[str, Any]:
    with SessionLocal() as session:
        try:
            # ---------------- Step 1: Get resort and its city ----------------
            resort = session.query(Resort).filter(Resort.name.ilike(f"%{resort_name}%")).first()
            if not resort:
                return {"error": f"Resort '{resort_name}' not found"}

            city = resort.city

            # ---------------- Step 2: Get the POI location for this city ----------------
            place_of_location = (
                session.query(EsPoiLocations)
                .filter(EsPoiLocations.city.ilike(f"%{city}%"))
                .first()
            )
            if not place_of_location:
                return {
                    "resort_name": resort.name,
                    "city": city,
                    "pois": "No POI location found"
                }

            poi_location_id = place_of_location.id

            # ---------------- Step 3: Prepare category filter ----------------
            if categories:
                category_ids = [CATEGORY_MAPPING[cat] for cat in categories if cat in CATEGORY_MAPPING]
            else:
                category_ids = list(CATEGORY_MAPPING.values())  # all categories by default

            # ---------------- Step 4: Fetch POIs for this location & categories ----------------
            pois: List[EsPlaceOfInterests] = (
                session.query(EsPlaceOfInterests)
                .filter(
                    EsPlaceOfInterests.es_poi_location_id == poi_location_id,
                    EsPlaceOfInterests.location_category_id.in_(category_ids)
                )
                .limit(5)  # limit 5 nearest POIs
                .all()
            )

            # ---------------- Step 5: Serialize results ----------------
            results = [
                {
                    "term": p.term,
                    "full_term": p.full_term,
                    "state": p.state,
                    "city": p.city,
                    "description": p.description
                }
                for p in pois
            ]

            # ---------------- Step 6: Build response ----------------
            return {
                "resort_name": resort.name,
                "city": city,
                "place_of_location": {
                    "id": place_of_location.id,
                    "city": place_of_location.city,
                    "state": place_of_location.state,
                    "country": place_of_location.country
                },
                "pois": results or "No POIs found"
            }

        except Exception as e:
            return {"error": str(e)}


# Cancellation policies
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

# def search_available_future_listings_enhanced(**filters) -> List[Dict[str, Any]]:
#     session = SessionLocal()
#     try:
#         query = (
#             session.query(
#                 PtRtListing.id,
#                 PtRtListing.resort_id,
#                 PtRtListing.resort_name,
#                 PtRtListing.resort_slug,
#                 PtRtListing.listing_check_in,
#                 PtRtListing.listing_check_out,
#                 PtRtListing.listing_price_night,
#                 PtRtListing.listing_cancelation_policy_option,
#                 PtRtListing.listing_cancelation_date,
#                 UnitType.sleeps,
#                 UnitType.name.label("unit_type_name"),
#                 UnitType.id.label("unit_type_id"),
#             )
#             .join(UnitType, PtRtListing.unit_type_id == UnitType.id)
#             .distinct()
#         )

#         filter_conditions = []

#         # ---------------- Non-date filters ----------------
#         skip_fields = {"year", "month", "day", "listing_check_in", "listing_check_out", "price_sort", "limit", "update_fields", "min_guests"}
#         for field_name, value in filters.items():
#             if value is not None and hasattr(PtRtListing, field_name) and field_name not in skip_fields:
#                 column = getattr(PtRtListing, field_name)
#                 filter_conditions.append(column.ilike(f"%{value.strip()}%") if isinstance(value, str) else column == value)

#         # ---------------- Date filters ----------------
#         exact_date_filter = False
#         check_in_str = filters.get("listing_check_in")
#         check_out_str = filters.get("listing_check_out")
#         year = filters.get("year")
#         month = filters.get("month")
#         day = filters.get("day")

#         try:
#             if check_in_str and check_out_str:
#                 # Use exact dates if provided
#                 ci_str, co_str = normalize_future_dates(check_in_str, check_out_str)
#                 check_in_start = datetime.strptime(ci_str, "%Y-%m-%d")
#                 check_in_end = datetime.strptime(co_str, "%Y-%m-%d")
#                 filter_conditions += [
#                     PtRtListing.listing_check_in == check_in_start,
#                     PtRtListing.listing_check_out == check_in_end,
#                 ]
#                 exact_date_filter = True

#             elif month and not check_in_str and not check_out_str:
#                 # Month-based filtering
#                 ci_str, co_str = get_month_year_range(month, year)
#                 check_in_start = datetime.strptime(ci_str, "%Y-%m-%d")
#                 check_in_end = datetime.strptime(co_str, "%Y-%m-%d")
#                 if day:
#                     specific_date = datetime(year, month, day)
#                     filter_conditions += [
#                         PtRtListing.listing_check_in == specific_date,
#                         PtRtListing.listing_check_out == specific_date,
#                     ]
#                     exact_date_filter = True
#                 else:
#                     filter_conditions += [
#                         PtRtListing.listing_check_in >= check_in_start,
#                         PtRtListing.listing_check_in <= check_in_end,
#                     ]
#                     exact_date_filter = False



#             elif year or day:
#                 col = PtRtListing.listing_check_in
#                 conditions = []
#                 if year: conditions.append(extract("year", col) == int(year))
#                 if month: conditions.append(extract("month", col) == int(month))
#                 if day: conditions.append(extract("day", col) == int(day))
#                 if conditions:
#                     filter_conditions.append(and_(*conditions))
#                     exact_date_filter = True

#         except ValueError as ve:
#             print(f"⚠ Date parsing error: {ve}")


#         if filter_conditions:
#             query = query.filter(and_(*filter_conditions))

#         # ---------------- Guests filter ----------------
#         min_guests = filters.get("min_guests")
#         if min_guests:
#             try:
#                 min_guests = int(min_guests)
#                 query = query.filter(func.abs(UnitType.sleeps) >= min_guests)
#             except ValueError:
#                 print(f"⚠ Invalid min_guests value: {filters['min_guests']}")
#         # ---------------- Price sorting ----------------
#         price_sort = filters.get("price_sort", "asc")
#         price_col_numeric = cast(PtRtListing.listing_price_night, Numeric)

#         # Default limit logic
#         if price_sort == "asc":
#             query = query.order_by(asc(func.abs(price_col_numeric)))
#             default_limit = 80
#             print("asc",query)
#         elif price_sort == "desc":
#             query = query.order_by(desc(func.abs(price_col_numeric)))
#             default_limit = 85
#             print("desc",query)
#         elif price_sort == "cheapest":
#             query = query.filter(func.abs(price_col_numeric) <= 333)\
#                         .order_by(asc(func.abs(price_col_numeric)))
#             default_limit = 80
#             print("cheapest",query)
#         elif price_sort == "average":
#             query = query.filter(func.abs(price_col_numeric).between(334, 666))\
#                         .order_by(asc(func.abs(price_col_numeric)))
#             default_limit = 80
#             print("average",query)
#         elif price_sort == "highest":
#             query = query.filter(func.abs(price_col_numeric) >= 667)\
#                         .order_by(desc(func.abs(price_col_numeric)))
#             default_limit = 85
#             print("highest",query)
#         else:
#             default_limit = 80  # fallback

#         # ---------------- Fetch + deduplicate ----------------
#         limit = int(filters.get("limit", default_limit))  # user limit overrides defaults
#         fetch_limit = limit * 10  # small buffer for deduplication
#         results = query.limit(fetch_limit).all()

#         unique_results = (
#             deduplicate_by_resort_id(results) if price_sort != "avg_price" else results
#         )

#         final_results = unique_results[:limit]

#         # ---------------- Build Structured Result ----------------
#         results_list = []
#         for row in final_results:
#             cancel_date_raw = row.listing_cancelation_date
#             cancel_date = str(cancel_date_raw).split(" ")[0] if cancel_date_raw and cancel_date_raw not in ["0000-00-00", "0000-00-00 00:00:00", None, ""] else "Date not specified"
#             policy_desc = CANCELLATION_POLICY_DESCRIPTIONS.get(row.listing_cancelation_policy_option, "Policy not specified")
#             slug = row.resort_slug or slugify_resort_name(row.resort_name) if row.resort_name else None
#             resort_url = f"{BASE_LIST_URL}{slug}?startD=&endD=&adults=0&months=&dateOption=7" if slug else None
#             booking_url = None
#             if slug and row.id and row.listing_check_in and row.listing_check_out:
#                 booking_url = (
#                     f"{BASE_LIST_URL}{slug}"
#                     f"?startD={row.listing_check_in.strftime('%Y-%m-%d')}"
#                     f"&endD={row.listing_check_out.strftime('%Y-%m-%d')}"
#                     f"&adults=0&months=&dateOption=7"
#                 )

#             display_price = f"from ${row.listing_price_night} per night" if row.listing_price_night else "Price not available"

#             results_list.append({
#                 "resort_id": row.resort_id,
#                 "resort_name": row.resort_name,
#                 "unit_type": row.unit_type_name,
#                 "sleeps": int(row.sleeps) if row.sleeps is not None else None,
#                 "check_in": row.listing_check_in.strftime("%Y-%m-%d") if row.listing_check_in else None,
#                 "check_out": row.listing_check_out.strftime("%Y-%m-%d") if row.listing_check_out else None,
#                 "price_per_night": display_price,
#                 "cancellation_policy_description": policy_desc,
#                 "listing_cancelation_date": cancel_date,
#                 "cancellation_info": f"{policy_desc} (By {cancel_date})",
#                 # "booking_type":l_booking_type,
#                 "resort_url": resort_url,
#                 "booking_url": booking_url
#             })
#             # print("rubi",booking_type)

#         return results_list

#     except Exception as e:
#         print(f"❌ Error in search_available_future_listings_enhanced: {str(e)}")
#         session.rollback()
#         return []
#     finally:
#         session.close()


 
#             # elif month and not check_in_str and not check_out_str:
#             #     ci_str, co_str = get_month_year_range(month, year)
#             #     check_in_start = datetime.strptime(ci_str, "%Y-%m-%d")
#             #     check_in_end = datetime.strptime(co_str, "%Y-%m-%d")
#             #     filter_conditions += [
#             #         PtRtListing.listing_check_in >= check_in_start,
#             #         PtRtListing.listing_check_in <= check_in_end,
#             #     ]
#             #     exact_date_filter = True




# def search_available_future_listings_enhanced_v2(**filters) -> List[Dict[str, Any]]:
#     session = SessionLocal()
#     try:
#         query = (
#             session.query(
#                 PtRtListing.id,
#                 PtRtListing.resort_id,
#                 PtRtListing.resort_name,
#                 PtRtListing.resort_slug,
#                 PtRtListing.listing_check_in,
#                 PtRtListing.listing_check_out,
#                 PtRtListing.listing_price_night,
#                 PtRtListing.listing_cancelation_policy_option,
#                 PtRtListing.listing_cancelation_date,
#                 PtRtListing.unit_type_name,
#                 UnitType.sleeps,
#                 UnitType.name.label("unit_type_name"),
#                 UnitType.id.label("unit_type_id"),
#             )
#             .join(UnitType, PtRtListing.unit_type_id == UnitType.id)
#             .distinct()
#         )

#         filter_conditions = []

#         # ---------------- Resort name filter ----------------
#         resort_name = filters.get("resort_name")
#         if resort_name:
#             filter_conditions.append(PtRtListing.resort_name.ilike(f"%{resort_name.strip()}%"))
            

#         # ---------------- Non-date filters ----------------
#         skip_fields = {
#             "year", "month", "day", "listing_check_in", "listing_check_out",
#             "price_sort", "limit", "update_fields", "min_guests", "resort_name"
#         }
#         for field_name, value in filters.items():
#             if value is not None and hasattr(PtRtListing, field_name) and field_name not in skip_fields:
#                 column = getattr(PtRtListing, field_name)
#                 filter_conditions.append(
#                     column.ilike(f"%{value.strip()}%") if isinstance(value, str) else column == value
#                 )

#         # ---------------- Date filters ----------------
#         check_in_str = filters.get("listing_check_in")
#         check_out_str = filters.get("listing_check_out")
#         year = filters.get("year")
#         month = filters.get("month")
#         day = filters.get("day")

#         try:
#             if check_in_str and check_out_str:
#                 # ✅ Exact match for specified dates
#                 ci_str, co_str = normalize_future_dates(check_in_str, check_out_str)
#                 check_in_date = datetime.strptime(ci_str, "%Y-%m-%d")
#                 check_out_date = datetime.strptime(co_str, "%Y-%m-%d")

#                 filter_conditions += [
#                     PtRtListing.listing_check_in == check_in_date,
#                     PtRtListing.listing_check_out == check_out_date,
#                 ]

#             elif month and not check_in_str and not check_out_str:
#                 # ✅ Month filtering (range)
#                 ci_str, co_str = get_month_year_range(month, year)
#                 check_in_start = datetime.strptime(ci_str, "%Y-%m-%d")
#                 check_in_end = datetime.strptime(co_str, "%Y-%m-%d")

#                 if day:
#                     # ✅ Exact single date in month
#                     specific_date = datetime(int(year), int(month), int(day))
#                     filter_conditions += [
#                         PtRtListing.listing_check_in == specific_date,
#                         PtRtListing.listing_check_out == specific_date,
#                     ]
#                 else:
#                     # ✅ Whole month range
#                     filter_conditions += [
#                         PtRtListing.listing_check_in >= check_in_start,
#                         PtRtListing.listing_check_in <= check_in_end,
#                     ]

#             elif year or month or day:
#                 # ✅ Partial date (only year, or year+month, etc.)
#                 col = PtRtListing.listing_check_in
#                 conditions = []
#                 if year: conditions.append(extract("year", col) == int(year))
#                 if month: conditions.append(extract("month", col) == int(month))
#                 if day: conditions.append(extract("day", col) == int(day))
#                 if conditions:
#                     filter_conditions.append(and_(*conditions))

#         except ValueError as ve:
#             print(f"⚠ Date parsing error: {ve}")


#         # # ---------------- Guests filter ----------------
#         # min_guests = filters.get("min_guests")
#         # if min_guests:
#         #     try:
#         #         min_guests = int(min_guests)
#         #         query = query.filter(func.abs(UnitType.sleeps) >= min_guests)
#         #     except ValueError:
#         #         print(f"⚠ Invalid min_guests value: {filters['min_guests']}")


#         # ---------------- Guests filter ----------------
#         min_guests = filters.get("min_guests")
#         if min_guests:
#             try:
#                 min_guests = int(min_guests)
#                 query = query.filter(func.abs(UnitType.sleeps) >= min_guests)
#             except ValueError:
#                 print(f"⚠ Invalid min_guests value: {filters['min_guests']}")

#         # ---------------- Unit type slug filter ----------------
#         unit_type_name = filters.get("unit_type_slug")
#         if unit_type_name:
#             try:
#                 unit_type_name = str(unit_type_name).strip()
#                 filter_conditions.append(PtRtListing.unit_type_name.ilike(f"%{unit_type_name}%"))
#             except Exception as e:
#                 print(f"⚠ Error filtering by unit_type_name: {e}")


#         # ---------------- Apply collected filters ----------------
#         if filter_conditions:
#             query = query.filter(and_(*filter_conditions))

#         # ---------------- Price sorting ----------------
#         price_sort = filters.get("price_sort", "asc")
#         price_col_numeric = cast(PtRtListing.listing_price_night, Numeric)

#         if price_sort == "asc":
#             query = query.order_by(asc(func.abs(price_col_numeric)))
#         elif price_sort == "desc":
#             query = query.order_by(desc(func.abs(price_col_numeric)))
#         elif price_sort == "cheapest":
#             query = query.filter(func.abs(price_col_numeric) <= 333).order_by(asc(func.abs(price_col_numeric)))
#         elif price_sort == "average":
#             query = query.filter(func.abs(price_col_numeric).between(334, 666)).order_by(asc(func.abs(price_col_numeric)))
#         elif price_sort == "highest":
#             query = query.filter(func.abs(price_col_numeric) >= 667).order_by(desc(func.abs(price_col_numeric)))

#         # ---------------- Limit ----------------
#         limit = int(filters.get("limit", 10))
#         results = query.limit(limit).all()
#         # print("ruban",query)

#         # ---------------- Build Structured Result ----------------
#         results_list = []
#         for row in results:
#             cancel_date_raw = row.listing_cancelation_date
#             cancel_date = (
#                 str(cancel_date_raw).split(" ")[0]
#                 if cancel_date_raw and cancel_date_raw not in ["0000-00-00", "0000-00-00 00:00:00", None, ""]
#                 else "Date not specified"
#             )
#             policy_desc = CANCELLATION_POLICY_DESCRIPTIONS.get(
#                 row.listing_cancelation_policy_option, "Policy not specified"
#             )
#             slug = row.resort_slug or slugify_resort_name(row.resort_name) if row.resort_name else None
#             resort_url = f"{BASE_LIST_URL}{slug}?startD=&endD=&adults=0&months=&dateOption=7" if slug else None
#             booking_url = None
#             if slug and row.id and row.listing_check_in and row.listing_check_out:
#                 booking_url = (
#                     f"{BASE_LIST_URL}{slug}"
#                     f"?startD={row.listing_check_in.strftime('%Y-%m-%d')}"
#                     f"&endD={row.listing_check_out.strftime('%Y-%m-%d')}"
#                     f"&adults=0&months=&dateOption=7"
#                 )

#             display_price = (
#                 f"from ${row.listing_price_night} per night"
#                 if row.listing_price_night else "Price not available"
#             )

#             results_list.append({
#                 "resort_id": row.resort_id,
#                 "resort_name": row.resort_name,
#                 "unit_type": row.unit_type_name,
#                 "sleeps": int(row.sleeps) if row.sleeps is not None else None,
#                 "check_in": row.listing_check_in.strftime("%Y-%m-%d") if row.listing_check_in else None,
#                 "check_out": row.listing_check_out.strftime("%Y-%m-%d") if row.listing_check_out else None,
#                 "price_per_night": display_price,
#                 "cancellation_policy_description": policy_desc,
#                 "listing_cancelation_date": cancel_date,
#                 "cancellation_info": f"{policy_desc} (By {cancel_date})",
#                 "resort_url": resort_url,
#                 "booking_url": booking_url
#             })

#         return results_list

#     except Exception as e:
#         print(f"❌ Error in search_available_future_listings_enhanced_v2: {str(e)}")
#         session.rollback()
#         return []
#     finally:
#         session.close()



# def search_available_future_listings_enhanced_v2(**filters) -> List[Dict[str, Any]]:
#     session = SessionLocal()
#     try:
#         query = (
#             session.query(
#                 PtRtListing.id,
#                 PtRtListing.resort_id,
#                 PtRtListing.resort_name,
#                 PtRtListing.resort_slug,
#                 PtRtListing.listing_check_in,
#                 PtRtListing.listing_check_out,
#                 PtRtListing.listing_price_night,
#                 PtRtListing.listing_cancelation_policy_option,
#                 PtRtListing.listing_cancelation_date,
#                 PtRtListing.unit_type_name,   # ✅ keep this
#                 UnitType.sleeps,              # ✅ from UnitType
#                 UnitType.id.label("unit_type_id"),
#             )
#             .join(UnitType, PtRtListing.unit_type_id == UnitType.id)
#             .distinct()
#         )
#         print("ruban_top",query)

#         filter_conditions = []

#         # ---------------- Resort name filter ----------------
#         resort_name = filters.get("resort_name")
#         if resort_name:
#             filter_conditions.append(PtRtListing.resort_name.ilike(f"%{resort_name.strip()}%"))

#         # ---------------- Non-date filters ----------------
#         skip_fields = {
#             "year", "month", "day", "listing_check_in", "listing_check_out",
#             "price_sort", "limit", "update_fields", "min_guests",
#             "resort_name", "unit_type_slug","unit_type_name"  # ✅ skip custom handled
#         }
#         for field_name, value in filters.items():
#             if value is not None and hasattr(PtRtListing, field_name) and field_name not in skip_fields:
#                 column = getattr(PtRtListing, field_name)
#                 filter_conditions.append(
#                     column.ilike(f"%{value.strip()}%") if isinstance(value, str) else column == value
#                 )

#         # ---------------- Date filters ----------------
#         check_in_str = filters.get("listing_check_in")
#         check_out_str = filters.get("listing_check_out")
#         year = filters.get("year")
#         month = filters.get("month")
#         day = filters.get("day")

#         try:
#             if check_in_str and check_out_str:
#                 ci_str, co_str = normalize_future_dates(check_in_str, check_out_str)
#                 check_in_date = datetime.strptime(ci_str, "%Y-%m-%d")
#                 check_out_date = datetime.strptime(co_str, "%Y-%m-%d")
#                 filter_conditions += [
#                     PtRtListing.listing_check_in == check_in_date,
#                     PtRtListing.listing_check_out == check_out_date,
#                 ]
#             elif month and not check_in_str and not check_out_str:
#                 ci_str, co_str = get_month_year_range(month, year)
#                 check_in_start = datetime.strptime(ci_str, "%Y-%m-%d")
#                 check_in_end = datetime.strptime(co_str, "%Y-%m-%d")
#                 if day:
#                     specific_date = datetime(int(year), int(month), int(day))
#                     filter_conditions += [
#                         PtRtListing.listing_check_in == specific_date,
#                         PtRtListing.listing_check_out == specific_date,
#                     ]
#                 else:
#                     filter_conditions += [
#                         PtRtListing.listing_check_in >= check_in_start,
#                         PtRtListing.listing_check_in <= check_in_end,
#                     ]
#             elif year or month or day:
#                 col = PtRtListing.listing_check_in
#                 conditions = []
#                 if year: conditions.append(extract("year", col) == int(year))
#                 if month: conditions.append(extract("month", col) == int(month))
#                 if day: conditions.append(extract("day", col) == int(day))
#                 if conditions:
#                     filter_conditions.append(and_(*conditions))
#         except ValueError as ve:
#             print(f"⚠ Date parsing error: {ve}")

#         # ---------------- Guests filter ----------------
#         min_guests = filters.get("min_guests")
#         if min_guests:
#             try:
#                 min_guests = int(min_guests)
#                 query = query.filter(func.abs(UnitType.sleeps) >= min_guests)
#             except ValueError:
#                 print(f"⚠ Invalid min_guests value: {filters['min_guests']}")

#         from sqlalchemy import or_

#         # ---------------- Unit type slug filter ----------------
#         unit_type_name = filters.get("unit_type_name")
#         if unit_type_name:
#             try:
#                 unit_type_name = str(unit_type_name).strip()
#                 filter_conditions.append(PtRtListing.unit_type_name.ilike(f"%{unit_type_name}%"))
#             except Exception as e:
#                 print(f"⚠ Error filtering by unit_type_name: {e}")


#         # ---------------- Apply collected filters ----------------
#         if filter_conditions:
#             query = query.filter(and_(*filter_conditions))
#             print("ruban1",query)

#         # ---------------- Price sorting ----------------
#         price_sort = filters.get("price_sort", "asc")
#         price_col_numeric = cast(PtRtListing.listing_price_night, Numeric)

#         if price_sort == "asc":
#             query = query.order_by(asc(func.abs(price_col_numeric)))
#             print("ruban_p)",query)
#         elif price_sort == "desc":
#             query = query.order_by(desc(func.abs(price_col_numeric)))
#         elif price_sort == "cheapest":
#             query = query.filter(func.abs(price_col_numeric) <= 333).order_by(asc(func.abs(price_col_numeric)))
#         elif price_sort == "average":
#             query = query.filter(func.abs(price_col_numeric).between(334, 666)).order_by(asc(func.abs(price_col_numeric)))
#         elif price_sort == "highest":
#             query = query.filter(func.abs(price_col_numeric) >= 667).order_by(desc(func.abs(price_col_numeric)))
#             print("ruban",query)

#         query = query.limit(80)    

#         # ---------------- Limit ----------------
#         limit = int(filters.get("limit", 10))
#         results = query.limit(limit).all()

#         # ---------------- Build Structured Result ----------------
#         results_list = []
#         for row in results:
#             cancel_date_raw = row.listing_cancelation_date
#             cancel_date = (
#                 str(cancel_date_raw).split(" ")[0]
#                 if cancel_date_raw and cancel_date_raw not in ["0000-00-00", "0000-00-00 00:00:00", None, ""]
#                 else "Date not specified"
#             )
#             policy_desc = CANCELLATION_POLICY_DESCRIPTIONS.get(
#                 row.listing_cancelation_policy_option, "Policy not specified"
#             )
#             slug = row.resort_slug or slugify_resort_name(row.resort_name) if row.resort_name else None
#             resort_url = f"{BASE_LIST_URL}{slug}?startD=&endD=&adults=0&months=&dateOption=7" if slug else None
#             booking_url = None
#             if slug and row.id and row.listing_check_in and row.listing_check_out:
#                 booking_url = (
#                     f"{BASE_LIST_URL}{slug}"
#                     f"?startD={row.listing_check_in.strftime('%Y-%m-%d')}"
#                     f"&endD={row.listing_check_out.strftime('%Y-%m-%d')}"
#                     f"&adults=0&months=&dateOption=7"
#                 )

#             display_price = (
#                 f"from ${row.listing_price_night} per night"
#                 if row.listing_price_night else "Price not available"
#             )

#             results_list.append({
#                 "resort_id": row.resort_id,
#                 "resort_name": row.resort_name,
#                 "unit_type_name": row.unit_type_name,   # ✅ from PtRtListing
#                 "sleeps": int(row.sleeps) if row.sleeps is not None else None,
#                 "check_in": row.listing_check_in.strftime("%Y-%m-%d") if row.listing_check_in else None,
#                 "check_out": row.listing_check_out.strftime("%Y-%m-%d") if row.listing_check_out else None,
#                 "price_per_night": display_price,
#                 "cancellation_policy_description": policy_desc,
#                 "listing_cancelation_date": cancel_date,
#                 "cancellation_info": f"{policy_desc} (By {cancel_date})",
#                 "resort_url": resort_url,
#                 "booking_url": booking_url
#             })

#         return results_list

#     except Exception as e:
#         print(f"❌ Error in search_available_future_listings_enhanced_v2: {str(e)}")
#         session.rollback()
#         return []
#     finally:
#         session.close()





def search_available_future_listings_merged(**filters) -> List[Dict[str, Any]]:
    session = SessionLocal()
    try:
        # ---------------- Base query ----------------
        query = (
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
                # ✅ From v2
                PtRtListing.unit_type_name,
                # ✅ From v1
                UnitType.sleeps,
                UnitType.name.label("unit_type_name_fallback"),
                UnitType.id.label("unit_type_id"),
            )
            .join(UnitType, PtRtListing.unit_type_id == UnitType.id)
            .distinct()
        )

        filter_conditions = []

        # ---------------- Resort name filter (v2) ----------------
        resort_name = filters.get("resort_name")
        if resort_name:
            filter_conditions.append(PtRtListing.resort_name.ilike(f"%{resort_name.strip()}%"))

        # ---------------- Total count listings with filter ----------------
        total_count_listings = (
            session.query(
                PtRtListing.resort_id,
                func.count(PtRtListing.id).label("count")
            )
            .filter(*filter_conditions)   # Apply full filters (resort_name, dates, etc.)
            .group_by(PtRtListing.resort_id)
            .all()
        )

        # ---------------- Unit type counts (separate filtering) ----------------
        unit_type_filters = [f for f in filter_conditions if not f.left.key == "unit_type_name"]

        unit_type_counts = (
            session.query(
                PtRtListing.unit_type_name,
                func.count(PtRtListing.id).label("count")
            )
            .filter(*unit_type_filters)   # Exclude explicit unit_type_name filter
            .group_by(PtRtListing.unit_type_name)
            .all()
        )
        
        # unit_type_breakdown = [ut[1] for ut in unit_type_counts]

        # Convert unit_type_counts query result into dict list
        unit_type_breakdown = [
            {"unit_type_name": ut[0], "listing_count": ut[1]}
            for ut in unit_type_counts
        ]

        # print("ruban_total_count_listings", total_count_listings)
        # print("ruban_unit_type_counts", unit_type_counts)
        print("ruban_unit_type_breakdown", unit_type_breakdown)



        # ---------------- Non-date filters ----------------
        skip_fields = {
            "year", "month", "day", "listing_check_in", "listing_check_out",
            "price_sort", "limit", "update_fields", "min_guests",
            "resort_name", "unit_type_name"
        }
        for field_name, value in filters.items():
            if value is not None and hasattr(PtRtListing, field_name) and field_name not in skip_fields:
                column = getattr(PtRtListing, field_name)
                filter_conditions.append(
                    column.ilike(f"%{value.strip()}%") if isinstance(value, str) else column == value
                )

        # ---------------- Date filters (v1 + v2 merged) ----------------
        check_in_str = filters.get("listing_check_in")
        check_out_str = filters.get("listing_check_out")
        year = filters.get("year")
        month = filters.get("month")
        day = filters.get("day")

        try:
            if check_in_str and check_out_str:
                ci_str, co_str = normalize_future_dates(check_in_str, check_out_str)
                check_in_date = datetime.strptime(ci_str, "%Y-%m-%d")
                check_out_date = datetime.strptime(co_str, "%Y-%m-%d")
                filter_conditions += [
                    PtRtListing.listing_check_in == check_in_date,
                    PtRtListing.listing_check_out == check_out_date,
                ]
            elif month and not check_in_str and not check_out_str:
                ci_str, co_str = get_month_year_range(month, year)
                check_in_start = datetime.strptime(ci_str, "%Y-%m-%d")
                check_in_end = datetime.strptime(co_str, "%Y-%m-%d")
                if day:
                    specific_date = datetime(int(year), int(month), int(day))
                    filter_conditions += [
                        PtRtListing.listing_check_in == specific_date,
                        PtRtListing.listing_check_out == specific_date,
                    ]
                else:
                    filter_conditions += [
                        PtRtListing.listing_check_in >= check_in_start,
                        PtRtListing.listing_check_in <= check_in_end,
                    ]
            elif year or month or day:
                col = PtRtListing.listing_check_in
                conditions = []
                if year: conditions.append(extract("year", col) == int(year))
                if month: conditions.append(extract("month", col) == int(month))
                if day: conditions.append(extract("day", col) == int(day))
                if conditions:
                    filter_conditions.append(and_(*conditions))
        except ValueError as ve:
            print(f"⚠ Date parsing error: {ve}")

        # ---------------- Guests filter ----------------
        min_guests = filters.get("min_guests")
        if min_guests:
            try:
                min_guests = int(min_guests)
                query = query.filter(func.abs(UnitType.sleeps) >= min_guests)
            except ValueError:
                print(f"⚠ Invalid min_guests value: {filters['min_guests']}")

        # ---------------- Unit type name filter (v2) ----------------
        unit_type_name = filters.get("unit_type_name")
        if unit_type_name:
            try:
                filter_conditions.append(PtRtListing.unit_type_name.ilike(f"%{str(unit_type_name).strip()}%"))
            except Exception as e:
                print(f"⚠ Error filtering by unit_type_name: {e}")


        # # ---------------- Unit type name filter (v2) ----------------
        # unit_type_name = filters.get("unit_type_name")
        # query = session.query(PtRtListing)

        # if unit_type_name:
        #     try:
        #         query = query.filter(
        #             PtRtListing.unit_type_name.ilike(f"%{str(unit_type_name).strip()}%")
        #         )
        #     except Exception as e:
        #         print(f"⚠ Error filtering by unit_type_name: {e}")

        # # Always apply fixed limit
        # results = query.limit(20).all()
        # print("ruban_unit_type_name_filter_results", results)


        # # ---------------- Unit type count listings with filter ----------------
        # unit_type_counts = (
        #     session.query(
        #         PtRtListing.unit_type_name,
        #         func.count(PtRtListing.id).label("count")
        #     )
        #     .filter(*filter_conditions)   # apply existing filters (resort_name, etc.)
        #     .group_by(PtRtListing.unit_type_name)
        #     .all()
        # )

        # print("ruban_unit_type_counts", unit_type_counts)



        # # ---------------- Unit type name filter (v2) ----------------
        # unit_type_name = filters.get("unit_type_name")
        # if unit_type_name:
        #     try:
        #         filter_conditions.append(
        #             PtRtListing.unit_type_name.ilike(f"%{str(unit_type_name).strip()}%")
        #         )
        #     except Exception as e:
        #         print(f"⚠ Error filtering by unit_type_name: {e}")

        # # ---------------- Unit type count listings ----------------
        # try:
        #     # ✅ Only apply "other" filters (exclude the direct unit_type_name filter)
        #     base_conditions = [fc for fc in filter_conditions if not str(fc).startswith("PtRtListing.unit_type_name")]

        #     unit_type_counts = (
        #         session.query(
        #             PtRtListing.unit_type_name,
        #             func.count(PtRtListing.id).label("count")
        #         )
        #         .filter(*base_conditions)   # apply resort_name, guests, etc.
        #         .group_by(PtRtListing.unit_type_name)
        #         .all()
        #     )

        #     print("ruban_unit_type_counts", unit_type_counts)
        # except Exception as e:
        #     print(f"⚠ Error fetching unit_type_counts: {e}")

                

        # ---------------- Apply collected filters ----------------
        if filter_conditions:
            query = query.filter(and_(*filter_conditions))

        # ---------------- Price sorting (v1 + v2 merged) ----------------
        price_sort = filters.get("price_sort", "asc")
        price_col_numeric = cast(PtRtListing.listing_price_night, Numeric)

        default_limit = 80
        if price_sort == "asc":
            query = query.order_by(asc(func.abs(price_col_numeric)))
            default_limit = 80
        elif price_sort == "desc":
            query = query.order_by(desc(func.abs(price_col_numeric)))
            default_limit = 85
        elif price_sort == "cheapest":
            query = query.filter(func.abs(price_col_numeric) <= 333).order_by(asc(func.abs(price_col_numeric)))
            default_limit = 80
        elif price_sort == "average":
            query = query.filter(func.abs(price_col_numeric).between(334, 666)).order_by(asc(func.abs(price_col_numeric)))
            default_limit = 80
        elif price_sort == "highest":
            query = query.filter(func.abs(price_col_numeric) >= 667).order_by(desc(func.abs(price_col_numeric)))
            default_limit = 85

        # ---------------- Limit ----------------
        limit = int(filters.get("limit", default_limit))
        results = query.limit(limit).all()

        # ---------------- Build Structured Result ----------------
        results_list = []
        for row in results:
            cancel_date_raw = row.listing_cancelation_date
            cancel_date = (
                str(cancel_date_raw).split(" ")[0]
                if cancel_date_raw and cancel_date_raw not in ["0000-00-00", "0000-00-00 00:00:00", None, ""]
                else "Date not specified"
            )
            policy_desc = CANCELLATION_POLICY_DESCRIPTIONS.get(
                row.listing_cancelation_policy_option, "Policy not specified"
            )
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

            display_price = (
                f"from ${row.listing_price_night} per night"
                if row.listing_price_night else "Price not available"
            )

            results_list.append({
                "resort_id": row.resort_id,
                "resort_name": row.resort_name,
                "unit_type_name": row.unit_type_name or row.unit_type_name_fallback,
                "sleeps": int(row.sleeps) if row.sleeps is not None else None,
                "check_in": row.listing_check_in.strftime("%Y-%m-%d") if row.listing_check_in else None,
                "check_out": row.listing_check_out.strftime("%Y-%m-%d") if row.listing_check_out else None,
                "price_per_night": display_price,
                "cancellation_policy_description": policy_desc,
                "listing_cancelation_date": cancel_date,
                "cancellation_info": f"{policy_desc} (By {cancel_date})",
                "resort_url": resort_url,
                "booking_url": booking_url,
               
            })

        # ✅ Wrap everything in one dict
        final_result = {
            "results": results_list,
            "unit_type_breakdown": unit_type_breakdown,
            "total_listings_for_resort": next(
                (item.count for item in total_count_listings if item.resort_id == row.resort_id), 0
            ),
            "total_unit_for_resort": sum(ut[1] for ut in unit_type_counts)
        }


        return final_result

    except Exception as e:
        print(f"❌ Error in search_available_future_listings_merged: {str(e)}")
        session.rollback()
        return {"results": [], "unit_type_breakdown": {}}

    finally:
        session.close()


#----------search_avaliable_future..... end 




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
                "user_email":User.email,
                "resort_name": booking.listing.resort.name,
                "resort_city": booking.listing.resort.city,
                "resort_country": booking.listing.resort.country,
                "unit_type": booking.listing.unit_type.name,
                "nights": booking.listing.nights,
                "check_in": check_in.strftime("%Y-%m-%d"),
                "check_out": booking.listing.check_out.strftime("%Y-%m-%d"),
                "reservation_no":booking.listing.reservation_no,
                # "price_per_night": f"${booking.price_night:.2f}",
                # "total_price": f"${booking.total_price:.2f}",
                # "total_listing_price": f"${booking.booking_metrics.total_listing_price :.2f}",
                "total_booking_price": f"${booking.booking_metrics.total_booking_price:.2f}",
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
        print(f"Error in get_user_bookings: {str(e)}")
        return {
            "upcoming_bookings": [],
            "past_bookings": [],
            "summary": {},
            "error": str(e)
        }

    finally:
        session.close()



# def search_available_future_listings_merged(**filters) -> List[Dict[str, Any]]:
#     session = SessionLocal()
#     try:
#         # ---------------- Base query ----------------
#         query = (
#             session.query(
#                 PtRtListing.id,
#                 PtRtListing.resort_id,
#                 PtRtListing.resort_name,
#                 PtRtListing.resort_slug,
#                 PtRtListing.listing_check_in,
#                 PtRtListing.listing_check_out,
#                 PtRtListing.listing_price_night,
#                 PtRtListing.listing_cancelation_policy_option,
#                 PtRtListing.listing_cancelation_date,
#                 # ✅ From v2
#                 PtRtListing.unit_type_name,
#                 # ✅ From v1
#                 UnitType.sleeps,
#                 UnitType.name.label("unit_type_name_fallback"),
#                 UnitType.id.label("unit_type_id"),
#             )
#             .join(UnitType, PtRtListing.unit_type_id == UnitType.id)
#             .distinct()
#         )

#         filter_conditions = []



#         # ---------------- Resort name filter (v2) ----------------
#         resort_name = filters.get("resort_name")
#         if resort_name:
#             filter_conditions.append(
#                 PtRtListing.resort_name.ilike(f"%{resort_name.strip()}%")
#             )

#         # Date logic
#         today = datetime.date.today()
#         ninety_days = today + datetime.timedelta(days=90)

#         # Priority ordering: listings in [today, today+90] come first
#         priority_case = case(
#             (
#                 (PtRtListing.listing_check_in.between(today, ninety_days), 0),
#             ),
#             else_=1
#         ).label("date_priority")

#         # Apply ordering so that 90-day listings appear first
#         query = (
#             session.query(PtRtListing)
#             .filter(*filter_conditions)
#             .order_by(priority_case, PtRtListing.listing_check_in.asc())
#         )
#         print("ruban_top",query)


#         # ---------------- Total count listings with filter ----------------
#         total_count_listings = (
#             session.query(
#                 PtRtListing.resort_id,
#                 func.count(PtRtListing.id).label("count")
#             )
#             .filter(*filter_conditions)   # Apply full filters (resort_name, dates, etc.)
#             .group_by(PtRtListing.resort_id)
#             .all()
#         )

#         # ---------------- Unit type counts (separate filtering) ----------------
#         unit_type_filters = [f for f in filter_conditions if not f.left.key == "unit_type_name"]

#         unit_type_counts = (
#             session.query(
#                 PtRtListing.unit_type_name,
#                 func.count(PtRtListing.id).label("count")
#             )
#             .filter(*unit_type_filters)   # Exclude explicit unit_type_name filter
#             .group_by(PtRtListing.unit_type_name)
#             .all()
#         )
#         unit_type_breakdown = [ut[1] for ut in unit_type_counts]

#         # ---------------- Non-date filters ----------------
#         skip_fields = {
#             "year", "month", "day", "listing_check_in", "listing_check_out",
#             "price_sort", "limit", "update_fields", "min_guests",
#             "resort_name", "unit_type_name"
#         }
#         for field_name, value in filters.items():
#             if value is not None and hasattr(PtRtListing, field_name) and field_name not in skip_fields:
#                 column = getattr(PtRtListing, field_name)
#                 filter_conditions.append(
#                     column.ilike(f"%{value.strip()}%") if isinstance(value, str) else column == value
#                 )

#         # ---------------- Date filters (v1 + v2 merged) ----------------
#         check_in_str = filters.get("listing_check_in")
#         check_out_str = filters.get("listing_check_out")
#         year = filters.get("year")
#         month = filters.get("month")
#         day = filters.get("day")

#         try:
#             if check_in_str and check_out_str:
#                 ci_str, co_str = normalize_future_dates(check_in_str, check_out_str)
#                 check_in_date = datetime.strptime(ci_str, "%Y-%m-%d")
#                 check_out_date = datetime.strptime(co_str, "%Y-%m-%d")
#                 filter_conditions += [
#                     PtRtListing.listing_check_in == check_in_date,
#                     PtRtListing.listing_check_out == check_out_date,
#                 ]
#             elif month and not check_in_str and not check_out_str:
#                 ci_str, co_str = get_month_year_range(month, year)
#                 check_in_start = datetime.strptime(ci_str, "%Y-%m-%d")
#                 check_in_end = datetime.strptime(co_str, "%Y-%m-%d")
#                 if day:
#                     specific_date = datetime(int(year), int(month), int(day))
#                     filter_conditions += [
#                         PtRtListing.listing_check_in == specific_date,
#                         PtRtListing.listing_check_out == specific_date,
#                     ]
#                 else:
#                     filter_conditions += [
#                         PtRtListing.listing_check_in >= check_in_start,
#                         PtRtListing.listing_check_in <= check_in_end,
#                     ]
#             elif year or month or day:
#                 col = PtRtListing.listing_check_in
#                 conditions = []
#                 if year: conditions.append(extract("year", col) == int(year))
#                 if month: conditions.append(extract("month", col) == int(month))
#                 if day: conditions.append(extract("day", col) == int(day))
#                 if conditions:
#                     filter_conditions.append(and_(*conditions))
#         except ValueError as ve:
#             print(f"⚠ Date parsing error: {ve}")

#         # ---------------- Guests filter ----------------
#         min_guests = filters.get("min_guests")
#         if min_guests:
#             try:
#                 min_guests = int(min_guests)
#                 query = query.filter(func.abs(UnitType.sleeps) >= min_guests)
#             except ValueError:
#                 print(f"⚠ Invalid min_guests value: {filters['min_guests']}")

#         # ---------------- Unit type name filter (v2) ----------------
#         unit_type_name = filters.get("unit_type_name")
#         if unit_type_name:
#             try:
#                 filter_conditions.append(PtRtListing.unit_type_name.ilike(f"%{str(unit_type_name).strip()}%"))
#             except Exception as e:
#                 print(f"⚠ Error filtering by unit_type_name: {e}")

#         # ---------------- Apply collected filters ----------------
#         if filter_conditions:
#             query = query.filter(and_(*filter_conditions))

#         # ---------------- Price sorting (v1 + v2 merged) ----------------
#         price_sort = filters.get("price_sort", "asc")
#         price_col_numeric = cast(PtRtListing.listing_price_night, Numeric)

#         default_limit = 80
#         if price_sort == "asc":
#             query = query.order_by(asc(func.abs(price_col_numeric)))
#             default_limit = 80
#         elif price_sort == "desc":
#             query = query.order_by(desc(func.abs(price_col_numeric)))
#             default_limit = 85
#         elif price_sort == "cheapest":
#             query = query.filter(func.abs(price_col_numeric) <= 333).order_by(asc(func.abs(price_col_numeric)))
#             default_limit = 80
#         elif price_sort == "average":
#             query = query.filter(func.abs(price_col_numeric).between(334, 666)).order_by(asc(func.abs(price_col_numeric)))
#             default_limit = 80
#         elif price_sort == "highest":
#             query = query.filter(func.abs(price_col_numeric) >= 667).order_by(desc(func.abs(price_col_numeric)))
#             default_limit = 85

#         # ---------------- Limit ----------------
#         limit = int(filters.get("limit", default_limit))
#         results = query.limit(limit).all()

#         # ---------------- Build Structured Result ----------------
#         results_list = []
#         for row in results:
#             cancel_date_raw = row.listing_cancelation_date
#             cancel_date = (
#                 str(cancel_date_raw).split(" ")[0]
#                 if cancel_date_raw and cancel_date_raw not in ["0000-00-00", "0000-00-00 00:00:00", None, ""]
#                 else "Date not specified"
#             )
#             policy_desc = CANCELLATION_POLICY_DESCRIPTIONS.get(
#                 row.listing_cancelation_policy_option, "Policy not specified"
#             )
#             slug = row.resort_slug or slugify_resort_name(row.resort_name) if row.resort_name else None
#             resort_url = f"{BASE_LIST_URL}{slug}?startD=&endD=&adults=0&months=&dateOption=7" if slug else None
#             booking_url = None
#             if slug and row.id and row.listing_check_in and row.listing_check_out:
#                 booking_url = (
#                     f"{BASE_LIST_URL}{slug}"
#                     f"?startD={row.listing_check_in.strftime('%Y-%m-%d')}"
#                     f"&endD={row.listing_check_out.strftime('%Y-%m-%d')}"
#                     f"&adults=0&months=&dateOption=7"
#                 )

#             display_price = (
#                 f"from ${row.listing_price_night} per night"
#                 if row.listing_price_night else "Price not available"
#             )

#             results_list.append({
#                 "resort_id": row.resort_id,
#                 "resort_name": row.resort_name,
#                 # prefer PtRtListing.unit_type_name, fallback to UnitType.name
#                 "unit_type_name": row.unit_type_name or row.unit_type_name_fallback,
#                 "sleeps": int(row.sleeps) if row.sleeps is not None else None,
#                 "check_in": row.listing_check_in.strftime("%Y-%m-%d") if row.listing_check_in else None,
#                 "check_out": row.listing_check_out.strftime("%Y-%m-%d") if row.listing_check_out else None,
#                 "price_per_night": display_price,
#                 "cancellation_policy_description": policy_desc,
#                 "listing_cancelation_date": cancel_date,
#                 "cancellation_info": f"{policy_desc} (By {cancel_date})",
#                 "resort_url": resort_url,
#                 "booking_url": booking_url,
#                 "total_listings_for_resort": next((item.count for item in total_count_listings if item.resort_id == row.resort_id), 0),
#                 "total_unit_for_resort": sum(ut[1] for ut in unit_type_counts),
#                 "unit_type_breakdown": unit_type_breakdown   # <--- added here}
#             })

#         return results_list

#     except Exception as e:
#         print(f"❌ Error in search_available_future_listings_merged: {str(e)}")
#         session.rollback()
#         return []
#     finally:
#         session.close()

        



def get_available_resorts(
    country: str = None,
    city: str = None,
    state: str = None,
    resort_status: str = "active",
    limit: int = 10,
    location_type: str = None
) -> List[Dict[str, Any]]:
    """
    List top resorts from ResortMigration filtered by location and sorted
    by number of active listings.
    """
    with SessionLocal() as session:
        try:
            # Subquery: top 80 resorts by active pt_rt_listings
            listing_subq = (
                session.query(
                    PtRtListing.resort_id,
                    func.count(PtRtListing.id).label("active_count")
                )
                .filter(
                    PtRtListing.listing_status == "active",   # equivalent to Listing.status
                    PtRtListing.listing_has_deleted == 0      # equivalent to has_deleted = 0
                )
                .group_by(PtRtListing.resort_id)
                .order_by(func.count(PtRtListing.id).desc())
                .subquery()
            )
            print("ruban_sub",listing_subq)


            # Join ResortMigration with listing counts
            query = (
                session.query(ResortMigration, listing_subq.c.active_count)
                .join(listing_subq, ResortMigration.resort_id == listing_subq.c.resort_id)
                .filter(ResortMigration.resort_has_deleted == 0)
                .filter(ResortMigration.resort_status == resort_status)
            )
            print("ruban_query_resort",query)

            # Apply optional filters
            if country:
                query = query.filter(ResortMigration.country.ilike(f"%{country.strip()}%"))
                print("ruban_country",query)
            if city:
                query = query.filter(ResortMigration.city.ilike(f"%{city.strip()}%"))
                print("ruban_city",query)
            if state:
                query = query.filter(ResortMigration.state.ilike(f"%{state.strip()}%"))
                print("ruban_state",query)
            if country:
                query = query.filter(ResortMigration.country.ilike(f"%{country.strip()}%"))
                print("ruban_country",query)
            if location_type:
                query = query.filter(ResortMigration.location_types.ilike(f"%{location_type.strip()}%"))
                print("ruban_location",query)

            # Fetch results ordered by active_count and limited by `limit`
            resorts = query.order_by(listing_subq.c.active_count.desc()).all()
            print("count",resorts)
            print("ruban",query)

            # Format results
            result = []
            for resort, active_count in resorts:
                result.append({
                    "id": resort.id,
                    "resort_id": resort.resort_id,
                    "resort_name": resort.resort_name,
                    "city": resort.city,
                    "state": resort.state,
                    "country": resort.country,
                    "address": resort.address,
                    "resort_slug": resort.resort_slug,
                    "location_types": [t.strip() for t in resort.location_types.split(",")] if resort.location_types else [],
                    "resort_status": resort.resort_status,
                    "resort_google_rating": resort.resort_google_rating,
                    
                })

            return result

        except Exception as e:
            print(f"Error in get_available_resorts: {e}")
            return []




# BASE_URL = "https://dev.go-koala.com/uploads/resorts"
BASE_URL = "https://koalaadmin-prod.s3.us-east-2.amazonaws.com/uploads/resorts" # live url
def get_resort_details(
    resort_id: Optional[int] = None,
    resort_name: Optional[str] = None,  
    amenities_list: Optional[List[str]] = None,
    amenities_only: bool = False,
    list_resorts_with_amenities: bool = False,
    limit: int = 5
) -> Dict[str, Any]:
    """
    Get resort details or filter resorts by amenities.
    Handles:
        1. list_resorts_with_amenities=True -> Returns all resorts with their amenities
        2. resort_id or resort_name -> Returns single resort details
        3. amenities_list -> Returns resorts that have ALL given amenities
    """
    session: Session = SessionLocal()
    try:
        # -------------------------
        # CASE 1: All resorts with amenities
        # -------------------------
        if list_resorts_with_amenities:
            resorts = session.query(Resort).filter(Resort.has_deleted == 0).all()
            return {
                "resorts_with_amenities": [
                    {
                        "resort_id": r.id,
                        "resort_name": r.name,
                        "amenities": [
                            {"id": a.id, "name": a.name}
                            for a in session.query(Amenity.id, Amenity.name)
                            .join(ResortAmenity, ResortAmenity.amenity_id == Amenity.id)
                            .filter(
                                ResortAmenity.resort_id == r.id,
                                or_(*[Amenity.name.ilike(f"%{amenity}%") for amenity in amenities_list])
                                if amenities_list else True
                            )
                            .all()
                        ]
                    }
                    for r in resorts
                ]
            }

        # -------------------------
        # CASE 2: Single resort details by ID or Name
        # -------------------------
        elif resort_id or resort_name:
            query = (
                session.query(Resort)
                .join(User, Resort.creator_id == User.id)
                .filter(Resort.has_deleted == 0)
            )
            print("ruban_top",query)
            if resort_id:
                query = query.filter(Resort.id == resort_id)
                print("ruban_detail_id",query)
            else:
                query = query.filter(Resort.name.ilike(f"%{resort_name.strip()}%"))
                print("ruban_detail_na",query)

            resort = query.first()
            if not resort:
                return {"error": "Resort not found with the given identifier."}

            amenities_data = [
                {"id": a.id, "name": a.name}
                for a in session.query(Amenity.id, Amenity.name)
                .join(ResortAmenity, ResortAmenity.amenity_id == Amenity.id)
                .filter(ResortAmenity.resort_id == resort.id)
                .all()
            ]

            if amenities_only:
                return {
                    "resort_id": resort.id,
                    "resort_name": resort.name,
                    "amenities": amenities_data
                }

            # Top image
            top_image = (
                session.query(ResortImage)
                .filter(ResortImage.resort_id == resort.id)
                .order_by(ResortImage.image_order.asc())
                .first()
            )
            image_data = (
                {
                    "id": top_image.id,
                    "filename": top_image.image,
                    "image_order": top_image.image_order,
                    "url": f"{BASE_URL}/{resort.id}/{top_image.image}"
                }
                if top_image and top_image.image
                else None
            )

            # Unit types
            unit_types = session.query(UnitType).filter(
                UnitType.resort_id == resort.id, UnitType.has_deleted == 0
            ).all()

            # Listings by status
            statuses = ['active', 'pending', 'booked', 'needs_fulfiment', 'fulfilment_request']
            listings_stats = {
                status: session.query(Listing).filter(
                    Listing.resort_id == resort.id,
                    Listing.has_deleted == 0,
                    Listing.status == status
                ).count()
                for status in statuses
            }

            # Total bookings
            total_bookings = session.query(Booking).join(
                Listing, Booking.listing_id == Listing.id
            ).filter(Listing.resort_id == resort.id).count()



            # Reviews
            reviews = (
                session.query(ResortReview)
                .filter(ResortReview.resort_id == resort.id)
                .order_by(ResortReview.rating.desc())  # highest rating first
                .limit(3)
                .all()
                 )
            print("ruban_revi",query)

            reviews_data = [
                {
                    "id": review.id,
                    "author_name": review.author_name,
                    "author_url": review.author_url,
                    "rating": review.rating,
                    "relative_time_description": review.relative_time_description,
                    "text": review.text,  
                  
                }
                for review in reviews
            ]


            return {
                "id": resort.id,
                "name": resort.name,
                "slug": resort.slug,
                "address": resort.address,
                "city": resort.city,
                "state": resort.state,
                "country": resort.country,
                "zip": resort.zip,
                "county": resort.county,
                # "lattitude": resort.lattitude,
                # "longitude": resort.longitude,
                "highlight_quote": resort.highlight_quote,
                "description": resort.description,
                "creator_name": f"{resort.creator.first_name} {resort.creator.last_name}",
                "creator_email": resort.creator.email,
                "status": resort.status,
                "unit_types": [
                    {"id": ut.id, "name": ut.name, "status": ut.status} for ut in unit_types
                ],
                "listings_by_status": listings_stats,
                "total_bookings": total_bookings,
                "top_image": image_data,
                "amenities": amenities_data,
                "reviews": reviews_data   # <--- added here
            }

        # -------------------------
        # CASE 3: Amenities-only search
        # -------------------------
        elif amenities_list:
            # Step 1: Find amenity IDs (case-insensitive)
            amenity_ids = [
                a[0]
                for a in session.query(Amenity.id)
                .filter(func.lower(Amenity.name).in_([name.lower() for name in amenities_list]))
                .all()
            ]
            # print("Amenities list:", amenities_list)
            # print("Amenity IDs:", amenity_ids)

            if not amenity_ids:
                return {"error": "No amenities found for the given names."}

            # Step 2: Resorts with these amenities
            query = session.query(ResortAmenity.resort_id).filter(
                ResortAmenity.amenity_id.in_(amenity_ids)
            )

            resort_ids = []
            if len(amenity_ids) > 0:
                resort_ids = (
                    session.query(ResortAmenity.resort_id)
                    .filter(
                        ResortAmenity.amenity_id.in_(amenity_ids),
                    )
                    # .distinct()
                    .limit(limit)
                    .all()
                )
                # print("rubi",resort_ids)
                # print("ruban",query)

            resort_ids = [r[0] for r in resort_ids]
            # print(resort_ids)


            # print("Resort IDs:", resort_ids)

            if not resort_ids:
                return {"error": "No resorts found with the given amenities."}


            # Step 3: Fetch resort details
            resorts = session.query(Resort).filter(
                Resort.id.in_(resort_ids), 
            ).limit(limit).all()

            return {
                "resorts": [
                    {
                        "resort_id": r.id,
                        "resort_name": r.name,
                        "amenities": [
                            {"id": a.id, "name": a.name}
                            for a in session.query(Amenity.id, Amenity.name)
                            .join(ResortAmenity, ResortAmenity.amenity_id == Amenity.id)
                            .filter(ResortAmenity.resort_id == r.id)
                            .all()
                        ]
                    }
                    for r in resorts
                ]
            }


        return {"error": "Please provide either resort_id, resort_name, or amenities_list."}

    except Exception as e:
        print(f"[ERROR] Failed to fetch resort details: {e}")
        return {"error": f"Exception occurred: {e}"}

    finally:
        session.close()





def get_user_profile(user_email: str) -> Dict[str, Any]:
    """Get user profile information."""
    session = SessionLocal()
    
    try:
        user = session.query(User)\
            .filter(User.email == user_email)\
            .filter(User.has_deleted == 0)\
            .first()
        
        if not user:
            return {"error": f"User with email {user_email} not found"}
        
        # Count user's bookings
        bookings_count = session.query(Booking)\
            .filter(Booking.user_id == user.id)\
            .count()
        
        # Count owned listings
        owned_listings_count = session.query(Booking)\
            .filter(Booking.owner_id == user.id)\
            .count()
        
        # Count created resorts
        created_resorts_count = session.query(Resort)\
            .filter(Resort.creator_id == user.id)\
            .filter(Resort.has_deleted == 0)\
            .count()
        
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "status": user.status,
            "total_bookings": bookings_count,
            "owned_listings": owned_listings_count,
            "created_resorts": created_resorts_count
        }
        
    except Exception as e:
        print(f"Error in get_user_profile: {str(e)}")
        return {"error": f"Error retrieving user profile: {str(e)}"}
        
    finally:
        session.close()




def search_resorts_by_amenities(
    amenities: List[str], 
    limit: int = 5, 
    match_all: bool = True  # True = AND, False = OR
) -> List[Dict[str, Any]]:
    session = SessionLocal()
    try:
        # Get amenity IDs from names (case-insensitive)
        amenity_ids = (
            session.query(Amenity.id)
            .filter(func.lower(Amenity.name).in_([name.lower() for name in amenities]))
            .all()
        )
        amenity_ids = [a[0] for a in amenity_ids]

        if not amenity_ids:
            return []

        if match_all:
            # AND logic → Resorts must have all amenities
            subquery = (
                session.query(ResortAmenity.resort_id)
                .filter(ResortAmenity.amenity_id.in_(amenity_ids))
                .group_by(ResortAmenity.resort_id)
                .having(func.count(func.distinct(ResortAmenity.amenity_id)) == len(amenity_ids))
                .subquery()
            )
            resorts_query = session.query(Resort).filter(Resort.id.in_(subquery))
        else:
            # OR logic → Resorts with at least one of the amenities
            resorts_query = (
                session.query(Resort)
                .join(ResortAmenity, Resort.id == ResortAmenity.resort_id)
                .filter(ResortAmenity.amenity_id.in_(amenity_ids))
                .distinct()
            )

        resorts = resorts_query.filter(Resort.has_deleted == 0).limit(limit).all()

        # Format results
        return [
            {
                "resort_id": r.id,
                "resort_name": r.name,
                "amenities": [ra.amenity.name for ra in r.resort_amenities]
            }
            for r in resorts
        ]

    finally:
        session.close()




# Tool function registry for easy lookup
AVAILABLE_TOOLS = {
    "get_user_bookings": get_user_bookings,
    "get_available_resorts": get_available_resorts,
    "get_resort_details": get_resort_details,
    # "search_available_future_listings_enhanced": search_available_future_listings_enhanced,
    # "search_available_future_listings_enhanced_v2": search_available_future_listings_enhanced_v2,
    "search_available_future_listings_merged": search_available_future_listings_merged,
    "get_city_from_resort":get_city_from_resort,
    "search_resorts_by_amenities": search_resorts_by_amenities,
    "get_user_profile": get_user_profile,
  
}

def call_tool(tool_name: str, **kwargs) -> Any:
    """
    Call a tool function by name with given arguments.
    
    Args:
        tool_name: Name of the tool to call
        **kwargs: Arguments to pass to the tool
        
    Returns:
        Result of the tool function call
    """
    if tool_name not in AVAILABLE_TOOLS:
        return {"error": f"Tool '{tool_name}' not found"}
    
    try:
        return AVAILABLE_TOOLS[tool_name](**kwargs)
    except Exception as e:
        return {"error": f"Error calling tool '{tool_name}': {str(e)}"}


if __name__ == "__main__":

    start_chatbot()
    # Test database connection
    print("🔧 Testing Database Connection...")
    conn_result = test_database_connection()
    print(f"Status: {conn_result['status']}")
    print(f"Message: {conn_result['message']}")
    
    if conn_result['status'] == 'success':
        print("\n✅ Database connection successful!")
        print("🔧 Available Tools:")
        for tool_name in AVAILABLE_TOOLS.keys():
            print(f"  - {tool_name}")
        
        # Test a few functions
        print("\n🧪 Testing Functions:")
        
        # Test get_available_resorts
        print("Testing get_available_resorts...")
        resorts = call_tool("get_available_resorts", limit=5)
        print(f"Found {len(resorts)} resorts")
        
    
        
        # Test search_resorts_by_amenities
        print("Testing search_resorts_by_amenities...")
        amenity_resorts = call_tool("search_resorts_by_amenities", amenities=["pool"], limit=5)
        print(f"Found {len(amenity_resorts)} resorts with pool amenity")
    else:
        print("\n❌ Database connection failed!")
        print("Please check your database configuration in the .env file")