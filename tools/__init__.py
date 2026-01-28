from typing import Any, Dict, List, Optional
from tools.resort_tools import (
    get_city_from_resort, 
    get_available_resorts, 
    get_resort_details, 
    search_resorts_by_amenities
)
from tools.booking_tools import (
    get_user_bookings, 
    book_resort_listing, 
    get_payment_methods, 
    get_cancellation_policy
)
from tools.search_tools import search_available_future_listings_merged
from tools.utils import get_user_profile, test_database_connection
from src.database.db import get_database_url, initialize_database
from tools.schema_utils import generate_schema

# Registry for Streamlit UI compatibility
AVAILABLE_TOOLS = {
    "get_user_bookings": get_user_bookings,
    "get_available_resorts": get_available_resorts,
    "get_resort_details": get_resort_details,
    "search_available_future_listings_merged": search_available_future_listings_merged,
    "search_available_future_listings_enhanced": search_available_future_listings_merged, # Alias
    "search_available_future_listings_enhanced_v2": search_available_future_listings_merged, # Alias
    "get_city_from_resort": get_city_from_resort,
    "search_resorts_by_amenities": search_resorts_by_amenities,
    "get_user_profile": get_user_profile,
    "test_database_connection": test_database_connection,
    "get_database_url": get_database_url,
    "book_resort_listing": book_resort_listing,
    "get_payment_methods": get_payment_methods,
    "get_cancellation_policy": get_cancellation_policy,
}

def call_tool(tool_name: str, **kwargs) -> Any:
    """
    Call a tool function by name with given arguments.
    Used by streamlit_app.py to interact with the backend.
    """
    if tool_name not in AVAILABLE_TOOLS:
        return {"error": f"Tool '{tool_name}' not found"}
    
    try:
        return AVAILABLE_TOOLS[tool_name](**kwargs)
    except Exception as e:
        return {"error": f"Error calling tool '{tool_name}': {str(e)}"}

# Automatically generate schemas for all available tools
ALL_FUNCTION_SCHEMAS = [generate_schema(func) for func in AVAILABLE_TOOLS.values()]
