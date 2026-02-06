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
    location_type: str = None
) -> List[Dict[str, Any]]:
    with SessionLocal() as session:
        try:
            listing_subq = (
                session.query(
                    PtRtListing.resort_id,
                    func.count(PtRtListing.id).label("active_count")
                )
                .filter(
                    PtRtListing.listing_status == "active",
                    PtRtListing.listing_has_deleted == 0
                )
                .group_by(PtRtListing.resort_id)
                .order_by(func.count(PtRtListing.id).desc())
                .subquery()
            )

            query = (
                session.query(ResortMigration, listing_subq.c.active_count)
                .join(listing_subq, ResortMigration.resort_id == listing_subq.c.resort_id)
                .filter(ResortMigration.resort_has_deleted == 0)
                .filter(ResortMigration.resort_status == resort_status)
            )

            if country:
                query = query.filter(ResortMigration.country.ilike(f"%{country.strip()}%"))
            if city:
                query = query.filter(ResortMigration.city.ilike(f"%{city.strip()}%"))
            if state:
                query = query.filter(ResortMigration.state.ilike(f"%{state.strip()}%"))
            if location_type:
                query = query.filter(ResortMigration.location_types.ilike(f"%{location_type.strip()}%"))

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

def get_user_profile(user_email: str) -> Dict[str, Any]:
    """Get user profile information including booking and listing counts."""
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.email == user_email, User.has_deleted == 0).first()
        if not user:
            return {"error": f"User with email {user_email} not found"}
        
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
    session = SessionLocal()
    try:
        from sqlalchemy.orm import joinedload
        # Group IDs by the keyword that found them to support match_all logic
        keyword_to_ids = {}
        all_found_ids = set()

        for term in amenities:
            term = term.strip().lower()
            if not term: continue
            
            # Find all amenities that CONTAIN this term
            # Using .like() with func.lower() for standard SQL compatibility
            ids = [
                a[0] for a in session.query(Amenity.id)
                .filter(func.lower(Amenity.name).like(f"%{term}%"))
                .all()
            ]
            if ids:
                keyword_to_ids[term] = set(ids)
                all_found_ids.update(ids)

        if not keyword_to_ids:
            return []

        # Start with a base query and eager load amenities to avoid lazy-loading issues
        query = session.query(Resort).filter(Resort.has_deleted == 0)
        query = query.options(joinedload(Resort.resort_amenities).joinedload(ResortAmenity.amenity))

        if match_all:
            # Find resorts that match ALL keywords (intersection of resort sets)
            for keyword, ids in keyword_to_ids.items():
                # For each keyword, at least one of its matching amenities must be present
                subq = session.query(ResortAmenity.resort_id).filter(ResortAmenity.amenity_id.in_(list(ids))).subquery()
                query = query.filter(Resort.id.in_(subq))
        else:
            # Any match will do
            query = query.join(ResortAmenity, Resort.id == ResortAmenity.resort_id)
            query = query.filter(ResortAmenity.amenity_id.in_(list(all_found_ids))).distinct()

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
