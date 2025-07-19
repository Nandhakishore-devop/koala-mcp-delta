#!/usr/bin/env python3
"""
Test script to verify OpenAI function calling is working correctly.
"""
from dotenv import load_dotenv
from main import chat_with_functions

# Load environment variables
load_dotenv()

def test_queries():
    """Test various queries to verify function calling works."""
    
    test_cases = [
        "What bookings does John Doe have?",
        "List all available resorts",
        "Tell me about Paradise Bay Resort",
        "Show me Jane Smith's bookings"
    ]
    
    print("🧪 Testing OpenAI Function Calling")
    print("=" * 50)
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {query}")
        print("-" * 40)
        
        try:
            response = chat_with_functions(query)
            print(f"✅ Response: {response}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("-" * 40)

if __name__ == "__main__":
    test_queries() 