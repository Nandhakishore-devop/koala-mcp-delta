import streamlit as st
import json
import os
from datetime import datetime, date, timedelta
from typing import Dict, Any, List
import pandas as pd
from openai import OpenAI
from schemas import ALL_FUNCTION_SCHEMAS
from tools import call_tool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🏖️ Resort Booking System",
    page_icon="🏖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Kayak-like styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B35 0%, #F7931E 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .resort-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #FF6B35;
    }
    
    .price-tag {
        background: #FF6B35;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    
    .feature-badge {
        background: #f0f2f6;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        margin: 0.25rem;
        display: inline-block;
        font-size: 0.8rem;
    }
    
    .chat-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .user-message {
        background: #FF6B35;
        color: white;
        padding: 0.75rem;
        border-radius: 15px 15px 5px 15px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
    }
    
    .assistant-message {
        background: white;
        color: #333;
        padding: 0.75rem;
        border-radius: 15px 15px 15px 5px;
        margin: 0.5rem 0;
        max-width: 80%;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"))

client = get_openai_client()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'user_bookings' not in st.session_state:
    st.session_state.user_bookings = []

def process_ai_query(query: str) -> str:
    """Process user query using OpenAI function calling"""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful resort booking assistant. Use available functions to fetch data "
                "and provide clear, formatted responses. Always be friendly and helpful."
            )
        },
        {
            "role": "user",
            "content": query
        }
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            tools=ALL_FUNCTION_SCHEMAS,
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        
        # Handle function calls if any
        if assistant_message.tool_calls:
            messages.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": assistant_message.tool_calls
            })
            
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                # Call the tool function
                result = call_tool(function_name, **arguments)
                result_str = json.dumps(result, indent=2, default=str)
                
                messages.append({
                    "role": "tool",
                    "content": result_str,
                    "tool_call_id": tool_call.id
                })
            
            # Get final response
            final_response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                tools=ALL_FUNCTION_SCHEMAS,
                tool_choice="auto"
            )
            
            return final_response.choices[0].message.content or "Sorry, I couldn't process your request."
        
        return assistant_message.content or "Sorry, I couldn't process your request."
        
    except Exception as e:
        return f"Error processing request: {str(e)}"

def display_resort_card(resort: Dict[str, Any]):
    """Display a resort in a card format"""
    with st.container():
        # Handle both dict and other formats
        if not isinstance(resort, dict):
            st.warning("Invalid resort data format")
            return
            
        st.markdown(f"""
        <div class="resort-card">
            <h3>🏨 {resort.get('name', 'Unknown Resort')}</h3>
            <p><strong>📍 Location:</strong> {resort.get('location', 'N/A')}</p>
            <p><strong>⭐ Rating:</strong> {resort.get('rating', 'N/A')}/5</p>
            <p><strong>💰 Price:</strong> <span class="price-tag">${resort.get('price_per_night', 'N/A')}/night</span></p>
            <p><strong>🏊 Amenities:</strong></p>
            <div>
        """, unsafe_allow_html=True)
        
        amenities = resort.get('amenities', [])
        if amenities and isinstance(amenities, list):
            for amenity in amenities:
                st.markdown(f'<span class="feature-badge">{amenity}</span>', unsafe_allow_html=True)
        elif amenities:
            st.markdown(f'<span class="feature-badge">{str(amenities)}</span>', unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"View Details", key=f"details_{resort.get('name', 'unknown')}"):
                st.session_state.selected_resort = resort.get('name')
        with col2:
            if st.button(f"Book Now", key=f"book_{resort.get('name', 'unknown')}"):
                st.session_state.booking_resort = resort.get('name')
        with col3:
            if st.button(f"Add to Favorites", key=f"fav_{resort.get('name', 'unknown')}"):
                st.success("Added to favorites! ❤️")

# Header
st.markdown("""
<div class="main-header">
    <h1>🏖️ Resort Booking System</h1>
    <p>Find your perfect getaway with AI-powered search</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for filters and user info
with st.sidebar:
    st.header("🔍 Search Filters")
    
    # User information
    st.subheader("👤 User Information")
    user_name = st.text_input("Your Name", value="John Doe")
    
    # Date selection
    st.subheader("📅 Travel Dates")
    check_in = st.date_input("Check-in Date", value=date.today() + timedelta(days=7))
    check_out = st.date_input("Check-out Date", value=date.today() + timedelta(days=10))
    
    # Guests
    st.subheader("👥 Guests")
    adults = st.number_input("Adults", min_value=1, max_value=10, value=2)
    children = st.number_input("Children", min_value=0, max_value=10, value=0)
    
    # Budget
    st.subheader("💰 Budget")
    budget_range = st.slider("Price per night ($)", 50, 1000, (100, 500))
    
    # User bookings
    st.subheader("📋 Your Bookings")
    if st.button("🔄 Refresh Bookings"):
        try:
            bookings_data = call_tool("get_user_bookings", user_name=user_name)
            
            # Handle different return types
            if isinstance(bookings_data, dict):
                st.session_state.user_bookings = bookings_data.get('bookings', [])
            elif isinstance(bookings_data, list):
                st.session_state.user_bookings = bookings_data
            else:
                st.session_state.user_bookings = []
                
        except Exception as e:
            st.error(f"Could not fetch bookings: {str(e)}")
    
    if st.session_state.user_bookings:
        for booking in st.session_state.user_bookings:
            st.info(f"🏨 {booking.get('resort', 'N/A')}\n📅 {booking.get('dates', 'N/A')}")

# Main content area
main_tab1, main_tab2, main_tab3 = st.tabs(["🔍 Search Resorts", "💬 AI Assistant", "📊 My Dashboard"])

with main_tab1:
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🌴 Where would you like to go?", 
                                   placeholder="e.g., Beach resort in Maldives, Mountain cabin, etc.")
    with col2:
        search_button = st.button("🚀 Search Resorts", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick search buttons
    st.subheader("🚀 Quick Searches")
    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
    with quick_col1:
        if st.button("🏖️ Beach Resorts"):
            search_query = "beach resorts"
            search_button = True
    with quick_col2:
        if st.button("🏔️ Mountain Retreats"):
            search_query = "mountain retreats"
            search_button = True
    with quick_col3:
        if st.button("🏙️ City Hotels"):
            search_query = "city hotels"
            search_button = True
    with quick_col4:
        if st.button("🌟 All Resorts"):
            search_query = "show all available resorts"
            search_button = True
    
    # Search results
    if search_button or search_query:
        if search_query:
            with st.spinner("🔍 Searching for the perfect resorts..."):
                try:
                    # Get available resorts
                    resorts_data = call_tool("get_available_resorts")
                    
                    # Handle different return types from call_tool
                    if isinstance(resorts_data, dict):
                        resorts = resorts_data.get('resorts', [])
                    elif isinstance(resorts_data, list):
                        resorts = resorts_data
                    else:
                        resorts = []
                    
                    if resorts:
                        st.success(f"Found {len(resorts)} resort(s)!")
                        
                        # Filter by budget if applicable
                        filtered_resorts = []
                        for resort in resorts:
                            # Handle both dict and direct value access
                            if isinstance(resort, dict):
                                price = resort.get('price_per_night', 0)
                            else:
                                price = 0
                                
                            if isinstance(price, (int, float)) and budget_range[0] <= price <= budget_range[1]:
                                filtered_resorts.append(resort)
                        
                        if not filtered_resorts:
                            filtered_resorts = resorts  # Show all if none match budget
                        
                        st.session_state.search_results = filtered_resorts
                        
                        # Display results
                        for resort in filtered_resorts:
                            display_resort_card(resort)
                    else:
                        st.warning("No resorts found. Try a different search!")
                        
                except Exception as e:
                    st.error(f"Search error: {str(e)}")
                    st.write("Debug info:", str(type(resorts_data)), str(resorts_data)[:200] if resorts_data else "No data")

with main_tab2:
    st.subheader("🤖 AI Travel Assistant")
    st.write("Ask me anything about resorts, bookings, or travel recommendations!")
    
    # Chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">{message["content"]}</div>', 
                           unsafe_allow_html=True)
    
    # Chat input
    user_question = st.text_input("💬 Ask me anything...", 
                                placeholder="e.g., What resorts do you recommend for families?",
                                key="chat_input")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        send_button = st.button("📤 Send")
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    if send_button and user_question:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_question})
        
        # Get AI response
        with st.spinner("🤔 Thinking..."):
            ai_response = process_ai_query(user_question)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        st.rerun()

with main_tab3:
    st.subheader("📊 Your Travel Dashboard")
    
    dashboard_col1, dashboard_col2 = st.columns(2)
    
    with dashboard_col1:
        st.subheader("📈 Booking Statistics")
        if st.session_state.user_bookings:
            booking_df = pd.DataFrame(st.session_state.user_bookings)
            st.dataframe(booking_df, use_container_width=True)
        else:
            st.info("No bookings found. Make your first booking today!")
    
    with dashboard_col2:
        st.subheader("❤️ Favorites & Preferences")
        st.info("Feature coming soon!")
        
        st.subheader("🎯 Recommendations")
        if st.button("Get Personalized Recommendations"):
            with st.spinner("Analyzing your preferences..."):
                recommendation_query = f"Give me personalized resort recommendations for {user_name} based on their booking history"
                recommendations = process_ai_query(recommendation_query)
                st.success("Here are your personalized recommendations:")
                st.markdown(recommendations)

# Footer
st.markdown("---")
st.markdown("🏖️ **Resort Booking System** - Powered by AI | Made with ❤️ using Streamlit")

# Handle booking flow
if 'booking_resort' in st.session_state and st.session_state.booking_resort:
    with st.expander("🎯 Complete Your Booking", expanded=True):
        st.success(f"Great choice! You're booking: **{st.session_state.booking_resort}**")
        
        booking_col1, booking_col2 = st.columns(2)
        with booking_col1:
            st.write(f"📅 **Check-in:** {check_in}")
            st.write(f"📅 **Check-out:** {check_out}")
        with booking_col2:
            st.write(f"👥 **Guests:** {adults} adults, {children} children")
            st.write(f"💰 **Budget:** ${budget_range[0]} - ${budget_range[1]} per night")
        
        if st.button("✅ Confirm Booking"):
            # Here you would integrate with your booking function
            st.success("🎉 Booking confirmed! Check your email for details.")
            del st.session_state.booking_resort