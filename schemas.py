from typing import List, Dict, Any
import datetime
import uuid


def get_resort_details_schema() -> Dict[str, Any]:
    """Schema for get_resort_details to handle ONLY static resort info queries."""
    return {
        "type": "function",
        "function": {
            "name": "get_resort_details",
            "description": (
                "Retrieve static resort details such as name, location, description, images, or amenities.  or comman give me the details about resort name "
                "Use ONLY when the user explicitly asks about a resort itself (e.g., "
                "'Tell me about Bonnet Creeks Resort' or 'What amenities does Club Wyndham have?'). "
                "Do NOT use for nearby restaurants, airports, transport, or sightseeing."
                "Do NOT use for pricing, availability, or reservations."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "resort_id": {"type": "integer", "description": "ID of the resort."},
                    "resort_name": {"type": "string", "description": "Name of the resort."},
                    "amenities_only": {"type": "boolean", "description": "If true, return only amenities."}
                },
                "required": [],
                "additionalProperties": False
            }
        }
    }




def get_city_from_resort_schema() -> Dict[str, Any]:
    """Schema for retrieving the city of a resort by name and optionally filtering POIs by categories."""
    return {
        "type": "function",
        "function": {
            "name": "get_city_from_resort",
            "description": (
                "Get the city of a resort based on its name and optionally retrieve nearby POIs "
                "filtered by categories. Category IDs are: "
                "Top Sights = 1, Restaurants = 2, Airport = 3, Transit = 4."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "resort_name": {
                        "type": "string",
                        "description": "The exact name of the resort (e.g., 'Bonnet Creek Resort')."
                    },
                    "categories": {
                        "type": "array",
                        "description": (
                            "Optional list of POI categories to filter. Allowed values: "
                            "'Top Sights' (1), 'Restaurants' (2), 'Airport' (3), 'Transit' (4). "
                            "If omitted, all categories are returned."
                        ),
                        "items": {
                            "type": "string",
                            "enum": ["Top Sights", "Restaurants", "Airport", "Transit"]
                        }
                    }
                },
                "required": ["resort_name"],
                "additionalProperties": False
            }
        }
    }





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
        "description": ( "Get a list of ALL EXISTING RESORTS in a specific location. "
                        "Use this when the user asks 'show me resorts in [location]' or "
                        "'what resorts are in [location]'. "
                        "This returns resort information, NOT availability or bookings. "
                        "For availability/booking searches, use search_available_future_listings_enhanced instead."),
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


# def get_featured_listings_schema() -> Dict[str, Any]:
#     """Auto-generated schema for get_featured_listings function."""
#     return {
#     "type": "function",
#     "function": {
#         "name": "get_featured_listings",
#         "description": "Get featured listings.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "limit": {
#                     "type": "integer",
#                     "description": "The limit parameter"
#                 }
#             },
#             "required": [],
#             "additionalProperties": False
#         }
#     }
# }


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
        "name": "search_available_future_listings_enhanced",
        "description": "Get price range summary for resorts in a specific location.",
        "parameters": {
            "type": "object",
            "properties": {
                "resort_id": {
                        "type": "integer",
                        "description": "The resort_id parameter"
                    },
                    "listing_check_in": {
                        "type": "string",
                        "description": "Check-in date in YYYY-MM-DD format  if there is not specified  date in  ptompt then give full avaliable  resort or ask the user define the  specify  the date "
                    },
                    "listing_check_out": {
                        "type": "string",
                        "description": "Check-out date in YYYY-MM-DD format if there is not specified  date in  ptompt then give full avaliable  resort  or ask the user define the  specify  the date "
                    },
                 
                    "resort_country": {
                        "type": "string",
                        "description": "Country to search in"
                    },
                    "resort_city": {
                        "type": "string",
                        "description": "City to search in"
                    },
                    "resort_state": {
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
                    },
                    "price_sort": {
                        "type": "string",
                        "description": "Order to sort results by price. Use 'asc' for cheapest listings, 'desc' for most expensive listings."
                    }
            },
            "required": [],
            "additionalProperties": False
        }
    }
}






def get_user_bookings_schema() -> Dict[str, Any]:
    """Schema for get_user_bookings function with optional filters by check-in date (year, month, day)."""
    return {
        "type": "function",
        "function": {
            "name": "get_user_bookings",
            "description": (
                "Fetch upcoming and past bookings for a user by email, including total_listing_price and total_booking_price. "
                "If only the month is specified, the year defaults to the current year (e.g., month=6 means June of the current year). "
                "If no year/month/day is provided, limits of 3 bookings each for upcoming and past are applied. "
                "If the number of bookings in a year is too high (e.g., over 5 to 1000+), the assistant may prompt the user "
                "to specify a month. The function also returns a summary of months with bookings per year."
                "resort_name,booker or user name ,check_in,check_out,reservation_no,total_booking_price,nights,unit_type,listing_status"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "user_email": {
                        "type": "string",
                        "description": "Email address of the user whose bookings are being fetched."
                    },
                    "year": {
                        "type": "integer",
                        "description": "Optional filter for the check-in year (e.g., 2028)."
                    },
                    "month": {
                        "type": "integer",
                        "description": "Optional filter for the check-in month (1-12). If only month is provided, the year defaults to current year."
                    },
                    "day": {
                        "type": "integer",
                        "description": "Optional filter for the check-in day of the month (1-31)."
                    }
                },
                "required": ["user_email"],
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


# def get_weekend_listings_schema() -> Dict[str, Any]:
#     """Auto-generated schema for get_weekend_listings function."""
#     return {
#     "type": "function",
#     "function": {
#         "name": "get_weekend_listings",
#         "description": "Get listings with weekend availability.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "limit": {
#                     "type": "integer",
#                     "description": "The limit parameter"
#                 }
#             },
#             "required": [],
#             "additionalProperties": False
#         }
#     }
# }

# def search_listings_by_type_schema() -> Dict[str, Any]:
#     """Auto-generated schema for search_listings_by_type function."""
#     return {
#     "type": "function",
#     "function": {
#         "name": "search_listings_by_type",
#         "description": "Get listings by type.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "listing_type": {
#                     "type": "string",
#                     "description": "The listing_type parameter"
#                 },
#                 "limit": {
#                     "type": "integer",
#                     "description": "The limit parameter"
#                 }
#             },
#             "required": [
#                 "listing_type"
#             ],
#             "additionalProperties": False
#         }
#     }
# }



def search_resorts_by_amenities_schema() -> Dict[str, Any]:
    """Schema for search_resorts_by_amenities function."""
    return {
        "type": "function",
        "function": {
            "name": "search_resorts_by_amenities",
            "description": (
                "Search for resorts that match the specified amenities. "
                "Matches are case-insensitive. "
                "Can match either ALL amenities (AND) or ANY amenities (OR). "
                "Returns resort details along with their amenities."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "amenities": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": (
                            "List of amenity names to search for. "
                            "Case-insensitive matching against the amenities table."
                        )
                    },
                    "match_all": {
                        "type": "boolean",
                        "description": (
                            "If true, resorts must have ALL specified amenities (AND search). "
                            "If false, resorts with ANY of the specified amenities will match (OR search). "
                            "Defaults to true."
                        ),
                        "default": True
                    },
                    "limit": {
                        "type": "integer",
                        "description": (
                            "Maximum number of resorts to return. "
                            "Defaults to 5."
                        ),
                        "default": 5
                    }
                },
                "required": ["amenities"],
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





def current_date():
    """Get the current date in YYYY-MM-DD format."""
    return datetime.datetime.now().strftime("%Y-%m-%d")


def search_available_future_listings_enhanced_schema() -> Dict[str, Any]:
    today = current_date()
    current_year = datetime.datetime.now().year
    """
    Schema for searching available listings by city, state, country, or general location.
    Unified schema for the search_available_future_listings_enhanced function.
    Supports flexible resort search with filters for location, pricing, unit type,
    currency, sorting, debugging, and date logic.
    Always ensures check-in/check-out dates are in the future (auto-adjusted).

    specifically:
    -> if specified all three year,month,day it will take as it is checkin and check out in pt_rt table .
    1. If no year/month/day is provided, defaults to future dates.
    2. If only month is provided (no year), it resolves to the next upcoming occurrence.

    
    If only month is provided (no year), it resolves to the next upcoming occurrence.
    If year is explicitly provided, it is used as-is (even if past).
    """
    return {
        "type": "function",
        "function": {
            "name": "search_available_future_listings_enhanced",
            "description": (
                "Search for AVAILABLE LISTINGS across multiple resorts in a location (state, city, country, or by holiday). "
                "Use this tool when the user asks about availability in a general area instead of a specific resort. "
                "Example: 'Find me available resorts in Florida in February' or 'Show me listings in Hawaii this summer.' "
                "Do NOT use this tool for static resort details (use get_resort_details) "
                "or for availability at a single named resort (use search_available_future_listings_enhanced_v2)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    # Resort/location filters
                    "resort_id": {
                        "type": "integer",
                        "description": "Unique resort ID (optional)."
                    },
                    "resort_name": {
                        "type": "string",
                        "description": "Name of the resort to search for (optional if location is provided)."
                    },
                    "resort_country": {
                        "type": "string",
                        "description": "Country where the resort is located."
                    },
                    "resort_state": {
                        "type": "string",
                        "description": "State or province where the resort is located."
                    },
                    "resort_city": {
                        "type": "string",
                        "description": "City where the resort is located."
                    },

                    # Date filters
                   "month": {
                        "type": "string",
                        "description": (
                            "Filter for check-in month (name or number, e.g., 'Jan' or 1-12). "
                            "Always used with automatic future year mapping if year not explicitly set."
                        )
                    },
                    "year": {
                        "type": "integer",
                        "description": (
                            "Optional filter for check-in year. "
                            "If not provided, the system automatically resolves to the correct future year."
                        )
                    },

                    # Pricing / currency
                 
                
                    "currency_code": {
                        "type": "string",
                        "description": "Currency code for price (e.g., USD, EUR, INR)."
                    },
                    "price_sort": {
                        "type": "string",
                        "description": (
                            "Sort results by price. "
                            "Use 'asc' for lowest to highest, 'desc' for highest to lowest, "
                            "'avg_price' for resort average, 'cheapest', 'average', or 'highest'."
                        )
                    },

                    # Unit / type filters
                    "unit_type": {
                        "type": "string",
                        "description": "Specific unit type to filter (e.g., Studio, 1 Bedroom, Suite)."
                    },

                    "min_guests": {
                       "type": "integer",
                       "description": "Minimum guest capacity required (filters by unit_types.sleeps)."
                    },
                     "listing_cancelation_date": {
                        "type": "string",
                        "format": "date",
                        "description": "The date when the user can cancel the booking, in YYYY-MM-DD format.eg: Cancellation: Full refund if canceled at least 16 days before check-in. (By 2025-12-07)"

                        
                    },

                    "cancellation_policy": {
                        "type": "string",
                        "description": "Filter listings by cancellation policy.",
                        "enum": ["flexible", "relaxed", "moderate", "firm", "strict"],
                        "x-enumDescriptions": {
                            "flexible": "Full refund if canceled at least 3 days before check-in.",
                            "relaxed": "Full refund if canceled at least 16 days before check-in.",
                            "moderate": "Full refund if canceled at least 32 days before check-in.",
                            "firm": "Full refund if canceled at least 62 days before check-in.",
                            "strict": "Booking is non-refundable."
                        }
                    },

                    "listing_url": {
                        "type": "string",
                        "description": "The URL to the resort's listing page."
                    },
                    "booking_url": {
                        "type": "string",
                        "description": "The URL to book the resort directly with the given check-in and check-out dates."
                    },
                                


 
                    # Options
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of listings to return (default: 30)."
                    },
                    "flexible_dates": {
                        "type": "boolean",
                        "description": "Search for alternative dates if exact not available (default: true)."
                    },
                    "debug": {
                        "type": "boolean",
                        "description": "Enable verbose output for debugging (default: false)."
                    }
                },
                "required": [],
                "additionalProperties": False
            }
        }
    }




def search_available_future_listings_enhanced_v2_schema() -> Dict[str, Any]:
    today = current_date()
    current_year = datetime.datetime.now().year
    """
    Unified schema for the search_available_future_listings_enhanced_v2 function.
    specified resort name or slug with listings details
    Supports flexible resort search with filters for location, pricing, unit type,
    only for this type of input {resort name} give me the listings details with price and availability
    """
    return {
        "type": "function",
        "function": {
            "name": "search_available_future_listings_enhanced_v2",
            "description": (
                "Search for AVAILABLE LISTINGS at a specific resort, including pricing, unit type, guest capacity, "
                "and cancellation policy. "
                "Use this tool when the user asks about availability, stays, or prices at ONE resort. "
                "Example: 'Show me listings at Club Wyndham Ocean Walk in March under $200/night' or "
                "'Find me a 2-bedroom deluxe at Bonnet Creek for 6 guests in July.' "
                "Do NOT use this tool for static resort details (use get_resort_details instead). "
                "Do NOT use this tool for general area searches across multiple resorts "
                "(use search_available_future_listings_enhanced instead)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    # Resort/location filters
                    "resort_id": {
                        "type": "integer",
                        "description": "Unique resort ID (optional)."
                    },
                    "resort_name": {
                        "type": "string",
                        "description": "Name of the resort to search for (optional if location is provided)."
                    },
                    "resort_country": {
                        "type": "string",
                        "description": "Country where the resort is located."
                    },
                    "resort_state": {
                        "type": "string",
                        "description": "State or province where the resort is located."
                    },
                    "resort_city": {
                        "type": "string",
                        "description": "City where the resort is located."
                    },

                    # Date filters
                   "month": {
                        "type": "string",
                        "description": (
                            "Filter for check-in month (name or number, e.g., 'Jan' or 1-12). "
                            "Always used with automatic future year mapping if year not explicitly set."
                        )
                    },
                    "year": {
                        "type": "integer",
                        "description": (
                            "Optional filter for check-in year. "
                            "If not provided, the system automatically resolves to the correct future year."
                        )
                    },

                    # Pricing / currency
            
                    "currency_code": {
                        "type": "string",
                        "description": "Currency code for price (e.g., USD, EUR, INR)."
                    },
                    "price_sort": {
                        "type": "string",
                        "description": (
                            "Sort results by price. "
                            "Use 'asc' for lowest to highest, 'desc' for highest to lowest, "
                            "'avg_price' for resort average, 'cheapest', 'average', or 'highest'."
                        )
                    },

                    # Unit / type filters
                    "unit_type": {
                        "type": "string",
                        "description": "Specific unit type to filter (e.g., Studio, 1 Bedroom, Suite)."
                    },

                    "min_guests": {
                       "type": "integer",
                       "description": "Minimum guest capacity required (filters by unit_types.sleeps)."
                    },
                     "listing_cancelation_date": {
                        "type": "string",
                        "format": "date",
                        "description": "The date when the user can cancel the booking, in YYYY-MM-DD format.eg: Cancellation: Full refund if canceled at least 16 days before check-in. (By 2025-12-07)"

                        
                    },

                    "cancellation_policy": {
                        "type": "string",
                        "description": "Filter listings by cancellation policy.",
                        "enum": ["flexible", "relaxed", "moderate", "firm", "strict"],
                        "x-enumDescriptions": {
                            "flexible": "Full refund if canceled at least 3 days before check-in.",
                            "relaxed": "Full refund if canceled at least 16 days before check-in.",
                            "moderate": "Full refund if canceled at least 32 days before check-in.",
                            "firm": "Full refund if canceled at least 62 days before check-in.",
                            "strict": "Booking is non-refundable."
                        }
                    },

                    "listing_url": {
                        "type": "string",
                        "description": "The URL to the resort's listing page."
                    },
                    "booking_url": {
                        "type": "string",
                        "description": "The URL to book the resort directly with the given check-in and check-out dates."
                    },
                                


 
                    # Options
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of listings to return (default: 30)."
                    },
                    "flexible_dates": {
                        "type": "boolean",
                        "description": "Search for alternative dates if exact not available (default: true)."
                    },
                    "debug": {
                        "type": "boolean",
                        "description": "Enable verbose output for debugging (default: false)."
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
        # get_featured_listings_schema(),
        get_listing_details_schema(),
        get_resort_details_schema(),
        get_price_range_summary_schema(),
        
        

        get_city_from_resort_schema(),


        get_user_bookings_schema(),
        get_user_profile_schema(),
        # get_weekend_listings_schema(),
        # search_listings_by_type_schema(),
        # search_resorts_by_amenities_schema(),
        test_database_connection_schema(),
        search_available_future_listings_enhanced_schema(),  # Enhanced version
        search_available_future_listings_enhanced_v2_schema(),  # New v2 version
    ]

# Export all schemas as a list
ALL_FUNCTION_SCHEMAS = get_all_function_schemas()