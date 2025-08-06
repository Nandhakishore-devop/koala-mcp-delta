"""
Fixed Tool functions for resort booking system using SQLAlchemy with MySQL.
"""
from typing import List, Dict, Any, Optional,Union
from sqlalchemy import create_engine, Column, Integer,BigInteger, String, DateTime, ForeignKey, Text, Float, Boolean, and_, asc, desc
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, DateTime, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import json
import os
from datetime import datetime, timedelta 
from dotenv import load_dotenv
from collections import Counter, defaultdict
import calendar

# Load environment variables
load_dotenv()

# Database models
Base = declarative_base()


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
    has_deleted = Column(Integer, default=0)
    created_by = Column(Integer, default=0)
    updated_by = Column(Integer, default=0)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_key_amenity = Column(Integer, default=0)


class ResortMigration(Base):
    __tablename__ = 'resort_migration'

    id = Column(BigInteger, primary_key=True)
    pt_rt_id = Column(Integer, nullable=False)
    listing_id = Column(Integer)
    listing_check_in = Column(DateTime)
    listing_check_out = Column(DateTime)
    listing_cancelation_date = Column(DateTime)
    listing_price_night = Column(String(50))
    listing_nights = Column(Integer)
    listing_publish_type = Column(String(50))
    listing_has_deleted = Column(Integer, default=0)
    listing_status = Column(String(50))
    listing_currency_id = Column(Integer, default=0)
    listing_currency_code = Column(String(255))
    has_weekend = Column(Integer, default=0)
    listing_owner_id = Column(Integer, default=0)  # Remove ForeignKey to avoid issues
    listing_count = Column(Integer, default=0)
    unit_type_id = Column(Integer, default=0)  # Remove ForeignKey to avoid issues
    available_count = Column(String(255))
    exactlisting_listing_count = Column(String(255))
    unit_type_slug = Column(String(255))
    unit_type_name = Column(String(255))
    unit_bedrooms = Column(String(5))
    unit_bathrooms = Column(String(7))
    unit_sleeps = Column(Integer, default=0)
    unit_kitchenate = Column(String(255))
    unit_has_deleted = Column(Integer, default=0)
    unit_type_images = Column(Text)  # JSON
    featured_amenities = Column(String(150))
    unit_status = Column(String(255))
    unit_cancelation_policy_option = Column(String(255))
    resort_id = Column(Integer, default=0)  # This is just an identifier, not a foreign key
    resort_slug = Column(String(255))
    resort_name = Column(String(255))
    lattitude = Column(String(255))
    longitude = Column(String(255))
    distance = Column(String(255))
    address = Column(String(255))
    location_types = Column(String(255))
    county = Column(String(255))
    country = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    zip = Column(String(255))
    is_featured = Column(Integer, default=0)
    popular = Column(Integer, default=0)
    is_fitness_center = Column(Integer, default=0)
    is_free_wifi = Column(Integer, default=0)
    is_restaurant = Column(Integer, default=0)
    is_swimming_pool = Column(Integer, default=0)
    hotel_star = Column(Integer, default=0)
    top_21_resort = Column(Integer, default=0)
    resort_amenities = Column(Text)  # JSON
    reslrt_updated_at = Column(DateTime)
    resort_google_rating = Column(Integer, default=0)
    resort_has_deleted = Column(Integer, default=0)
    resort_status = Column(String(50))
    google_rating = Column(Integer, default=0)
    user_ratings_total = Column(Integer, default=0)
    google_rating_default = Column(String(8))
    pets_friendly = Column(Integer, default=0)
    unit_rates_price = Column(String(50))
    offer = Column(String(255))
    offer_price = Column(String(255))
    offer_popup = Column(String(255))
    drivetime = Column(String(255))
    image = Column(String(255))
    images = Column(Text)  # JSON
    resort_images = Column(Text)  # JSON
    resort_aminities = Column(Text)  # JSON
    amenities = Column(Text)  # JSON
    highlight_quote = Column(String(255))
    hotelStar = Column(String(255))
    is_open_availability = Column(String(255))
    brand_id = Column(Integer, default=0)
    brand_name = Column(String(255))
    brand_slug = Column(String(255))
    brand_order = Column(String(255))
    unit_rate_id = Column(Integer, default=0)
    unit_rate_start_date = Column(DateTime)
    unit_rate_availability = Column(String(255))
    unit_rate_number_available = Column(String(255))
    unit_rate_nightly_price = Column(String(255))
    unit_rates_count = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

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
    # Remove the problematic relationship - we'll handle this differently


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
    unit_type_id = Column(Integer, default=0)
    pro_unit_type_id = Column(Integer, default=0)
    unit_has_deleted = Column(Integer, default=0)
    unit_type_slug = Column(String(255))
    unit_type_name = Column(String(255))
    unit_bedrooms = Column(String(5))
    unit_bathrooms = Column(String(7))
    unit_sleeps = Column(Integer, default=0)
    unit_kitchenate = Column(String(255))
    unit_status = Column(String(255))
    unit_cancelation_policy_option = Column(String(255))
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
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
  
    # Remove the problematic relationships since resort_id is not a real foreign key
    # If you need to join with Resort table, do it manually in queries


class UnitType(Base):
    __tablename__ = 'unit_types'
    
    id = Column(Integer, primary_key=True)
    resort_id = Column(Integer, ForeignKey('resorts.id'), nullable=False)
    name = Column(String(200), nullable=False)
    has_deleted = Column(Integer, default=0)  # 0 = active, 1 = deleted
    status = Column(String(20), default='active')  # active/pending
    
    # Relationships
    resort = relationship("Resort", back_populates="unit_types")
    listings = relationship("Listing", back_populates="unit_type")
    # Remove pt_rt_listings relationship


class Booking(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True)
    unique_booking_code = Column(String(50), unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Owner of the listing
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)   # Booker/traveller
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    price_night = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    
    # Relationships
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_bookings")
    user = relationship("User", foreign_keys=[user_id], back_populates="user_bookings")
    listing = relationship("Listing", back_populates="bookings")
    # Remove pt_rt_listings relationship since it's not a real foreign key

# Database setup
def get_database_url():
    """Get database URL from environment variables."""
    host = os.getenv("MYSQL_HOST", "localhost")
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "koala_live_laravel")
    
    # Build MySQL URL
    if password:
        return f"mysql+pymysql://{user}:{password}@{host}/{database}"
    else:
        return f"mysql+pymysql://{user}@{host}/{database}"


DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def search_available_future_listings_enhanced(**filters) -> List[PtRtListing]:
    """
    Dynamically filters PtRtListing based on provided keyword arguments.

    Args:
        **filters: Key-value pairs for filtering (e.g., resort_city="Orlando", listing_status="active")

    Returns:
        List of filtered PtRtListing objects
    """
    session = SessionLocal()

    try:
        query = session.query(PtRtListing).distinct()

        # Apply filters dynamically
        filter_conditions = []
        for field_name, value in filters.items():
            if value is not None and hasattr(PtRtListing, field_name):
                column = getattr(PtRtListing, field_name)

                # Case-insensitive partial match for strings
                if isinstance(value, str):
                    filter_conditions.append(column.ilike(f"%{value.strip()}%"))
                else:
                    filter_conditions.append(column == value)

        # ✅ Handle check-in/check-out range filtering
        # if filters.get('listing_check_in') and filters.get('listing_check_out'):
        #     try:
        #         check_in = datetime.strptime(filters['listing_check_in'], "%Y-%m-%d")
        #         check_out = datetime.strptime(filters['listing_check_out'], "%Y-%m-%d")

        #         # Find listings that are available within the range
        #         filter_conditions.append(PtRtListing.listing_check_in <= check_in)
        #         filter_conditions.append(PtRtListing.listing_check_out >= check_out)

        #         print("Date range filtering:")
        #         print("check_in:", check_in)
        #         print("check_out:", check_out)

        #     except ValueError as ve:
                # print("Date parsing error:", ve)

        price_sort = filters.get('price_sort');
        if price_sort != None:
            field = getattr(PtRtListing, 'listing_price_night')
            if price_sort == 'asc':
                query = query.order_by(asc(field))
                print('inside asc')
            else:
                query = query.order_by(desc(field))

        if filter_conditions:
            query = query.filter(and_(*filter_conditions))

        # print(query)

        results =  query.limit(50).all()

        unique_results = deduplicate_by_resort_id(results)

        final_results = unique_results[:10]

        listings = [model_to_dict(listing) for listing in final_results]
        return listings

    except Exception as e:
        print(f"Error in get_pt_rt_listings: {str(e)}")
        return []

    finally:
        session.close()




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



def get_user_bookings(user_email: str) -> List[Dict[str, Any]]:
    """
    Fetch all bookings for a user by email.
    
    Args:
        user_email: The email of the user to fetch bookings for
        
    Returns:
        List of dictionaries with booking details
    """
    session = SessionLocal()
    
    try:
        # Query for user and their bookings with joins
        bookings = session.query(Booking)\
            .join(User, Booking.user_id == User.id)\
            .join(Listing, Booking.listing_id == Listing.id)\
            .join(Resort, Listing.resort_id == Resort.id)\
            .join(UnitType, Listing.unit_type_id == UnitType.id)\
            .filter(User.email == user_email)\
            .filter(User.has_deleted == 0)\
            .filter(Listing.has_deleted == 0)\
            .filter(Resort.has_deleted == 0)\
            .all()
        
        if not bookings:
            return []
        
        result = []
        for booking in bookings:
            result.append({
                "booking_code": booking.unique_booking_code,
                "resort_name": booking.listing.resort.name,
                "resort_city": booking.listing.resort.city,
                "resort_country": booking.listing.resort.country,
                "unit_type": booking.listing.unit_type.name,
                "nights": booking.listing.nights,
                "check_in": booking.listing.check_in.strftime("%Y-%m-%d"),
                "check_out": booking.listing.check_out.strftime("%Y-%m-%d"),
                "price_per_night": f"${booking.price_night:.2f}",
                "total_price": f"${booking.total_price:.2f}",
                "listing_status": booking.listing.status
            })
        
        return result
        
    except Exception as e:
        print(f"Error in get_user_bookings: {str(e)}")
        return []
        
    finally:
        session.close()


def get_available_resorts(
    country: str = None,
    city: str = None,
    state: str = None,
    status: str = "active",
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    List available resorts with optional filtering by country, city, and state.

    Args:
        country: Optional country filter
        city: Optional city filter
        state: Optional state filter
        status: Resort status filter (default: active)
        limit: Maximum number of resorts to return (default: 10)

    Returns:
        List of dictionaries with resort information
    """
    session = SessionLocal()

    try:
        query = session.query(Resort)\
            .join(User, Resort.creator_id == User.id)\
            .filter(Resort.has_deleted == 0)\
            .filter(Resort.status == status)

        if country:
            query = query.filter(Resort.country.isnot(None), Resort.country.ilike(f"%{country.strip()}%"))
        if city:
            query = query.filter(Resort.city.isnot(None), Resort.city.ilike(f"%{city.strip()}%"))
        if state:
            query = query.filter(Resort.state.isnot(None), Resort.state.ilike(f"%{state.strip()}%"))

        resorts = query.limit(limit).all()

        result = []
        for resort in resorts:
            active_listings = session.query(Listing)\
                .filter(Listing.resort_id == resort.id)\
                .filter(Listing.has_deleted == 0)\
                .filter(Listing.status.in_(['active', 'pending']))\
                .count()

            result.append({
                "id": resort.id,
                "name": resort.name,
                "city": resort.city,
                "state": resort.state,
                "country": resort.country,
                "highlight_quote": resort.highlight_quote[:200] + "..." if resort.highlight_quote and len(resort.highlight_quote) > 200 else resort.highlight_quote,
                "active_listings": active_listings,
                "status": resort.status
            })

        result = sorted(result, key=lambda result: result['active_listings'], reverse=True)

        return result


    except Exception as e:
        print(f"Error in get_available_resorts: {str(e)}")
        return []

    finally:
        session.close()


def get_resort_price(
    resort_name: str = None,
    country: str = None,
    city: str = None,
    state: str = None,
    min_price: float = None,
    max_price: float = None,
    unit_type: str = None,
    nights: int = None,
    currency_code: str = None,
    limit: int = 20,
    debug: bool = False
) -> List[Dict[str, Any]]:
    """
    Enhanced version of get_resort_price with better debugging and flexible matching.
    """
    session = SessionLocal()
    
    try:
        if debug:
            print(f"🔍 Searching for resort: '{resort_name}'")
        
        # Start with base query
        query = session.query(ResortMigration)
        
        # Apply filters one by one and count results at each step
        if resort_name:
            query = query.filter(ResortMigration.resort_name.ilike(f"%{resort_name.strip()}%"))
            if debug:
                count = query.count()
                print(f"📊 After name filter '{resort_name}': {count} records")
        
        # Try less restrictive status filter first
        query = query.filter(ResortMigration.listing_has_deleted == 0)
        if debug:
            count = query.count()
            print(f"📊 After deleted filter: {count} records")
        
        # Use broader status filter
        query = query.filter(ResortMigration.listing_status.isnot(None))
        if debug:
            count = query.count()
            print(f"📊 After status not null filter: {count} records")
        
        # Location filters
        if country:
            query = query.filter(
                ResortMigration.country.isnot(None),
                ResortMigration.country.ilike(f"%{country.strip()}%")
            )
            if debug:
                count = query.count()
                print(f"📊 After country filter '{country}': {count} records")
        
        if city:
            query = query.filter(
                ResortMigration.city.isnot(None),
                ResortMigration.city.ilike(f"%{city.strip()}%")
            )
            if debug:
                count = query.count()
                print(f"📊 After city filter '{city}': {count} records")
        
        if state:
            query = query.filter(
                ResortMigration.state.isnot(None),
                ResortMigration.state.ilike(f"%{state.strip()}%")
            )
            if debug:
                count = query.count()
                print(f"📊 After state filter '{state}': {count} records")
        
        # Execute query to get raw results
        all_resorts = query.limit(limit * 3).all()  # Get more for filtering
        
        if debug:
            print(f"📊 Raw query returned: {len(all_resorts)} records")
        
        if not all_resorts:
            # Try fallback searches
            if resort_name:
                # Try searching individual words
                words = resort_name.split()
                if len(words) > 1:
                    fallback_query = session.query(ResortMigration)\
                        .filter(ResortMigration.listing_has_deleted == 0)
                    
                    for word in words:
                        if len(word) > 2:  # Skip small words
                            fallback_query = fallback_query.filter(
                                ResortMigration.resort_name.ilike(f"%{word}%")
                            )
                    
                    all_resorts = fallback_query.limit(limit).all()
                    if debug:
                        print(f"📊 Fallback word search returned: {len(all_resorts)} records")
        
        result = []
        
        for resort in all_resorts:
            try:
                # Enhanced price parsing
                def parse_price_enhanced(price_str):
                    if not price_str:
                        return 0.0
                    
                    # Convert to string and clean
                    clean_price = str(price_str).strip()
                    
                    # Remove currency symbols and commas
                    for symbol in ['$', '€', '£', '¥', ',', ' ']:
                        clean_price = clean_price.replace(symbol, '')
                    
                    # Handle ranges (take the first number)
                    if '-' in clean_price:
                        clean_price = clean_price.split('-')[0].strip()
                    
                    try:
                        return float(clean_price) if clean_price and clean_price.replace('.', '').isdigit() else 0.0
                    except (ValueError, AttributeError):
                        return 0.0
                
                # Try multiple price fields
                listing_price = parse_price_enhanced(resort.listing_price_night)
                unit_price = parse_price_enhanced(resort.unit_rates_price)
                nightly_price = parse_price_enhanced(resort.unit_rate_nightly_price)
                offer_price = parse_price_enhanced(resort.offer_price) if resort.offer_price else None
                
                # Use the best available price
                price_per_night = listing_price or unit_price or nightly_price or 0.0
                
                if debug and price_per_night == 0:
                    print(f"⚠️ No valid price found for {resort.resort_name}")
                    print(f"   listing_price_night: {resort.listing_price_night}")
                    print(f"   unit_rates_price: {resort.unit_rates_price}")
                    print(f"   unit_rate_nightly_price: {resort.unit_rate_nightly_price}")
                
                # Apply price filters (but be more lenient)
                if min_price and price_per_night > 0 and price_per_night < min_price:
                    continue
                if max_price and price_per_night > max_price:
                    continue
                
                # Apply other filters
                if unit_type and resort.unit_type_name:
                    if unit_type.lower() not in resort.unit_type_name.lower():
                        continue
                
                if nights and resort.listing_nights != nights:
                    continue
                
                if currency_code and resort.listing_currency_code:
                    if resort.listing_currency_code.upper() != currency_code.upper():
                        continue
                
                # Calculate totals
                nights_count = resort.listing_nights or 1
                total_price = price_per_night * nights_count if price_per_night > 0 else None
                
                # Build result
                resort_info = {
                    "resort_id": resort.resort_id,
                    "resort_name": resort.resort_name or "Unknown Resort",
                    "location": {
                        "address": resort.address,
                        "city": resort.city,
                        "state": resort.state,
                        "country": resort.country,
                        "zip_code": resort.zip,
                        "coordinates": {
                            "latitude": resort.lattitude,
                            "longitude": resort.longitude
                        }
                    },
                    "pricing": {
                        "price_per_night": price_per_night,
                        "currency_code": resort.listing_currency_code or "USD",
                        "nights": nights_count,
                        "total_price": total_price,
                        "offer_price": offer_price,
                        "offer_description": resort.offer,
                        "price_display": f"{resort.listing_currency_code or '$'}{price_per_night:.2f}" if price_per_night > 0 else "Contact for pricing",
                        "raw_prices": {
                            "listing_price_night": resort.listing_price_night,
                            "unit_rates_price": resort.unit_rates_price,
                            "unit_rate_nightly_price": resort.unit_rate_nightly_price
                        }
                    },
                    "unit_details": {
                        "unit_type": resort.unit_type_name,
                        "bedrooms": resort.unit_bedrooms,
                        "bathrooms": resort.unit_bathrooms,
                        "sleeps": resort.unit_sleeps or 0,
                        "kitchenette": resort.unit_kitchenate
                    },
                    "availability": {
                        "check_in": resort.listing_check_in.strftime("%Y-%m-%d") if resort.listing_check_in else None,
                        "check_out": resort.listing_check_out.strftime("%Y-%m-%d") if resort.listing_check_out else None,
                        "status": resort.listing_status,
                        "has_weekend": bool(resort.has_weekend)
                    },
                    "amenities": {
                        "fitness_center": bool(resort.is_fitness_center),
                        "free_wifi": bool(resort.is_free_wifi),
                        "restaurant": bool(resort.is_restaurant),
                        "swimming_pool": bool(resort.is_swimming_pool),
                        "pets_friendly": bool(resort.pets_friendly)
                    },
                    "ratings": {
                        "hotel_stars": resort.hotel_star or 0,
                        "google_rating": resort.google_rating or 0,
                        "is_featured": bool(resort.is_featured),
                        "is_popular": bool(resort.popular)
                    }
                }
                
                result.append(resort_info)
                
                if len(result) >= limit:
                    break
                    
            except Exception as e:
                if debug:
                    print(f"❌ Error processing resort {resort.resort_id}: {str(e)}")
                continue
        
        # Sort by price (but show zero prices too)
        result.sort(key=lambda x: (x['pricing']['price_per_night'] == 0, x['pricing']['price_per_night']))
        
        if debug:
            print(f"✅ Final result count: {len(result)}")
        
        return result
        
    except Exception as e:
        print(f"Database error in get_resort_price_enhanced: {str(e)}")
        return []
        
    finally:
        session.close()


# Add to tools


def get_resort_details(resort_id: Optional[int] = None, resort_name: Optional[str] = None) -> Dict[str, Any]:
    """Get detailed information about a specific resort by ID or Name."""
    session: Session = SessionLocal()

    try:
        if not resort_id and not resort_name:
            return {"error": "Please provide either resort_id or resort_name."}

        # --- Fetch resort based on ID or Name ---
        query = session.query(Resort).join(User, Resort.creator_id == User.id).filter(Resort.has_deleted == 0)

        if resort_id:
            query = query.filter(Resort.id == resort_id)
        else:
            query = query.filter(Resort.name.ilike(f"%{resort_name.strip()}%"))

        resort = query.first()

        if not resort:
            return {"error": "Resort not found with the given identifier."}

        # --- Fetch unit types ---
        unit_types = session.query(UnitType).filter(
            UnitType.resort_id == resort.id,
            UnitType.has_deleted == 0
        ).all()

        # Optional: print unit types for debugging
        print("unit_types:", [ut.name for ut in unit_types])

        # --- Listings count by status ---
        statuses = ['active', 'pending', 'booked', 'needs_fulfiment', 'fulfilment_request']
        listings_stats = {
            status: session.query(Listing).filter(
                Listing.resort_id == resort.id,
                Listing.has_deleted == 0,
                Listing.status == status
            ).count()
            for status in statuses
        }

        # --- Total bookings ---
        total_bookings = session.query(Booking).join(
            Listing, Booking.listing_id == Listing.id
        ).filter(
            Listing.resort_id == resort.id
        ).count()

        # --- Construct final result ---
        resort_details = {
            "id": resort.id,
            "name": resort.name,
            "slug": resort.slug,
            "address": resort.address,
            "city": resort.city,
            "state": resort.state,
            "country": resort.country,
            "zip": resort.zip,
            "county": resort.county,
            "lattitude": resort.lattitude,
            "longitude": resort.longitude,
            "highlight_quote": resort.highlight_quote,
            "description": resort.description,
            "creator_name": f"{resort.creator.first_name} {resort.creator.last_name}",
            "creator_email": resort.creator.email,
            "status": resort.status,
            "unit_types": [
                {"id": ut.id, "name": ut.name, "status": ut.status} for ut in unit_types
            ],
            "listings_by_status": listings_stats,
            "total_bookings": total_bookings
        }

        return resort_details

    except Exception as e:
        print(f"[ERROR] Failed to fetch resort details: {str(e)}")
        return {"error": f"Exception occurred: {str(e)}"}

    finally:
        session.close()

# def get_resort_details(resort_id: Optional[int] = None, resort_name: Optional[str] = None) -> Dict[str, Any]:
#     """Get detailed information about a specific resort by ID or Name."""
#     session = SessionLocal()

#     try:
#         if resort_id is None and resort_name is None:
#             return {"error": "Please provide either resort_id or resort_name."}

#         # Fetch resort based on ID or Name
#         query = session.query(Resort).join(User, Resort.creator_id == User.id).filter(Resort.has_deleted == 0)

#         if resort_id is not None:
#             query = query.filter(Resort.id == resort_id)
#         elif resort_name is not None:
#             query = query.filter(Resort.name.ilike(f"%{resort_name}%"))  # case-insensitive match

#         resort = query.first()

#         if not resort:
#             return {"error": f"Resort not found with given identifier."}

#         # Get unit types
#         unit_types = session.query(UnitType)\
#             .filter(UnitType.resort_id == resort.id)\
#             .filter(UnitType.has_deleted == 0)\
#             .all()

#         # Get listings count by status
#         listings_stats = {}
#         for status in ['active', 'pending', 'booked', 'needs_fulfiment', 'fulfilment_request']:
#             count = session.query(Listing)\
#                 .filter(Listing.resort_id == resort.id)\
#                 .filter(Listing.has_deleted == 0)\
#                 .filter(Listing.status == status)\
#                 .count()
#             listings_stats[status] = count

#         # Total bookings
#         total_bookings = session.query(Booking)\
#             .join(Listing, Booking.listing_id == Listing.id)\
#             .filter(Listing.resort_id == resort.id)\
#             .count()

#         # Final resort details
#         return {
#             "id": resort.id,
#             "name": resort.name,
#             "slug": resort.slug,
#             "address": resort.address,
#             "city": resort.city,
#             "state": resort.state,
#             "country": resort.country,
#             "zip": resort.zip,
#             "county": resort.county,
#             "lattitude": resort.lattitude,
#             "longitude": resort.longitude,
#             "highlight_quote": resort.highlight_quote,
#             "description": resort.description,
#             "creator_name": f"{resort.creator.first_name} {resort.creator.last_name}",
#             "creator_email": resort.creator.email,
#             "status": resort.status,
#             "unit_types": [{"id": ut.id, "name": ut.name, "status": ut.status} for ut in unit_types],
#             "listings_by_status": listings_stats,
#             "total_bookings": total_bookings
#         }

#     except Exception as e:
#         print(f"Error in get_resort_details: {str(e)}")
#         return {"error": f"Error retrieving resort details: {str(e)}"}

#     finally:
#         session.close()


# def get_resort_details(resort_id: Optional[int] = None, resort_name: Optional[str] = None) -> Dict[str, Any]:
#     """Get detailed information about a specific resort by ID or Name."""
#     session = SessionLocal()

#     try:
#         if resort_id is None and resort_name is None:
#             return {"error": "Please provide either resort_id or resort_name."}

#         # Fetch resort based on ID or Name
#         query = session.query(Resort).join(User, Resort.creator_id == User.id).filter(Resort.has_deleted == 0)

#         if resort_id is not None:
#             query = query.filter(Resort.id == resort_id)
#         elif resort_name is not None:
#             query = query.filter(Resort.name.ilike(f"%{resort_name}%"))  # case-insensitive partial match

#         resort = query.first()

#         if not resort:
#             return {"error": f"Resort not found with the given identifier."}
#         #get unit_types_rubi
#         unit_types = session.query(UnitType).filter(
#             UnitType.resort_id == resort_id,
#             UnitType.has_deleted == 0
#         ).all()

#         return {
#             "resort_name": resort.name,
#             "unit_types": [
#                 {
#                     "id": ut.id,
#                     "name": ut.name,
#                     "status": ut.status
#                 } for ut in unit_types
#             ]
#         }
    

#         # ✅ Get listings count by status
#         listings_stats = {}
#         for status in ['active', 'pending', 'booked', 'needs_fulfiment', 'fulfilment_request']:
#             count = session.query(Listing)\
#                 .filter(Listing.resort_id == resort.id)\
#                 .filter(Listing.has_deleted == 0)\
#                 .filter(Listing.status == status)\
#                 .count()
#             listings_stats[status] = count

#         # ✅ Get total bookings
#         total_bookings = session.query(Booking)\
#             .join(Listing, Booking.listing_id == Listing.id)\
#             .filter(Listing.resort_id == resort.id)\
#             .count()

#         # ✅ Return full resort details
#         return {
#             "id": resort.id,
#             "name": resort.name,
#             "slug": resort.slug,
#             "address": resort.address,
#             "city": resort.city,
#             "state": resort.state,
#             "country": resort.country,
#             "zip": resort.zip,
#             "county": resort.county,
#             "lattitude": resort.lattitude,
#             "longitude": resort.longitude,
#             "highlight_quote": resort.highlight_quote,
#             "description": resort.description,
#             "creator_name": f"{resort.creator.first_name} {resort.creator.last_name}",
#             "creator_email": resort.creator.email,
#             "status": resort.status,
#             "unit_types": [{"id": ut.id, "name": ut.name, "status": ut.status} for ut in unit_types],
#             "listings_by_status": listings_stats,
#             "total_bookings": total_bookings
#         }

#     except Exception as e:
#         print(f"Error in get_resort_details: {str(e)}")
#         return {"error": f"Error retrieving resort details: {str(e)}"}

#     finally:
#         session.close()






# Also update the search_available_listings function to remove problematic relationships
def search_available_listings(
    resort_id: int = None,
    check_in_date: str = None,
    check_out_date: str = None,
    nights: int = None,
    country: str = None,
    limit: int = 20
) -> List[Dict[str, Any]]:
    """Search for available listings with various filters."""
    session = SessionLocal()
    try:
        query = session.query(PtRtListing)\
            .filter(PtRtListing.listing_has_deleted == 0)\
            .filter(PtRtListing.listing_status.in_(['active', 'pending']))
        
        if resort_id:
            query = query.filter(PtRtListing.resort_id == resort_id)
        
        if check_in_date:
            if isinstance(check_in_date, str):
                check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d")
            query = query.filter(PtRtListing.listing_check_in >= check_in_date)
        
        if check_out_date:
            if isinstance(check_out_date, str):
                check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d")
            query = query.filter(PtRtListing.listing_check_out <= check_out_date)
        
        if nights:
            query = query.filter(PtRtListing.listing_nights == nights)
        
        if country:
            query = query.filter(PtRtListing.resort_country.ilike(f"%{country}%"))
        
        listings = query.limit(limit).all()
        
        result = []
        for listing in listings:
            price_per_night = None
            if listing.listing_price_night:
                try:
                    clean_price = str(listing.listing_price_night).replace(',', '').replace('$', '').strip()
                    price_per_night = float(clean_price) if clean_price and clean_price.replace('.', '').isdigit() else None
                except (ValueError, AttributeError):
                    price_per_night = None
            
            result.append({
                "id": listing.id,
                "listing_id": listing.listing_id,
                "resort_id": listing.resort_id,
                "resort_name": listing.resort_name,
                "resort_city": listing.resort_city,
                "resort_country": listing.resort_country,
                "resort_state": listing.resort_state,
                "unit_type": listing.unit_type_name,
                "unit_bedrooms": listing.unit_bedrooms,
                "unit_bathrooms": listing.unit_bathrooms,
                "unit_sleeps": listing.unit_sleeps,
                "nights": listing.listing_nights,
                "check_in": listing.listing_check_in.strftime("%Y-%m-%d") if listing.listing_check_in else None,
                "check_out": listing.listing_check_out.strftime("%Y-%m-%d") if listing.listing_check_out else None,
                "status": listing.listing_status,
                "price_per_night": price_per_night,
                "currency_code": listing.listing_currency_code,
                "listing_type": listing.listing_type,
                "pt_or_rt": listing.pt_or_rt,
                "hot_deals": listing.hot_deals,
                "exclusive": listing.exclusive,
                "resort_google_rating": listing.resort_google_rating
            })
        
        return result
        
    except Exception as e:
        print(f"Error in search_available_listings: {str(e)}")
        return []
        
    finally:
        session.close()


def get_booking_details(booking_id: int, fields: str = "all") -> Dict[str, Any]:
    """Get detailed information about a specific booking by its ID."""
    session = SessionLocal()
    
    try:
        # Query booking with all related information
        booking = session.query(Booking)\
            .join(User, Booking.user_id == User.id)\
            .join(Listing, Booking.listing_id == Listing.id)\
            .join(Resort, Listing.resort_id == Resort.id)\
            .join(UnitType, Listing.unit_type_id == UnitType.id)\
            .filter(Booking.id == booking_id)\
            .first()
        
        if not booking:
            return {"error": f"Booking with ID {booking_id} not found"}
        
        # Get owner information
        owner = session.query(User).filter(User.id == booking.owner_id).first()
        
        # Return different data based on requested fields
        if fields == "price":
            return {
                "booking_id": booking.id,
                "booking_code": booking.unique_booking_code,
                "price_per_night": booking.price_night,
                "total_price": booking.total_price
            }
        elif fields == "dates":
            return {
                "booking_id": booking.id,
                "booking_code": booking.unique_booking_code,
                "check_in": booking.listing.check_in.strftime("%Y-%m-%d"),
                "check_out": booking.listing.check_out.strftime("%Y-%m-%d"),
                "nights": booking.listing.nights
            }
        elif fields == "basic":
            return {
                "booking_id": booking.id,
                "booking_code": booking.unique_booking_code,
                "total_price": booking.total_price,
                "check_in": booking.listing.check_in.strftime("%Y-%m-%d"),
                "check_out": booking.listing.check_out.strftime("%Y-%m-%d"),
                "resort_name": booking.listing.resort.name,
                "status": booking.listing.status
            }
        elif fields == "participants":
            return {
                "booking_id": booking.id,
                "booking_code": booking.unique_booking_code,
                "booker_info": {
                    "name": f"{booking.user.first_name} {booking.user.last_name}",
                    "email": booking.user.email,
                    "phone": booking.user.phone_number
                },
                "owner_info": {
                    "name": f"{owner.first_name} {owner.last_name}" if owner else "Unknown",
                    "email": owner.email if owner else "Unknown"
                }
            }
        elif fields == "resort":
            return {
                "booking_id": booking.id,
                "booking_code": booking.unique_booking_code,
                "resort_info": {
                    "resort_id": booking.listing.resort.id,
                    "resort_name": booking.listing.resort.name,
                    "city": booking.listing.resort.city,
                    "state": booking.listing.resort.state,
                    "country": booking.listing.resort.country,
                    "address": booking.listing.resort.address
                },
                "unit_type": booking.listing.unit_type.name
            }
        else:  # fields == "all" or any other value
            return {
                "booking_id": booking.id,
                "booking_code": booking.unique_booking_code,
                "price_per_night": booking.price_night,
                "total_price": booking.total_price,
                "status": booking.listing.status,
                "booker_info": {
                    "name": f"{booking.user.first_name} {booking.user.last_name}",
                    "email": booking.user.email,
                    "phone": booking.user.phone_number
                },
                "owner_info": {
                    "name": f"{owner.first_name} {owner.last_name}" if owner else "Unknown",
                    "email": owner.email if owner else "Unknown"
                },
                "listing_info": {
                    "listing_id": booking.listing.id,
                    "nights": booking.listing.nights,
                    "check_in": booking.listing.check_in.strftime("%Y-%m-%d"),
                    "check_out": booking.listing.check_out.strftime("%Y-%m-%d"),
                    "unit_type": booking.listing.unit_type.name,
                    "status": booking.listing.status
                },
                "resort_info": {
                    "resort_id": booking.listing.resort.id,
                    "resort_name": booking.listing.resort.name,
                    "city": booking.listing.resort.city,
                    "state": booking.listing.resort.state,
                    "country": booking.listing.resort.country,
                    "address": booking.listing.resort.address
                }
            }
        
    except Exception as e:
        print(f"Error in get_booking_details: {str(e)}")
        return {"error": f"Error retrieving booking details: {str(e)}"}
    
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


def get_listing_details(listing_id: int) -> Dict[str, Any]:
    """Get all details for a specific listing by its ID."""
    session = SessionLocal()
    try:
        listing = session.query(PtRtListing).filter(PtRtListing.id == listing_id).first()
        if not listing:
            return {"error": f"Listing with ID {listing_id} not found"}
        return {col.name: getattr(listing, col.name) for col in PtRtListing.__table__.columns}
    except Exception as e:
        print(f"Error in get_listing_details: {str(e)}")
        return {"error": f"Error retrieving listing details: {str(e)}"}
    finally:
        session.close()


def get_amenity_details(amenity_id: int) -> Dict[str, Any]:
    """Get all details for a specific amenity by its ID."""
    session = SessionLocal()
    try:
        amenity = session.query(Amenity).filter(Amenity.id == amenity_id).first()
        if not amenity:
            return {"error": f"Amenity with ID {amenity_id} not found"}
        return {col.name: getattr(amenity, col.name) for col in Amenity.__table__.columns}
    except Exception as e:
        print(f"Error in get_amenity_details: {str(e)}")
        return {"error": f"Error retrieving amenity details: {str(e)}"}
    finally:
        session.close()


def search_listings_by_type(listing_type: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Get listings by type."""
    session = SessionLocal()
    try:
        listings = session.query(PtRtListing)\
            .filter(PtRtListing.listing_type == listing_type)\
            .limit(limit).all()
        return [{col.name: getattr(listing, col.name) for col in PtRtListing.__table__.columns} for listing in listings]
    except Exception as e:
        print(f"Error in search_listings_by_type: {str(e)}")
        return []
    finally:
        session.close()


def get_featured_listings(limit: int = 10) -> List[Dict[str, Any]]:
    """Get featured listings."""
    session = SessionLocal()
    try:
        listings = session.query(PtRtListing)\
            .filter(PtRtListing.resort_is_featured == 1)\
            .limit(limit).all()
        return [{col.name: getattr(listing, col.name) for col in PtRtListing.__table__.columns} for listing in listings]
    except Exception as e:
        print(f"Error in get_featured_listings: {str(e)}")
        return []
    finally:
        session.close()


def get_weekend_listings(limit: int = 10) -> List[Dict[str, Any]]:
    """Get listings with weekend availability."""
    session = SessionLocal()
    try:
        listings = session.query(PtRtListing)\
            .filter(PtRtListing.has_weekend == 1)\
            .limit(limit).all()
        return [{col.name: getattr(listing, col.name) for col in PtRtListing.__table__.columns} for listing in listings]
    except Exception as e:
        print(f"Error in get_weekend_listings: {str(e)}")
        return []
    finally:
        session.close()


def search_resorts_by_amenities(amenities: List[str], limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search for resorts that have specific amenities.
    
    Args:
        amenities: List of amenity names to search for
        limit: Maximum number of resorts to return
        
    Returns:
        List of resorts with matching amenities
    """
    session = SessionLocal()
    
    try:
        # Search in ResortMigration table for amenities
        query = session.query(ResortMigration)\
            .filter(ResortMigration.resort_has_deleted == 0)\
            .filter(ResortMigration.resort_status == 'active')
        
        # Apply amenity filters
        for amenity in amenities:
            if amenity.lower() in ['pool', 'swimming pool']:
                query = query.filter(ResortMigration.is_swimming_pool == 1)
            elif amenity.lower() in ['wifi', 'free wifi']:
                query = query.filter(ResortMigration.is_free_wifi == 1)
            elif amenity.lower() in ['fitness', 'gym', 'fitness center']:
                query = query.filter(ResortMigration.is_fitness_center == 1)
            elif amenity.lower() in ['restaurant', 'dining']:
                query = query.filter(ResortMigration.is_restaurant == 1)
            elif amenity.lower() in ['pets', 'pet friendly']:
                query = query.filter(ResortMigration.pets_friendly == 1)
        
        resorts = query.limit(limit).all()
        
        result = []
        seen_resorts = set()  # To avoid duplicates
        
        for resort in resorts:
            if resort.resort_id not in seen_resorts:
                seen_resorts.add(resort.resort_id)
                
                result.append({
                    "resort_id": resort.resort_id,
                    "resort_name": resort.resort_name,
                    "location": {
                        "city": resort.city,
                        "state": resort.state,
                        "country": resort.country,
                        "address": resort.address
                    },
                    "amenities": {
                        "swimming_pool": bool(resort.is_swimming_pool),
                        "free_wifi": bool(resort.is_free_wifi),
                        "fitness_center": bool(resort.is_fitness_center),
                        "restaurant": bool(resort.is_restaurant),
                        "pets_friendly": bool(resort.pets_friendly)
                    },
                    "ratings": {
                        "google_rating": resort.google_rating or 0,
                        "hotel_stars": resort.hotel_star or 0,
                        "is_featured": bool(resort.is_featured)
                    },
                    "brand": resort.brand_name,
                    "highlight_quote": resort.highlight_quote
                })
        
        return result
        
    except Exception as e:
        print(f"Error in search_resorts_by_amenities: {str(e)}")
        return []
        
    finally:
        session.close()


def get_price_range_summary(country: str = None, state: str = None) -> Dict[str, Any]:
    """
    Get price range summary for resorts in a specific location.
    
    Args:
        country: Optional country filter
        state: Optional state filter
        
    Returns:
        Dictionary with price statistics
    """
    session = SessionLocal()
    
    try:
        query = session.query(ResortMigration)\
            .filter(ResortMigration.listing_has_deleted == 0)\
            .filter(ResortMigration.listing_status.in_(['active', 'pending', 'available']))
        
        if country:
            query = query.filter(ResortMigration.country.ilike(f"%{country}%"))
        
        if state:
            query = query.filter(ResortMigration.state.ilike(f"%{state}%"))
        
        resorts = query.all()
        
        if not resorts:
            return {"error": "No resorts found for the specified criteria"}
        
        # Parse prices
        prices = []
        for resort in resorts:
            try:
                price_str = resort.listing_price_night or resort.unit_rates_price
                if price_str:
                    clean_price = str(price_str).replace(',', '').replace(',', '').strip()
                    try:
                        price = float(clean_price)
                        if price > 0:
                            prices.append(price)
                    except (ValueError, TypeError):
                        continue
            except Exception:
                continue
        
        if not prices:
            return {"error": "No valid pricing data found"}
        
        # Calculate statistics
        prices.sort()
        count = len(prices)
        
        return {
            "location": {
                "country": country,
                "state": state
            },
            "price_statistics": {
                "min_price": min(prices),
                "max_price": max(prices),
                "average_price": sum(prices) / count,
                "median_price": prices[count // 2] if count % 2 else (prices[count // 2 - 1] + prices[count // 2]) / 2,
                "total_listings": count
            },
            "price_ranges": {
                "budget": len([p for p in prices if p < 100]),
                "mid_range": len([p for p in prices if 100 <= p < 300]),
                "luxury": len([p for p in prices if p >= 300])
            }
        }
        
    except Exception as e:
        print(f"Error in get_price_range_summary: {str(e)}")
        return {"error": f"Error calculating price summary: {str(e)}"}
        
    finally:
        session.close()




# Tool function registry for easy lookup
AVAILABLE_TOOLS = {
    "get_user_bookings": get_user_bookings,
    "get_available_resorts": get_available_resorts,
    "get_resort_details": get_resort_details,
    "search_available_future_listings_enhanced": search_available_future_listings_enhanced,
    "get_booking_details": get_booking_details,
    "get_user_profile": get_user_profile,
    "get_listing_details": get_listing_details,
    "get_amenity_details": get_amenity_details,
    "search_listings_by_type": search_listings_by_type,
    "get_featured_listings": get_featured_listings,
    "get_weekend_listings": get_weekend_listings,
    "get_weekend_listings": get_weekend_listings,
    "get_resort_price": get_resort_price,
    "search_resorts_by_amenities": search_resorts_by_amenities,
    "get_price_range_summary": get_price_range_summary
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


# Test the database connection
def test_database_connection():
    """Test if the database connection works."""
    try:
        session = SessionLocal()
        # Simple test query using SQLAlchemy 2.0 syntax
        from sqlalchemy import text
        result = session.execute(text("SELECT 1")).fetchone()
        session.close()
        return {"status": "success", "message": "Database connection successful"}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}



if __name__ == "__main__":
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
        resorts = call_tool("get_available_resorts", limit=3)
        print(f"Found {len(resorts)} resorts")
        
        # Test get_resort_price
        print("Testing get_resort_price...")
        prices = call_tool("get_resort_price", limit=3)
        print(f"Found {len(prices)} price records")
        
        # Test search_resorts_by_amenities
        print("Testing search_resorts_by_amenities...")
        amenity_resorts = call_tool("search_resorts_by_amenities", amenities=["pool"], limit=3)
        print(f"Found {len(amenity_resorts)} resorts with pool amenity")
    else:
        print("\n❌ Database connection failed!")
        print("Please check your database configuration in the .env file")