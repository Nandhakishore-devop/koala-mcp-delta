from typing import Any, Dict, List, Optional
from sqlalchemy import func, or_
from src.database.db import SessionLocal
from src.database.models import PtRtListing

def get_market_price_trends(location: str) -> Dict[str, Any]:
    """Analyze current active listings to provide price trends for a specific location (City or State)."""
    session = SessionLocal()
    try:
        search_term = location.strip()
        # Get active listings in the city or state
        listings = (
            session.query(PtRtListing)
            .filter(PtRtListing.listing_status == "active", PtRtListing.listing_has_deleted == 0)
            .filter(
                or_(
                    PtRtListing.resort_city.ilike(f"%{search_term}%"),
                    PtRtListing.resort_state.ilike(f"%{search_term}%")
                )
            )
            .all()
        )
        
        if not listings:
            return {"info": f"No active listings found in '{location}' to analyze trends."}
            
        prices = [float(l.listing_price_night) for l in listings if l.listing_price_night and l.listing_price_night.replace('.', '', 1).isdigit()]
        
        if not prices:
            return {"info": f"No price data available for listings in '{location}'."}
            
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        
        return {
            "location": location,
            "total_listings_analyzed": len(prices),
            "average_nightly_rate": round(avg_price, 2),
            "price_range": {
                "min": min_price,
                "max": max_price
            },
            "market_status": "Competitive" if len(prices) > 10 else "Niche",
            "currency": "USD"
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        session.close()
