"""
OpenAI-compatible function tool schemas for MySQL resort booking system.
"""
from typing import List, Dict, Any


def get_user_bookings_schema() -> Dict[str, Any]:
    """OpenAI function schema for get_user_bookings function."""
    return {
        "type": "function",
        "function": {
            "name": "get_user_bookings",
            "description": "Fetch all bookings for a user by their email address",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_email": {
                        "type": "string",
                        "description": "The email address of the user to fetch bookings for"
                    }
                },
                "required": ["user_email"],
                "additionalProperties": False
            }
        }
    }


def get_available_resorts_schema() -> Dict[str, Any]:
    """OpenAI function schema for get_available_resorts function."""
    return {
        "type": "function",
        "function": {
            "name": "get_available_resorts",
            "description": "List all available resorts with optional filtering by country and status",
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "description": "Optional country filter to search resorts in a specific country"
                    },
                    "status": {
                        "type": "string",
                        "description": "Resort status filter (active, pending). Default is 'active'"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of resorts to return (default: 10)"
                    }
                },
                "required": [],
                "additionalProperties": False
            }
        }
    }


def get_resort_details_schema() -> Dict[str, Any]:
    """OpenAI function schema for get_resort_details function."""
    return {
        "type": "function",
        "function": {
            "name": "get_resort_details",
            "description": "Get detailed information about a specific resort by its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "resort_id": {
                        "type": "integer",
                        "description": "The ID of the resort to get details for"
                    }
                },
                "required": ["resort_id"],
                "additionalProperties": False
            }
        }
    }


def search_available_listings_schema() -> Dict[str, Any]:
    """OpenAI function schema for search_available_listings function."""
    return {
        "type": "function",
        "function": {
            "name": "search_available_listings",
            "description": "Search for available listings with various filters like resort, dates, nights, and country",
            "parameters": {
                "type": "object",
                "properties": {
                    "resort_id": {
                        "type": "integer",
                        "description": "Optional resort ID to filter listings for a specific resort"
                    },
                    "check_in_date": {
                        "type": "string",
                        "description": "Optional check-in date filter in YYYY-MM-DD format"
                    },
                    "check_out_date": {
                        "type": "string",
                        "description": "Optional check-out date filter in YYYY-MM-DD format"
                    },
                    "nights": {
                        "type": "integer",
                        "description": "Optional number of nights filter"
                    },
                    "country": {
                        "type": "string",
                        "description": "Optional country filter to search listings in a specific country"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of listings to return (default: 20)"
                    }
                },
                "required": [],
                "additionalProperties": False
            }
        }
    }


def get_booking_details_schema() -> Dict[str, Any]:
    """OpenAI function schema for get_booking_details function."""
    return {
        "type": "function",
        "function": {
            "name": "get_booking_details",
            "description": "Get detailed information about a specific booking by its ID, with selective field returns based on user query",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_id": {
                        "type": "integer",
                        "description": "The ID of the booking to get details for"
                    },
                    "fields": {
                        "type": "string",
                        "description": "What fields to return: 'price' (only pricing info), 'dates' (only date info), 'basic' (key booking details), 'participants' (booker and owner info), 'resort' (resort details), 'all' (complete details). Default is 'all'",
                        "enum": ["price", "dates", "basic", "participants", "resort", "all"]
                    }
                },
                "required": ["booking_id"],
                "additionalProperties": False
            }
        }
    }


def get_user_profile_schema() -> Dict[str, Any]:
    """OpenAI function schema for get_user_profile function."""
    return {
        "type": "function",
        "function": {
            "name": "get_user_profile",
            "description": "Get user profile information including bookings and listings statistics",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_email": {
                        "type": "string",
                        "description": "The email address of the user to get profile for"
                    }
                },
                "required": ["user_email"],
                "additionalProperties": False
            }
        }
    }


def get_all_function_schemas() -> List[Dict[str, Any]]:
    """Get all OpenAI-compatible function schemas."""
    return [
        get_user_bookings_schema(),
        get_available_resorts_schema(),
        get_resort_details_schema(),
        search_available_listings_schema(),
        get_booking_details_schema(),
        get_user_profile_schema()
    ]


# Export individual schemas for convenience
GET_USER_BOOKINGS_SCHEMA = get_user_bookings_schema()
GET_AVAILABLE_RESORTS_SCHEMA = get_available_resorts_schema()
GET_RESORT_DETAILS_SCHEMA = get_resort_details_schema()
SEARCH_AVAILABLE_LISTINGS_SCHEMA = search_available_listings_schema()
GET_BOOKING_DETAILS_SCHEMA = get_booking_details_schema()
GET_USER_PROFILE_SCHEMA = get_user_profile_schema()

# Export all schemas as a list
ALL_FUNCTION_SCHEMAS = get_all_function_schemas() 