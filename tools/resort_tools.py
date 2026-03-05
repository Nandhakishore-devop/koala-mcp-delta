from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from src.database.db import SessionLocal
from src.database.models import Resort, Amenity, ResortAmenity, ResortImage, ResortReview, User, UnitType, Listing, Booking, ResortMigration, EsPoiLocations, EsPlaceOfInterests, PtRtListing

CATEGORY_MAPPING = {
    "Top Sights": 1,
    "Restaurants": 2,
    "Airport": 3,
    "Transit": 4
}

BASE_URL = "https://koalaadmin-prod.s3.us-east-2.amazonaws.com/uploads/resorts"

def get_city_from_resort(resort_name: str, categories: List[str] = None) -> Dict[str, Any]:
    with SessionLocal() as session:
        try:
            resort = session.query(Resort).filter(Resort.name.ilike(f"%{resort_name}%")).first()
            if not resort:
                return {"error": f"Resort '{resort_name}' not found"}

            city = resort.city
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
            if categories:
                category_ids = [CATEGORY_MAPPING[cat] for cat in categories if cat in CATEGORY_MAPPING]
            else:
                category_ids = list(CATEGORY_MAPPING.values())

            pois: List[EsPlaceOfInterests] = (
                session.query(EsPlaceOfInterests)
                .filter(
                    EsPlaceOfInterests.es_poi_location_id == poi_location_id,
                    EsPlaceOfInterests.location_category_id.in_(category_ids)
                )
                .limit(5)
                .all()
            )

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

def get_available_resorts(
    country: str = None,
    city: str = None,
    state: str = None,
    resort_status: str = "active",
    limit: int = 10,
    location_type: str = None,
    brand_id: int = None,
    brand_name: str = None
) -> List[Dict[str, Any]]:
    """
    Search for resorts with active inventory based on geographic location and high-level categories.
    
    Use this tool when the user specifies a Country, City, or State, or searches for major categories
    like 'Beach', 'Ski', or 'Golf' resorts. This tool joins with location metadata and amenities
    internally to provide the most accurate geographic matches.
    
    :param country: Filter by country name (e.g., 'Mexico', 'Aruba', 'United States').
    :param city: Filter by city name (e.g., 'Cabo San Lucas').
    :param state: Filter by state or region.
    :param location_type: Primary traveler category (e.g., 'Beach', 'Ski', 'Golf', 'Mountain').
    :param brand_name: Filter by brand (e.g., 'Marriott', 'Hilton', 'WorldMark').
    :param limit: Maximum number of resorts to return (default 10).
    """
    with SessionLocal() as session:
        try:
            listing_q = (
                session.query(
                    PtRtListing.resort_id,
                    func.count(PtRtListing.id).label("active_count"),
                    func.max(PtRtListing.resort_location_types).label('resort_location_types')
                )
                .filter(
                    PtRtListing.listing_status == "active",
                    PtRtListing.listing_has_deleted == 0
                )
            )

            if brand_id:
                listing_q = listing_q.filter(PtRtListing.resort_brand_id == brand_id)
            if brand_name:
                listing_q = listing_q.filter(PtRtListing.resort_brand_name.ilike(f"%{brand_name.strip()}%"))

            # Subquery to get location data from ANY listing of the resort (fallback for missing active metadata)
            loc_fallback_subq = (
                session.query(
                    PtRtListing.resort_id,
                    func.max(PtRtListing.resort_location_types).label('all_locs')
                )
                .group_by(PtRtListing.resort_id)
                .subquery()
            )

            listing_subq = (
                listing_q.group_by(PtRtListing.resort_id)
                .order_by(func.count(PtRtListing.id).desc())
                .subquery()
            )

            query = (
                session.query(ResortMigration, listing_subq.c.active_count)
                .join(listing_subq, ResortMigration.resort_id == listing_subq.c.resort_id)
                .outerjoin(loc_fallback_subq, ResortMigration.resort_id == loc_fallback_subq.c.resort_id)
                .filter(ResortMigration.resort_has_deleted == 0)
                .filter(ResortMigration.resort_status == resort_status)
            )

            # Join with LocationType and Amenity if location_type filter is provided
            if location_type:
                from src.database.models import LocationType, ResortAmenity, Amenity
                from sqlalchemy import or_
                
                # Standardize search term
                search_term = location_type.strip().lower()
                if "beach" in search_term: search_term = "beach"
                elif "ski" in search_term: search_term = "ski"
                elif "golf" in search_term: search_term = "golf"
                
                # Use outerjoin to avoid filtering out resorts missing in LocationType table 
                # if they still match via other sources
                query = query.outerjoin(LocationType, ResortMigration.resort_id == LocationType.resort_id)
                query = query.outerjoin(ResortAmenity, ResortMigration.resort_id == ResortAmenity.resort_id)
                query = query.outerjoin(Amenity, ResortAmenity.amenity_id == Amenity.id)
                
                query = query.filter(
                    or_(
                        LocationType.types.ilike(f"%{search_term}%"),
                        ResortMigration.location_types.ilike(f"%{search_term}%"),
                        ResortMigration.resort_name.ilike(f"%{search_term}%"),
                        loc_fallback_subq.c.all_locs.ilike(f"%{search_term}%"),
                        Amenity.name.ilike(f"%{search_term}%")
                    )
                )
                # Ensure we don't return duplicate resorts due to multiple matching amenities
                query = query.distinct()

            if country:
                query = query.filter(ResortMigration.country.ilike(f"%{country.strip()}%"))
            if city:
                query = query.filter(ResortMigration.city.ilike(f"%{city.strip()}%"))
            if state:
                query = query.filter(ResortMigration.state.ilike(f"%{state.strip()}%"))
            # Removed redundant/unreliable ResortMigration.location_types filtering

            resorts = query.order_by(listing_subq.c.active_count.desc()).limit(limit).all()

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
                    "active_listings_count": active_count
                })
            return result
        except Exception as e:
            return [{"error": str(e)}]

def get_resort_details(
    resort_id: Optional[int] = None,
    resort_name: Optional[str] = None,  
    amenities_list: Optional[List[str]] = None,
    amenities_only: bool = False,
    list_resorts_with_amenities: bool = False,
    limit: int = 5
) -> Dict[str, Any]:
    session: Session = SessionLocal()
    try:
        if list_resorts_with_amenities:
            resorts = session.query(Resort).filter(Resort.has_deleted == 0).limit(limit).all()
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
        elif resort_id or resort_name:
            resort = None
            
            # 1. Try by ID first if provided
            if resort_id:
                try:
                    rid = int(resort_id)
                    resort = session.query(Resort).filter(Resort.id == rid, Resort.has_deleted == 0).first()
                except (ValueError, TypeError):
                    pass
            
            # 2. Try by Name if ID failed or wasn't provided
            if not resort and resort_name:
                name_search = resort_name.strip()
                resort = session.query(Resort).filter(Resort.name.ilike(f"%{name_search}%"), Resort.has_deleted == 0).first()
                
                # 3. Fuzzy fallback
                if not resort and len(name_search.split()) > 2:
                    words = name_search.split()
                    short_name = " ".join(words[-2:])
                    resort = session.query(Resort).filter(Resort.name.ilike(f"%{short_name}%"), Resort.has_deleted == 0).first()

            if not resort:
                return {"error": "Resort not found."}

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

            top_image = (
                session.query(ResortImage)
                .filter(ResortImage.resort_id == resort.id)
                .order_by(ResortImage.image_order.asc())
                .first()
            )
            image_data = (
                {"url": f"{BASE_URL}/{resort.id}/{top_image.image}"}
                if top_image and top_image.image
                else None
            )

            unit_types = session.query(UnitType).filter(
                UnitType.resort_id == resort.id, UnitType.has_deleted == 0
            ).all()

            # Expanded statuses for richer data
            statuses = ['active', 'pending', 'booked', 'needs_fulfiment', 'fulfilment_request']
            listings_stats = {
                status: session.query(Listing).filter(
                    Listing.resort_id == resort.id,
                    Listing.has_deleted == 0,
                    Listing.status == status
                ).count()
                for status in statuses
            }

            # Total bookings count
            total_bookings = session.query(Booking).join(
                Listing, Booking.listing_id == Listing.id
            ).filter(Listing.resort_id == resort.id).count()

            reviews = (
                session.query(ResortReview)
                .filter(ResortReview.resort_id == resort.id)
                .order_by(ResortReview.rating.desc())
                .limit(3)
                .all()
            )
            reviews_data = [
                {"author_name": review.author_name, "rating": review.rating, "text": review.text}
                for review in reviews
            ]

            # Get additional metadata
            resort_mig = session.query(ResortMigration).filter(ResortMigration.resort_id == resort.id).first()
            first_listing = session.query(PtRtListing).filter(PtRtListing.resort_id == resort.id).first()
            
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
                "highlight_quote": resort.highlight_quote,
                "description": resort.description,
                "creator_name": f"{resort.creator.first_name} {resort.creator.last_name}" if resort.creator else "Unknown",
                "creator_email": resort.creator.email if resort.creator else "Unknown",
                "status": resort.status,
                "resort_google_rating": resort_mig.resort_google_rating if resort_mig else 0,
                "resort_brand_name": first_listing.resort_brand_name if first_listing and first_listing.resort_brand_name else "Independent",
                "unit_types": [{"id": ut.id, "name": ut.name, "status": ut.status} for ut in unit_types],
                "listings_by_status": listings_stats,
                "total_bookings": total_bookings,
                "top_image": image_data,
                "amenities": amenities_data,
                "reviews": reviews_data
            }
        return {"error": "Missing parameters."}
    except Exception as e:
        return {"error": str(e)}
    finally:
        session.close()

def get_user_profile(user_email: str = None, user_id: int = None) -> Dict[str, Any]:
    """Get user profile information including booking and listing counts."""
    session = SessionLocal()
    try:
        if user_id:
            user = session.query(User).filter(User.id == user_id, User.has_deleted == 0).first()
        elif user_email:
            user = session.query(User).filter(User.email == user_email, User.has_deleted == 0).first()
        else:
            return {"error": "user_email or user_id required"}

        if not user:
            identifier = f"ID {user_id}" if user_id else f"email {user_email}"
            return {"error": f"User with {identifier} not found"}
        
        bookings_count = session.query(Booking).filter(Booking.user_id == user.id).count()
        owned_listings_count = session.query(Booking).filter(Booking.owner_id == user.id).count()
        created_resorts_count = session.query(Resort).filter(Resort.creator_id == user.id, Resort.has_deleted == 0).count()
        
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
        return {"error": str(e)}
    finally:
        session.close()

def search_resorts_by_amenities(
    amenities: List[str], 
    limit: int = 5, 
    match_all: bool = True
) -> List[Dict[str, Any]]:
    """
    Find resorts based on specific property features and conveniences (amenities).
    
    Use this tool for granular feature searches like 'Pool', 'Kitchen', 'Balcony', 'Gym', or 'WiFi'. 
    
    **CRITICAL**: 
    1. Do NOT use this tool for 'Pet Friendly' or 'Pets Allowed' searches. 
       Instead, use `search_available_future_listings_merged(pets_allowed=True)` from `search_tools.py`.
    2. Do NOT use this tool for geographic filtering (e.g., 'Florida', 'Orlando'). 
       For searches involving a Country, City, or State, use `get_available_resorts` or `search_available_future_listings_merged`.
    
    :param amenities: List of strings (e.g., ['Pool', 'Kitchen']).
    :param match_all: If True, only returns resorts containing ALL specified amenities.
    :param limit: Maximum number of resorts to return.
    """
    session = SessionLocal()
    try:
        from sqlalchemy.orm import joinedload
        # Group subqueries by keyword to support match_all logic
        keyword_to_subqs = {}

        for term in amenities:
            term = term.strip().lower()
            if not term: continue
            
            # 1. Match via ResortAmenity table
            amenity_ids = [
                a[0] for a in session.query(Amenity.id)
                .filter(func.lower(Amenity.name).like(f"%{term}%"))
                .all()
            ]
            
            # 2. Match via UnitType names (common fallback for "Kitchen", "Balcony", etc.)
            unittype_match_subq = (
                session.query(PtRtListing.resort_id)
                .join(UnitType, PtRtListing.unit_type_id == UnitType.id)
                .filter(UnitType.name.ilike(f"%{term}%"))
            )

            if amenity_ids:
                amenity_match_subq = session.query(ResortAmenity.resort_id).filter(ResortAmenity.amenity_id.in_(amenity_ids))
                # Union the results for this specific keyword
                combined_term_subq = amenity_match_subq.union(unittype_match_subq).subquery()
            else:
                combined_term_subq = unittype_match_subq.subquery()
            
            keyword_to_subqs[term] = combined_term_subq

        if not keyword_to_subqs:
            return []

        # Base query
        query = session.query(Resort).filter(Resort.has_deleted == 0)
        query = query.options(joinedload(Resort.resort_amenities).joinedload(ResortAmenity.amenity))

        if match_all:
            # Must match EVERY keyword
            for keyword, subq in keyword_to_subqs.items():
                query = query.filter(Resort.id.in_(subq))
        else:
            # Match ANY of the keywords
            all_subqs = or_(*[Resort.id.in_(subq) for subq in keyword_to_subqs.values()])
            query = query.filter(all_subqs).distinct()

        results = query.limit(limit).all()
        return [
            {
                "resort_id": r.id,
                "resort_name": r.name,
                "amenities": [ra.amenity.name for ra in r.resort_amenities if ra.amenity]
            }
            for r in results
        ]
    finally:
        session.close()

def get_platform_stats() -> Dict[str, Any]:
    """Get aggregate statistics about Go-Koala's resort and listing coverage."""
    session = SessionLocal()
    try:
        total_resorts = session.query(func.count(ResortMigration.id)).filter(ResortMigration.resort_has_deleted == 0).scalar()
        
        active_listings = (
            session.query(func.count(PtRtListing.id))
            .filter(PtRtListing.listing_status == "active", PtRtListing.listing_has_deleted == 0)
            .scalar()
        )
        
        country_count = session.query(func.count(func.distinct(ResortMigration.country))).scalar()
        state_count = session.query(func.count(func.distinct(ResortMigration.state))).scalar()
        
        top_cities = (
            session.query(ResortMigration.city, func.count(PtRtListing.id).label("count"))
            .join(PtRtListing, ResortMigration.resort_id == PtRtListing.resort_id)
            .filter(PtRtListing.listing_status == "active", PtRtListing.listing_has_deleted == 0)
            .group_by(ResortMigration.city)
            .order_by(func.count(PtRtListing.id).desc())
            .limit(3)
            .all()
        )
        
        return {
            "platform": "Go-Koala",
            "total_resorts_on_platform": total_resorts,
            "current_active_listings": active_listings,
            "geographic_coverage": {
                "countries": country_count,
                "states_regions": state_count
            },
            "top_cities_by_availability": [
                {"city": city, "active_listings": count} for city, count in top_cities
            ],
            "service_rating": "9.8/10",
            "description": "Go-Koala is a premium timeshare marketplace focusing on verified, high-quality resort stays."
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        session.close()

def get_top_rated_resorts(limit: int = 5, min_rating: float = 4.0) -> List[Dict[str, Any]]:
    """
    Find highly-rated resorts using Google ratings and count of reviews.
    
    :param limit: Maximum number of resorts to return.
    :param min_rating: Minimum rating threshold. If no resorts meet this threshold (e.g., asked for 9.5 but max is 5.0), 
                      the tool will automatically return the top available resorts.
    """
    session = SessionLocal()
    try:
        # 1. Try matching the specific threshold
        top_resorts = (
            session.query(ResortMigration)
            .filter(ResortMigration.resort_has_deleted == 0)
            .filter(ResortMigration.resort_google_rating >= min_rating)
            .order_by(ResortMigration.resort_google_rating.desc())
            .limit(limit)
            .all()
        )
        
        # 2. Fallback: If no results (e.g., threshold was out of range), return the top results anyway
        if not top_resorts:
            top_resorts = (
                session.query(ResortMigration)
                .filter(ResortMigration.resort_has_deleted == 0)
                .order_by(ResortMigration.resort_google_rating.desc())
                .limit(limit)
                .all()
            )
        
        results = []
        for r in top_resorts:
            # Get a sample review snippet if available
            review = session.query(ResortReview).filter(ResortReview.resort_id == r.resort_id).first()
            
            results.append({
                "resort_id": r.resort_id,
                "name": r.resort_name,
                "city": r.city,
                "rating": r.resort_google_rating,
                "address": r.address,
                "featured_review": review.text[:150] + "..." if review else "Great choice for vacationers."
            })
        return results
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        session.close()

def get_nearby_poi(resort_id: int, limit: int = 5) -> List[Dict[str, Any]]:
    """Get local points of interest (attractions, dining, sights) near a specific resort."""
    session = SessionLocal()
    try:
        # Get resort city
        resort = session.query(ResortMigration).filter(ResortMigration.resort_id == resort_id).first()
        if not resort:
             return [{"error": f"Resort ID {resort_id} not found."}]
        
        # Find POIs in the same city
        pois = (
            session.query(EsPlaceOfInterests)
            .filter(EsPlaceOfInterests.city.ilike(f"%{resort.city}%"))
            .limit(limit)
            .all()
        )
        
        return [
            {
                "name": p.full_term or p.term,
                "category": p.type,
                "description": p.description[:150] + "..." if p.description else "A popular local spot.",
                "url": p.url
            }
            for p in pois
        ]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        session.close()

def get_resort_reviews(resort_id: int, limit: int = 3) -> List[Dict[str, Any]]:
    """Get the latest guest reviews for a resort to understand sentiment and highlights."""
    session = SessionLocal()
    try:
        reviews = (
            session.query(ResortReview)
            .filter(ResortReview.resort_id == resort_id)
            .order_by(ResortReview.id.desc())
            .limit(limit)
            .all()
        )
        
        if not reviews:
            return [{"info": "No reviews available for this resort yet."}]
            
        return [
            {
                "author": r.author_name,
                "rating": r.rating,
                "text": r.text,
                "date_description": r.relative_time_description
            }
            for r in reviews
        ]
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        session.close()
