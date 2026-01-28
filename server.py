import sys
from mcp.server.fastmcp import FastMCP
from tools.resort_tools import get_city_from_resort, get_available_resorts, get_resort_details, search_resorts_by_amenities
from tools.booking_tools import get_user_bookings, book_resort_listing, get_payment_methods, get_cancellation_policy
from tools.search_tools import search_available_future_listings_merged
from tools.utils import get_user_profile, test_database_connection
from src.database.db import initialize_database

# Initialize FastMCP server
mcp = FastMCP("Koala Resort Server")

# Initialize database on startup
if initialize_database():
    print("✅ Database initialized successfully",file=sys.stderr)
else:
    print("❌ Database initialization failed")

# Register Resort Tools
@mcp.tool()
def city_from_resort(resort_name: str, categories: list[str] = None):
    """Get city and POIs (sights, restaurants, etc.) for a resort."""
    return get_city_from_resort(resort_name, categories)

@mcp.tool()
def available_resorts(country: str = None, city: str = None, limit: int = 10):
    """List available resorts filtered by location."""
    return get_available_resorts(country=country, city=city, limit=limit)

@mcp.tool()
def resort_details(resort_id: int = None, resort_name: str = None):
    """Get detailed information about a specific resort."""
    return get_resort_details(resort_id=resort_id, resort_name=resort_name)

# Register Search Tools
@mcp.tool()
def search_listings(resort_name: str = None, check_in: str = None, check_out: str = None, limit: int = 10):
    """Search for available resort listings with date and price filters."""
    return search_available_future_listings_merged(resort_name=resort_name, listing_check_in=check_in, listing_check_out=check_out, limit=limit)

# Register Booking Tools
@mcp.tool()
def user_bookings(email: str, limit: int = 5):
    """Get upcoming and past bookings for a user email."""
    return get_user_bookings(user_email=email, upcoming_limit=limit)

@mcp.tool()
def book_listing(listing_id: int, check_in: str, check_out: str, email: str):
    """Book a specific resort listing."""
    return book_resort_listing(listing_id, check_in, check_out, email)

# Register Utility Tools
@mcp.tool()
def user_profile(email: str):
    """Get user profile summary including booking counts."""
    return get_user_profile(email)

@mcp.tool()
def check_database():
    """Check database connection health."""
    return test_database_connection()

if __name__ == "__main__":
    mcp.run()
