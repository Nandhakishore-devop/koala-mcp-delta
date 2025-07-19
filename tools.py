"""
Tool functions for resort booking system using SQLAlchemy with MySQL.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import json
import os
from dotenv import load_dotenv

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
    
    # Relationships
    created_resorts = relationship("Resort", foreign_keys="Resort.creator_id", back_populates="creator")
    owned_listings = relationship("Booking", foreign_keys="Booking.owner_id", back_populates="owner")
    bookings = relationship("Booking", foreign_keys="Booking.user_id", back_populates="user")


class Resort(Base):
    __tablename__ = 'resorts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    address = Column(Text)
    has_deleted = Column(Integer, default=0)  # 0 = active, 1 = deleted
    status = Column(String(20), default='active')  # active/pending
    lattitude = Column(String(255))  # Note: it's 'lattitude' with double 't' in the actual DB
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


class Listing(Base):
    __tablename__ = 'listings'
    
    id = Column(Integer, primary_key=True)
    resort_id = Column(Integer, ForeignKey('resorts.id'), nullable=False)
    unit_type_id = Column(Integer, ForeignKey('unit_types.id'), nullable=False)
    nights = Column(Integer, nullable=False)
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    has_deleted = Column(Integer, default=0)  # 0 = active, 1 = deleted
    status = Column(String(30), default='active')  # active/pending/booked/needs_fulfiment/fulfilment_request/deleted/failed/draft
    
    # Relationships
    resort = relationship("Resort", back_populates="listings")
    unit_type = relationship("UnitType", back_populates="listings")
    bookings = relationship("Booking", back_populates="listing")


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
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_listings")
    user = relationship("User", foreign_keys=[user_id], back_populates="bookings")
    listing = relationship("Listing", back_populates="bookings")


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
        
    finally:
        session.close()


def get_available_resorts(country: str = None, status: str = "active", limit: int = 10) -> List[Dict[str, Any]]:
    """
    List available resorts with optional filtering.
    
    Args:
        country: Optional country filter
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
            query = query.filter(Resort.country.ilike(f"%{country}%"))
        
        resorts = query.limit(limit).all()
        
        result = []
        for resort in resorts:
            # Count active listings for this resort
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
        
        return result
        
    finally:
        session.close()


def get_resort_details(resort_id: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific resort.
    
    Args:
        resort_id: The ID of the resort to get details for
        
    Returns:
        Dictionary with detailed resort information
    """
    session = SessionLocal()
    
    try:
        resort = session.query(Resort)\
            .join(User, Resort.creator_id == User.id)\
            .filter(Resort.id == resort_id)\
            .filter(Resort.has_deleted == 0)\
            .first()
        
        if not resort:
            return {"error": f"Resort with ID {resort_id} not found"}
        
        # Get unit types for this resort
        unit_types = session.query(UnitType)\
            .filter(UnitType.resort_id == resort.id)\
            .filter(UnitType.has_deleted == 0)\
            .all()
        
        # Get listings count by status
        listings_stats = {}
        for status in ['active', 'pending', 'booked', 'needs_fulfiment', 'fulfilment_request']:
            count = session.query(Listing)\
                .filter(Listing.resort_id == resort.id)\
                .filter(Listing.has_deleted == 0)\
                .filter(Listing.status == status)\
                .count()
            listings_stats[status] = count
        
        # Get total bookings
        total_bookings = session.query(Booking)\
            .join(Listing, Booking.listing_id == Listing.id)\
            .filter(Listing.resort_id == resort.id)\
            .count()
        
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
            "lattitude": resort.lattitude,
            "longitude": resort.longitude,
            "highlight_quote": resort.highlight_quote,
            "description": resort.description,
            "creator_name": f"{resort.creator.first_name} {resort.creator.last_name}",
            "creator_email": resort.creator.email,
            "status": resort.status,
            "unit_types": [{"id": ut.id, "name": ut.name, "status": ut.status} for ut in unit_types],
            "listings_by_status": listings_stats,
            "total_bookings": total_bookings
        }
        
    finally:
        session.close()


def search_available_listings(
    resort_id: int = None,
    check_in_date: str = None,
    check_out_date: str = None,
    nights: int = None,
    country: str = None,
    limit: int = 20
) -> List[Dict[str, Any]]:
    """
    Search for available listings with various filters.
    
    Args:
        resort_id: Optional resort ID filter
        check_in_date: Optional check-in date filter (YYYY-MM-DD)
        check_out_date: Optional check-out date filter (YYYY-MM-DD)
        nights: Optional number of nights filter
        country: Optional country filter
        limit: Maximum number of listings to return (default: 20)
        
    Returns:
        List of available listings
    """
    session = SessionLocal()
    
    try:
        query = session.query(Listing)\
            .join(Resort, Listing.resort_id == Resort.id)\
            .join(UnitType, Listing.unit_type_id == UnitType.id)\
            .filter(Listing.has_deleted == 0)\
            .filter(Listing.status.in_(['active', 'pending']))\
            .filter(Resort.has_deleted == 0)\
            .filter(Resort.status == 'active')
        
        if resort_id:
            query = query.filter(Listing.resort_id == resort_id)
        
        if check_in_date:
            query = query.filter(Listing.check_in >= check_in_date)
        
        if check_out_date:
            query = query.filter(Listing.check_out <= check_out_date)
        
        if nights:
            query = query.filter(Listing.nights == nights)
        
        if country:
            query = query.filter(Resort.country.ilike(f"%{country}%"))
        
        listings = query.limit(limit).all()
        
        result = []
        for listing in listings:
            result.append({
                "listing_id": listing.id,
                "resort_name": listing.resort.name,
                "resort_city": listing.resort.city,
                "resort_country": listing.resort.country,
                "unit_type": listing.unit_type.name,
                "nights": listing.nights,
                "check_in": listing.check_in.strftime("%Y-%m-%d"),
                "check_out": listing.check_out.strftime("%Y-%m-%d"),
                "status": listing.status,
                "resort_highlight": listing.resort.highlight_quote
            })
        
        return result
        
    finally:
        session.close()


def get_booking_details(booking_id: int, fields: str = "all") -> Dict[str, Any]:
    """
    Get detailed information about a specific booking by its ID.
    
    Args:
        booking_id: The ID of the booking to get details for
        fields: What fields to return - "all", "price", "dates", "basic", "participants", "resort"
        
    Returns:
        Dictionary with booking information based on requested fields
    """
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
        
    finally:
        session.close()


def get_user_profile(user_email: str) -> Dict[str, Any]:
    """
    Get user profile information.
    
    Args:
        user_email: Email of the user
        
    Returns:
        User profile information
    """
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
        
    finally:
        session.close()


# Tool function registry for easy lookup
AVAILABLE_TOOLS = {
    "get_user_bookings": get_user_bookings,
    "get_available_resorts": get_available_resorts,
    "get_resort_details": get_resort_details,
    "search_available_listings": search_available_listings,
    "get_booking_details": get_booking_details,
    "get_user_profile": get_user_profile
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