"""
Auto-generated OpenAI function tool schemas.
Generated using schema_generator.py
"""
from typing import List, Dict, Any


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
                "resort_name": {
                    "type": "string",
                    "description": "The resort_name parameter"
                }
            },
            "required": [
                "resort_name"
            ],
            "additionalProperties": false
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
                "user_name": {
                    "type": "string",
                    "description": "The user_name parameter"
                }
            },
            "required": [
                "user_name"
            ],
            "additionalProperties": false
        }
    }
}


def list_available_resorts_schema() -> Dict[str, Any]:
    """Auto-generated schema for list_available_resorts function."""
    return {
    "type": "function",
    "function": {
        "name": "list_available_resorts",
        "description": "List all available resorts with their basic information",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": false
        }
    }
}


def get_all_function_schemas() -> List[Dict[str, Any]]:
    """Get all auto-generated OpenAI-compatible function schemas."""
    return [
        get_resort_details_schema(),
        get_user_bookings_schema(),
        list_available_resorts_schema(),
    ]

# Export all schemas as a list
ALL_FUNCTION_SCHEMAS = get_all_function_schemas()
