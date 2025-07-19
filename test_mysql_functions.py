#!/usr/bin/env python3
"""
Test script to demonstrate MySQL-based resort booking functions.
"""
from dotenv import load_dotenv
from tools import call_tool
import json

# Load environment variables
load_dotenv()

def test_mysql_functions():
    """Test the MySQL-based functions with sample data."""
    
    print("🧪 Testing MySQL Resort Booking Functions")
    print("=" * 60)
    
    # Test cases for the new functions
    test_cases = [
        {
            "name": "Get User Bookings",
            "function": "get_user_bookings",
            "args": {"user_email": "test@example.com"},
            "description": "Fetch bookings for a user by email"
        },
        {
            "name": "Get Available Resorts",
            "function": "get_available_resorts",
            "args": {},
            "description": "List all available resorts"
        },
        {
            "name": "Get Available Resorts (USA)",
            "function": "get_available_resorts",
            "args": {"country": "USA"},
            "description": "List resorts in USA"
        },
        {
            "name": "Get Resort Details",
            "function": "get_resort_details",
            "args": {"resort_id": 1},
            "description": "Get details for resort ID 1"
        },
        {
            "name": "Search Available Listings",
            "function": "search_available_listings",
            "args": {},
            "description": "Search all available listings"
        },
        {
            "name": "Search Listings by Country",
            "function": "search_available_listings",
            "args": {"country": "USA"},
            "description": "Search listings in USA"
        },
        {
            "name": "Get User Profile",
            "function": "get_user_profile",
            "args": {"user_email": "test@example.com"},
            "description": "Get user profile information"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   📝 Description: {test_case['description']}")
        print(f"   🔧 Function: {test_case['function']}")
        print(f"   📋 Args: {test_case['args']}")
        print("-" * 50)
        
        try:
            result = call_tool(test_case['function'], **test_case['args'])
            if isinstance(result, dict) and "error" in result:
                print(f"   ⚠️  Result: {result['error']}")
            else:
                print(f"   ✅ Result: {json.dumps(result, indent=4)}")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        print("-" * 50)

def create_sample_openai_queries():
    """Create sample OpenAI queries for testing."""
    
    print("\n🤖 Sample OpenAI Queries for Testing")
    print("=" * 60)
    
    sample_queries = [
        "What bookings does user test@example.com have?",
        "Show me all available resorts",
        "List resorts in USA",
        "Tell me about resort ID 1",
        "Find available listings for 3 nights",
        "Search for listings in Thailand",
        "Get profile information for user test@example.com",
        "Show me resorts with active status",
        "Find listings available from 2024-12-01",
        "What unit types are available at resort ID 2?"
    ]
    
    print("\n📋 Example queries you can test with the OpenAI system:")
    for i, query in enumerate(sample_queries, 1):
        print(f"{i:2d}. {query}")
    
    print("\n" + "=" * 60)
    print("💡 These queries will automatically call the appropriate MySQL functions")
    print("   and return real-time data from your koala_live_laravel database!")

if __name__ == "__main__":
    test_mysql_functions()
    create_sample_openai_queries() 