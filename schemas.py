from typing import List, Dict, Any


def get_amenity_details_schema() -> Dict[str, Any]:
    """Auto-generated schema for get_amenity_details function."""
    return {
    "type": "function",
    "function": {
        "name": "get_amenity_details",
        "description": "Get all details for a specific amenity by its ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "amenity_id": {
                    "type": "integer",
                    "description": "The amenity_id parameter"
                }
            },
            "required": [
                "amenity_id"
            ],
            "additionalProperties": False
        }
    }
}


def get_available_resorts_schema() -> Dict[str, Any]:
    """Auto-generated schema for get_available_resorts function."""
    return {
    "type": "function",
    "function": {
        "name": "get_available_resorts",
        "description": "List all available resorts with their basic information",
        "parameters": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "description": "The country parameter"
                },
                "city": {
                    "type": "string",
                    "description": "The city parameter"
                },
                "state": {
                    "type": "string",
                    "description": "The state parameter"
                },
                "status": {
                    "type": "string",
                    "description": "The status parameter"
                },
                "limit": {
                    "type": "integer",
                    "description": "The limit parameter"
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
}


def get_booking_details_schema() -> Dict[str, Any]:
    """Auto-generated schema for get_booking_details function."""
    return {
    "type": "function",
    "function": {
        "name": "get_booking_details",
        "description": "Get detailed information about a specific booking by its ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "booking_id": {
                    "type": "integer",
                    "description": "The booking_id parameter"
                },
                "fields": {
                    "type": "string",
                    "description": "The fields parameter"
                }
            },
            "required": [
                "booking_id"
            ],
            "additionalProperties": False
        }
    }
}


def get_database_url_schema() -> Dict[str, Any]:
    """Auto-generated schema for get_database_url function."""
    return {
    "type": "function",
    "function": {
        "name": "get_database_url",
        "description": "Get database URL from environment variables.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
}


def get_featured_listings_schema() -> Dict[str, Any]:
    """Auto-generated schema for get_featured_listings function."""
    return {
    "type": "function",
    "function": {
        "name": "get_featured_listings",
        "description": "Get featured listings.",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "The limit parameter"
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
}


def get_listing_details_schema() -> Dict[str, Any]:
    """Auto-generated schema for get_listing_details function."""
    return {
    "type": "function",
    "function": {
        "name": "get_listing_details",
        "description": "Get all details for a specific listing by its ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "listing_id": {
                    "type": "integer",
                    "description": "The listing_id parameter"
                }
            },
            "required": [
                "listing_id"
            ],
            "additionalProperties": False
        }
    }
}


def get_price_range_summary_schema() -> Dict[str, Any]:
    """Auto-generated schema for get_price_range_summary function."""
    return {
    "type": "function",
    "function": {
        "name": "get_price_range_summary",
        "description": "Get price range summary for resorts in a specific location.",
        "parameters": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "description": "The country parameter"
                },
                "state": {
                    "type": "string",
                    "description": "The state parameter"
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
}


def get_resort_details_schema() -> Dict[str, Any]:
    """Auto-generated schema for get_resort_details function."""
    return {
    "type": "function",
    "function": {
        "name": "get_resort_details",
        "description": "Get detailed information about a specific resort",
        "parameters": {
            "type": "object",
            "properties": {
                "resort_id": {
                    "type": "integer",
                    "description": "The resort_id parameter"
                }
            },
            "required": [
                "resort_id"
            ],
            "additionalProperties": False
        }
    }
}


def get_resort_price_schema() -> Dict[str, Any]:
    """Auto-generated schema for get_resort_price function."""
    return {
    "type": "function",
    "function": {
        "name": "get_resort_price",
        "description": "Enhanced version of get_resort_price with better debugging and flexible matching.",
        "parameters": {
            "type": "object",
            "properties": {
                "resort_name": {
                    "type": "string",
                    "description": "The resort_name parameter"
                },
                "country": {
                    "type": "string",
                    "description": "The country parameter"
                },
                "city": {
                    "type": "string",
                    "description": "The city parameter"
                },
                "state": {
                    "type": "string",
                    "description": "The state parameter"
                },
                "min_price": {
                    "type": "number",
                    "description": "The min_price parameter"
                },
                "max_price": {
                    "type": "number",
                    "description": "The max_price parameter"
                },
                "unit_type": {
                    "type": "string",
                    "description": "The unit_type parameter"
                },
                "nights": {
                    "type": "integer",
                    "description": "The nights parameter"
                },
                "currency_code": {
                    "type": "string",
                    "description": "The currency_code parameter"
                },
                "limit": {
                    "type": "integer",
                    "description": "The limit parameter"
                },
                "debug": {
                    "type": "boolean",
                    "description": "The debug parameter"
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
}


def get_user_bookings_schema() -> Dict[str, Any]:
    """Auto-generated schema for get_user_bookings function."""
    return {
    "type": "function",
    "function": {
        "name": "get_user_bookings",
        "description": "Fetch all bookings for a user by name",
        "parameters": {
            "type": "object",
            "properties": {
                "user_email": {
                    "type": "string",
                    "description": "The user_email parameter"
                }
            },
            "required": [
                "user_email"
            ],
            "additionalProperties": False
        }
    }
}


def get_user_profile_schema() -> Dict[str, Any]:
    """Auto-generated schema for get_user_profile function."""
    return {
    "type": "function",
    "function": {
        "name": "get_user_profile",
        "description": "Get user profile information.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_email": {
                    "type": "string",
                    "description": "The user_email parameter"
                }
            },
            "required": [
                "user_email"
            ],
            "additionalProperties": False
        }
    }
}


def get_weekend_listings_schema() -> Dict[str, Any]:
    """Auto-generated schema for get_weekend_listings function."""
    return {
    "type": "function",
    "function": {
        "name": "get_weekend_listings",
        "description": "Get listings with weekend availability.",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "The limit parameter"
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
}





def search_listings_by_type_schema() -> Dict[str, Any]:
    """Auto-generated schema for search_listings_by_type function."""
    return {
    "type": "function",
    "function": {
        "name": "search_listings_by_type",
        "description": "Get listings by type.",
        "parameters": {
            "type": "object",
            "properties": {
                "listing_type": {
                    "type": "string",
                    "description": "The listing_type parameter"
                },
                "limit": {
                    "type": "integer",
                    "description": "The limit parameter"
                }
            },
            "required": [
                "listing_type"
            ],
            "additionalProperties": False
        }
    }
}

def search_resorts_by_amenities_schema() -> Dict[str, Any]:
    """Auto-generated schema for search_resorts_by_amenities function."""
    return {
    "type": "function",
    "function": {
        "name": "search_resorts_by_amenities",
        "description": "Search for resorts that have specific amenities.",
        "parameters": {
            "type": "object",
            "properties": {
                "amenities": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "The amenities parameter"
                },
                "limit": {
                    "type": "integer",
                    "description": "The limit parameter"
                }
            },
            "required": [
                "amenities"
            ],
            "additionalProperties": False
        }
    }
}


def test_database_connection_schema() -> Dict[str, Any]:
    """Auto-generated schema for test_database_connection function."""
    return {
    "type": "function",
    "function": {
        "name": "test_database_connection",
        "description": "Test if the database connection works.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
}
def search_available_future_listings_enhanced_schema() -> Dict[str, Any]:
    """Auto-generated schema for search_available_future_listings_enhanced function."""
    return {
        "type": "function",
        "function": {
            "name": "search_available_future_listings_enhanced",
            "description": "Enhanced search for available future listings with fallback options and better user guidance. Returns both results and suggestions for alternative searches when no exact matches are found.",
            "parameters": {
                "type": "object",
                "properties": {
                    "resort_id": {
                        "type": "integer",
                        "description": "The resort_id parameter"
                    },
                    "check_in_date": {
                        "type": "string",
                        "description": "Check-in date in YYYY-MM-DD format"
                    },
                    "check_out_date": {
                        "type": "string",
                        "description": "Check-out date in YYYY-MM-DD format"
                    },
                    "nights": {
                        "type": "integer",
                        "description": "Number of nights for the stay"
                    },
                    "country": {
                        "type": "string",
                        "description": "Country to search in"
                    },
                    "city": {
                        "type": "string",
                        "description": "City to search in"
                    },
                    "state": {
                        "type": "string",
                        "description": "State to search in"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default: 20)"
                    },
                    "flexible_dates": {
                        "type": "boolean",
                        "description": "Whether to search for alternative dates if exact dates not available (default: true)"
                    },
                    "debug": {
                        "type": "boolean",
                        "description": "Enable debug output (default: false)"
                    }
                },
                "required": [],
                "additionalProperties": False
            }
        }
    }


def get_availability_insights_schema() -> Dict[str, Any]:
    """Auto-generated schema for get_availability_insights function."""
    return {
        "type": "function",
        "function": {
            "name": "get_availability_insights",
            "description": "Get insights about availability patterns to help users understand when to search. Provides monthly distribution, popular durations, price statistics, and recommendations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "country": {
                        "type": "string",
                        "description": "Optional country filter for availability insights"
                    },
                    "days_ahead": {
                        "type": "integer",
                        "description": "Number of days ahead to analyze (default: 90)"
                    }
                },
                "required": [],
                "additionalProperties": False
            }
        }
    }


# Updated get_all_function_schemas to include the new functions
def get_all_function_schemas() -> List[Dict[str, Any]]:
    """Get all auto-generated OpenAI-compatible function schemas including enhanced versions."""
    return [
        get_amenity_details_schema(),
        get_available_resorts_schema(),
        get_booking_details_schema(),
        get_database_url_schema(),
        get_featured_listings_schema(),
        get_listing_details_schema(),
        get_resort_details_schema(),
        get_price_range_summary_schema(),
        get_resort_price_schema(),
        get_user_bookings_schema(),
        get_user_profile_schema(),
        get_weekend_listings_schema(),
        search_listings_by_type_schema(),
        search_resorts_by_amenities_schema(),
        test_database_connection_schema(),
        search_available_future_listings_enhanced_schema(),  # Enhanced version
        get_availability_insights_schema(),  # New insights function
    ]



# Export all schemas as a list
ALL_FUNCTION_SCHEMAS = get_all_function_schemas()