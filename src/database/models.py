from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20))
    has_deleted = Column(Integer, default=0)
    status = Column(String(20), default='active')
    
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
    has_deleted = Column(Integer, default=0)
    status = Column(String(30), default='active')
    reservation_no = Column(String(30), nullable=False)
    
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
    resort_amenities = relationship("ResortAmenity", back_populates="amenity")

class ResortMigration(Base):
    __tablename__ = 'resort_migration'
    id = Column(BigInteger, primary_key=True)
    pt_rt_id = Column(Integer, nullable=False)
    listing_id = Column(Integer)
    resort_id = Column(Integer, default=0)
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

class Resort(Base):
    __tablename__ = 'resorts'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    address = Column(Text)
    has_deleted = Column(Integer, default=0)
    status = Column(String(20), default='active')
    lattitude = Column(String(255))
    longitude = Column(String(255))
    country = Column(String(100))
    city = Column(String(100))
    state = Column(String(100))
    zip = Column(String(20))
    county = Column(String(100))
    highlight_quote = Column(Text)
    description = Column(Text)
    
    creator = relationship("User", foreign_keys=[creator_id], back_populates="created_resorts")
    unit_types = relationship("UnitType", back_populates="resort")
    listings = relationship("Listing", back_populates="resort")
    images = relationship("ResortImage", back_populates="resort")
    resort_amenities = relationship("ResortAmenity", back_populates="resort")
    reviews = relationship("ResortReview", back_populates="resort", cascade="all, delete-orphan")
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
    unit_type_slug = Column(String(255))
    unit_type_name = Column(String(255))
    unit_sleeps = Column(String(50))
    resort_id = Column(Integer, default=0)
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
    
    unit_type = relationship("UnitType", back_populates="pt_rt_listings")

class UnitType(Base):
    __tablename__ = 'unit_types'
    id = Column(Integer, primary_key=True)
    resort_id = Column(Integer, ForeignKey('resorts.id'), nullable=False)
    name = Column(String(200), nullable=False)
    has_deleted = Column(Integer, default=0)
    status = Column(String(20), default='active')
    sleeps = Column(String(50))
    
    resort = relationship("Resort", back_populates="unit_types")
    listings = relationship("Listing", back_populates="unit_type")
    pt_rt_listings = relationship(
        "PtRtListing",
        primaryjoin="UnitType.resort_id == foreign(PtRtListing.resort_id)",
        back_populates="unit_type"
    )

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    unique_booking_code = Column(String(50), unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_bookings")
    user = relationship("User", foreign_keys=[user_id], back_populates="user_bookings")
    listing = relationship("Listing", back_populates="bookings")
    booking_metrics = relationship("BookingMetrics", back_populates="booking", uselist=False)

class BookingMetrics(Base):
    __tablename__ = 'booking_metrics'
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=False)
    total_listing_price = Column(Float, nullable=False)
    total_booking_price = Column(Float, nullable=False)
    booking = relationship("Booking", back_populates="booking_metrics")

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
    resort = relationship("Resort", back_populates="resort_amenities")
    amenity = relationship("Amenity", back_populates="resort_amenities")

class EsPlaceOfInterests(Base):
    __tablename__ = "es_place_of_interests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    es_poi_location_id = Column(Integer, ForeignKey("es_poi_locations.id"), nullable=False)
    location_category_id = Column(Integer)
    term = Column(String(255))
    full_term = Column(String(255))
    image = Column(String(255))
    price = Column(String(255))
    type = Column(String(255))
    lattitude = Column(String(255))
    longitude = Column(String(255))
    radius = Column(String(255))
    country = Column(String(255))
    state = Column(String(255))
    city = Column(String(255))
    description = Column(Text)
    url = Column(String(300))
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
    place_of_interests = relationship("EsPlaceOfInterests", back_populates="location", cascade="all, delete-orphan")

class LocationType(Base):
    __tablename__ = "location_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    resort_id = Column(Integer, ForeignKey("resorts.id"), nullable=False)
    resort_location_master_id = Column(Integer, ForeignKey("resort_location_master.id"), nullable=False)
    types = Column(String(255), nullable=False)
    status = Column(Integer, default=1, nullable=False)
    resort = relationship("Resort", back_populates="location_types")

class ResortReview(Base):
    __tablename__ = "resort_reviews"
    id = Column(Integer, primary_key=True, autoincrement=True)
    resort_id = Column(Integer, ForeignKey("resorts.id"), nullable=False)
    author_name = Column(String(255))
    author_url = Column(String(255))
    language = Column(String(255))
    profile_photo_url = Column(String(600))
    rating = Column(String(10))
    relative_time_description = Column(String(255))
    text = Column(Text)
    time = Column(String(255))
    resort = relationship("Resort", back_populates="reviews")
