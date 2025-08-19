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
        "description": "List all available resorts with their basic information"
                        "the count of activate listings, and the total number of bookings. it manditory",
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
                    "listing_price_night": {
                        "type": "integer",
                        "description": "Number of nights for the stay incase price is present in the prompt then call listing_price_night ar  ugement "
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

# details_with_out imag

# def get_resort_details_schema() -> Dict[str, Any]:
#     """Schema for get_resort_details function, supporting ID or Name and includes unit types."""
#     return {
#         "type": "function",
#         "function": {
#             "name": "get_resort_details",
#             "description": "Get detailed information about a specific resort using either ID or Name. Returns resort details including unit types, listing stats, and total bookings.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "resort_id": {
#                         "type": "integer",
#                         "description": "The ID of the resort to retrieve details for"
#                     },
#                     "resort_name": {
#                         "type": "string",
#                         "description": "The name of the resort to retrieve details for"
#                     }
                    

#                 },
#                 "required": [],
#                 "additionalProperties": False
#             }
#         }
#     }
# with img
# def get_resort_details_schema() -> Dict[str, Any]:
#     """Schema for get_resort_details function, supporting ID or Name and including amenities, unit types, listings, and top image."""
#     return {
#         "type": "function",
#         "function": {
#             "name": "get_resort_details",
#             "description": (
#                 "List of amenity names to search for. Must match all provided amenities."
#                 "Get detailed information about a specific resort using either ID or Name. "
#                 "Returns resort details including amenities, unit types, listing stats, total bookings, "
#                 "and the top resort image (only the image filename, no URL)."
#                 "Search for resorts that have all the specified amenities. "
#                 "Matches are case-insensitive. "
#                 "Returns resort details along with their amenities."
#             ),
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "resort_id": {
#                         "type": "integer",
#                         "description": "The ID of the resort to retrieve details for."
#                     },
#                     "resort_name": {
#                         "type": "string",
#                         "description": "The name of the resort to retrieve details for."
#                     }
#                 },
#                 "required": [],
#                 "additionalProperties": False
#             }
#         }
#     }

# def get_resort_details_schema() -> Dict[str, Any]:
#     """Unified schema for get_resort_details to handle search by ID, Name, or Amenities."""
#     return {
#         "type": "function",
#         "function": {
#             "name": "get_resort_details",
#             "description": (
#                 "Get resort details or search for resorts by amenities.\n"
#                 "Modes:\n"
#                 "1. Provide resort_id or resort_name → returns details for that resort.\n"
#                 "2. Provide amenities_list → returns resorts that have ALL those amenities.\n"
#                 "Case-insensitive matching is used for amenities.\n"
#                 "Results include resort info, amenities, unit types, listings, and top image."
#             ),
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "resort_id": {
#                         "type": "integer",
#                         "description": "The ID of the resort to retrieve details for."
#                     },
#                     "resort_name": {
#                         "type": "string",
#                         "description": "The name of the resort to retrieve details for (case-insensitive partial match allowed)."
#                     },
#                     "amenities_list": {
#                         "type": "array",
#                         "items": {"type": "string"},
#                         "description": (
#                             "List of amenity names to search for. "
#                             "Must match all provided amenities (case-insensitive)."
#                         )
#                     },
#                     "amenities_only": {
#                         "type": "boolean",
#                         "description": "If true, returns only the amenities for the given resort_id or resort_name."
#                     },
#                     "list_resorts_with_amenities": {
#                         "type": "boolean",
#                         "description": "If true, lists all resorts with their amenities."
#                     },
#                     "limit": {
#                         "type": "integer",
#                         "description": "Maximum number of resorts to return. Defaults to 10."
#                     }
#                 },
#                 "required": [],
#                 "additionalProperties": False
#             }
#         }
#     }
def get_resort_details_schema() -> Dict[str, Any]:
    """Compact schema for get_resort_details to handle ID, Name, or Amenities search."""
    return {
        "type": "function",
        "function": {
            "name": "get_resort_details",
            "description": (
                "Retrieve resort details by ID or name, or search resorts by amenities. "
                "Amenities search matches all given amenities (case-insensitive)."
                "resort name with price based question means to call in this tool search_available_future_listings_enhanced "
                "if asking any specify resort details means the image must show"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "resort_id": {
                        "type": "integer",
                        "description": "ID of the resort."
                    },
                    "resort_name": {
                        "type": "string",
                        "description": "Name of the resort (case-insensitive partial match allowed)."
                    },
                    "amenities_list": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Amenities to match (all must be present)."
                    },
                    "amenities_only": {
                        "type": "boolean",
                        "description": "If true, returns only amenities for the given resort."
                    },
                    "list_resorts_with_amenities": {
                        "type": "boolean",
                        "description": "If true, lists all resorts with amenities."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max number of resorts to return."
                    }
                },
                "required": [],
                "additionalProperties": False
            }
        }
    }



# def get_resort_price_schema() -> Dict[str, Any]:
#     """Auto-generated schema for get_resort_price function."""
#     return {
#     "type": "function",
#     "function": {
#         "name": "search_available_future_listings_enhanced",
#         "description": "Enhanced version of get_resort_price with better debugging and flexible matching.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "resort_name": {
#                     "type": "string",
#                     "description": "The resort_name parameter"
#                 },
#                 "resort_country": {
#                     "type": "string",
#                     "description": "The country parameter"
#                 },
#                 "resort_city": {
#                     "type": "string",
#                     "description": "The city parameter"
#                 },
#                 "resort_state": {
#                     "type": "string",
#                     "description": "The state parameter"
#                 },
#                 "min_price": {
#                     "type": "number",
#                     "description": "The min_price parameter"
#                 },
#                 "max_price": {
#                     "type": "number",
#                     "description": "The max_price parameter"
#                 },
#                 "unit_type": {
#                     "type": "string",
#                     "description": "The unit_type parameter"
#                 },
#                 "listing_pricing_night": {
#                     "type": "integer",
#                     "description": "The nights parameter"
#                 },
#                 "currency_code": {
#                     "type": "string",
#                     "description": "The currency_code parameter"
#                 },
#                 "limit": {
#                     "type": "integer",
#                     "description": "The limit parameter"
#                 },
#                 "debug": {
#                     "type": "boolean",
#                     "description": "The debug parameter"
#                 },
#                 "price_sort": {
#                         "type": "string",
#                         "description": "Order to sort results by price. Use 'asc' for cheapest listings, 'desc' for most expensive listings."
#                 }
#             },
#             "required": [],
#             "additionalProperties": False
#         }
#     }
# }


def get_resort_price_schema() -> Dict[str, Any]:
    """
    Schema for the search_available_future_listings_enhanced function.
    This enhanced version supports flexible filtering based on resort location, price range,
    unit type, and other options. Also includes support for debugging and price sorting.
    """
    return {
        "type": "function",
        "function": {
            "name": "search_available_future_listings_enhanced",
            "description": (
                "Search for available future resort listings with advanced filters. "
                "Supports location (country, state, city), price range, unit type, nights, "
                "currency code, sorting by price, and debugging options."
            ),
            "parameters": {
                "type": "object",
                "properties": {
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
                    "min_price": {
                        "type": "number",
                        "description": "Minimum price per night to filter listings."
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price per night to filter listings."
                    },
                    "unit_type": {
                        "type": "string",
                        "description": "Specific unit type to filter (e.g., Studio, 1 Bedroom, Suite)."
                    },
                    "listing_pricing_night": {
                        "type": "integer",
                        "description": "Number of nights for the booking (used for total price calculation)."
                    },
                    "currency_code": {
                        "type": "string",
                        "description": "Currency code for price (e.g., USD, EUR, INR)."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of listings to return."
                    },
                    "debug": {
                        "type": "boolean",
                        "description": "Enable verbose output for debugging (optional)."
                    },
                    "price_sort": {
                        "type": "string",
                        "description": "Sort results by price. Use 'asc' for lowest to highest, 'desc' for highest to lowest."
                    }
                },
                "required": [],
                "additionalProperties": False
            }
        }
    }




# def get_user_bookings_schema() -> Dict[str, Any]:
#     """Schema for get_user_bookings function with optional date filters."""
#     return {
#         "type": "function",
#         "function": {
#             "name": "get_user_bookings",
#             "description": "Fetch upcoming and filtered past bookings for a user by email. You can optionally filter past bookings by year, month, or day of check-in date.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "user_email": {
#                         "type": "string",
#                         "description": "Email address of the user."
#                     },
#                     "year": {
#                         "type": "integer",
#                         "description": "Filter past and upcoming  bookings by check-in year (e.g., 2023)."
#                     },
#                     "month": {
#                         "type": "integer",
#                         "description": "Filter past  and upcoming bookings by check-in month (1-12)."
#                     },
#                     "day": {
#                         "type": "integer",
#                         "description": "Filter past and upcoming bookings by check-in day of month (1-31)."
#                     }
#                 },
#                 "required": ["user_email"],
#                 "additionalProperties": False
#             }
#         }
#     }


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
# in live 
# def search_resorts_by_amenities_schema() -> Dict[str, Any]:
#     """Auto-generated schema for search_resorts_by_amenities function."""
#     return {
#     "type": "function",
#     "function": {
#         "name": "search_resorts_by_amenities",
#         "description": "Search for resorts that have specific amenities.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "amenities": {
#                     "type": "array",
#                     "items": {
#                         "type": "string"
#                     },
#                     "description": "The amenities parameter"
#                 },
#                 "limit": {
#                     "type": "integer",
#                     "description": "The limit parameter"
#                 }
#             },
#             "required": [
#                 "amenities"
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

#-----1
# def search_available_future_listings_enhanced_schema() -> Dict[str, Any]:
#     """Auto-generated schema for search_available_future_listings_enhanced function."""
#     "If only the month is specified, the year defaults to the current year or resquest (e.g., month=6 means June of the current year). "
#     return {
#         "type": "function",
#         "function": {
#             "name": "search_available_future_listings_enhanced",
#             "description": "Enhanced search for available future listings with fallback options and better user guidance. Returns both results and suggestions for alternative searches when no exact matches are found.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "resort_id": {
#                         "type": "integer",
#                         "description": "The resort_id parameter"
#                     },
#                     "listing_check_in": {
#                         "type": "string",
#                         "description": "Check-in date in YYYY-MM-DD format"
#                     },
#                     "listing_check_out": {
#                         "type": "string",
#                         "description": "Check-out date in YYYY-MM-DD format"
#                     },
#                     "listing_price_night": {
#                         "type": "integer",
#                         "description": "Number of nights for the stay"
#                     },
#                     "resort_country": {
#                         "type": "string",
#                         "description": "Country to search in"
#                     },
#                     "resort_city": {
#                         "type": "string",
#                         "description": "City to search in"
#                     },
#                     "month": {
#                         "type": "integer",
#                         "description": "Optional filter for the check-in month (1-12). If only month is provided, the year defaults to current year."
#                     },
#                     "resort_state": {
#                         "type": "string",
#                         "description": "State to search in"
#                     },
#                     "limit": {
#                         "type": "integer",
#                         "description": "Maximum number of results to return (default: 30)"
#                     },
#                     "flexible_dates": {
#                         "type": "boolean",
#                         "description": "Whether to search for alternative dates if exact dates not available (default: true)"
#                     },
#                     "debug": {
#                         "type": "boolean",
#                         "description": "Enable debug output (default: false)"
#                     }
#                 },
#                 "required": [],
#                 "additionalProperties": False
#             }
#         }
#     }

def search_available_future_listings_enhanced_schema() -> Dict[str, Any]:
    """Auto-generated schema for search_available_future_listings_enhanced function."""
    return {
        "type": "function",
        "function": {
            "name": "search_available_future_listings_enhanced",
            "description": (
                "Enhanced search for available future listings with fallback options and better user guidance. "
                "If only the month is provided (no year), the system applies special rules based on today's date: "
                "Jun, Jul, Oct → year = 2026; Sep, Nov → year = 2025; Aug → current year (starting from today’s day if in Aug); "
                "All other months → current year unless the month has already passed, in which case next year is used."
                "resort name with price based question means to call in this tool  search_available_future_listings_enhanced "
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "resort_id": {"type": "integer", "description": "The resort_id parameter"},
                    "listing_check_in": {"type": "string", "description": "Check-in date in YYYY-MM-DD format"},
                    "listing_check_out": {"type": "string", "description": "Check-out date in YYYY-MM-DD format"},
                    "listing_price_night": {"type": "integer", "description": "Number of nights for the stay"},
                    "resort_country": {"type": "string", "description": "Country to search in"},
                    "resort_city": {"type": "string", "description": "City to search in"},
                    "month": {
                        "type": "integer",
                        "description": (
                            "Optional filter for the check-in month (1-12). "
                            "If provided without year, uses special mapping rules based on current date."
                        )
                    },
                    "year": {
                        "type": "integer",
                        "description": "Optional filter for the check-in year (overrides special rules if provided)"
                    },
                    "resort_state": {"type": "string", "description": "State to search in"},
                    "limit": {"type": "integer", "description": "Maximum number of results to return (default: 30)"},
                    "flexible_dates": {"type": "boolean", "description": "Whether to search for alternative dates if exact dates not available (default: true)"},
                    "debug": {"type": "boolean", "description": "Enable debug output (default: false)"}
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
        get_resort_price_schema(),
        get_user_bookings_schema(),
        get_user_profile_schema(),
        # get_weekend_listings_schema(),
        search_listings_by_type_schema(),
        # search_resorts_by_amenities_schema(),
        test_database_connection_schema(),
        search_available_future_listings_enhanced_schema(),  # Enhanced version
        # get_availability_insights_schema(),  # New insights function
    ]



# Export all schemas as a list
ALL_FUNCTION_SCHEMAS = get_all_function_schemas()