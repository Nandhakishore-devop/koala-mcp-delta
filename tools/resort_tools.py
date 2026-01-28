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
                    # Ensure it's an integer
                    rid = int(resort_id)
                    resort = session.query(Resort).filter(Resort.id == rid, Resort.has_deleted == 0).first()
                except (ValueError, TypeError):
                    pass # Not a valid integer ID
            
            # 2. Try by Name if ID failed or wasn't provided
            if not resort and resort_name:
                name_search = resort_name.strip()
                resort = session.query(Resort).filter(Resort.name.ilike(f"%{name_search}%"), Resort.has_deleted == 0).first()
                
                # 3. Fuzzy fallback: If name is long, try matching parts of it 
                # (e.g., "Club Wyndham Bonnet Creek" -> try "Bonnet Creek")
                if not resort and len(name_search.split()) > 2:
                    words = name_search.split()
                    # Try the last two words which usually contain the core name
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

            listings_stats = {
                status: session.query(Listing).filter(
                    Listing.resort_id == resort.id,
                    Listing.has_deleted == 0,
                    Listing.status == status
                ).count()
                for status in ['active', 'pending', 'booked']
            }

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
                "address": resort.address,
                "city": resort.city,
                "description": resort.description,
                "unit_types": [{"id": ut.id, "name": ut.name} for ut in unit_types],
                "listings_by_status": listings_stats,
                "top_image": image_data,
                "amenities": amenities_data,
                "reviews": reviews_data
            }
        return {"error": "Missing parameters."}
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
        amenity_ids = [
            a[0] for a in session.query(Amenity.id)
            .filter(func.lower(Amenity.name).in_([name.lower() for name in amenities]))
            .all()
        ]
        if not amenity_ids: return []

        if match_all:
            subquery = (
                session.query(ResortAmenity.resort_id)
                .filter(ResortAmenity.amenity_id.in_(amenity_ids))
                .group_by(ResortAmenity.resort_id)
                .having(func.count(func.distinct(ResortAmenity.amenity_id)) == len(amenity_ids))
                .subquery()
            )
            resorts_query = session.query(Resort).filter(Resort.id.in_(subquery))
        else:
            resorts_query = (
                session.query(Resort)
                .join(ResortAmenity, Resort.id == ResortAmenity.resort_id)
                .filter(ResortAmenity.amenity_id.in_(amenity_ids))
                .distinct()
            )

        resorts = resorts_query.filter(Resort.has_deleted == 0).limit(limit).all()
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
