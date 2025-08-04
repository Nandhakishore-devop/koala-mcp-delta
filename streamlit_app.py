"""
Simple Streamlit chatbot application for resort booking system with OpenAI function calling.
Clean black background with white text interface.
"""
import os
import json
import streamlit as st
from typing import Dict, Any, List
from openai import OpenAI
from schemas import ALL_FUNCTION_SCHEMAS
from tools import call_tool
from dotenv import load_dotenv
from assistant_thread import AssistantThread
import time

# Load environment variables
load_dotenv()

# OpenAI pricing (as of 2024) - prices per 1K tokens
GPT4_TURBO_PROMPT_PRICE = 0.01  # $0.01 per 1K prompt tokens
GPT4_TURBO_COMPLETION_PRICE = 0.03  # $0.03 per 1K completion tokens

def calculate_cost(prompt_tokens: int, completion_tokens: int) -> float:
    """Calculate the cost of OpenAI API usage."""
    prompt_cost = (prompt_tokens / 1000) * GPT4_TURBO_PROMPT_PRICE
    completion_cost = (completion_tokens / 1000) * GPT4_TURBO_COMPLETION_PRICE
    return prompt_cost + completion_cost

# Page configuration
st.set_page_config(
    page_title="🏖️ koala_chat_bot_DM",
    page_icon="🏖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for black background and white text
st.markdown("""
<style>
    .main {
        background-color: #000000;
        color: #ffffff;
    }
    
    .stApp {
        background-color: #000000;
    }
    
    .main-header {
        background-color:black ;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        margin-top:-50px 
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: -10px;
        margin: 1rem 0;
        border-left: 4px solid #4ECDC4;
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .user-message {
        background-color: #2d2d2d;
        border-left-color: #FF6B6B;
    }
    
    .assistant-message {
        background-color: #1a1a1a;
        border-left-color: #4ECDC4;
    }
    
    .function-call {
        background-color: #2a2a1a;
        border-left-color: #ffc107;
        font-family: monospace;
        font-size: 0.9em;
        color: #ffffff;
        
    }
    
    .function-call pre {
        background-color: #0d0d0d;
        padding: 0.5rem;
        border-radius: 5px;
        white-space: pre-wrap;
        word-wrap: break-word;
        max-height: 300px;
        overflow-y: auto;
        color: #ffffff;
    }
    
    .function-call details {
        margin-top: 0.5rem;
    }
    
    .function-call summary {
        cursor: pointer;
        font-weight: bold;
        color: #28a745;
    }
    
    .stTextInput > div > div > input {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #4ECDC4;
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF6B6B;
        box-shadow: 0 0 0 2px rgba(255, 107, 107, 0.2);
    }
    
    .stTextInput label {
        color: #ffffff !important;
    }
    
    .stMarkdown {
        color: #ffffff;
    }
    
    .stSpinner > div {
        border-color: #4ECDC4;
    }
    
    .stError {
        background-color: #2d1a1a;
        color: #ff6b6b;
        border: 1px solid #ff6b6b;
    }
    
    div[data-testid="stSidebar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'thread' not in st.session_state:
    st.session_state.thread = AssistantThread()

if 'total_tokens' not in st.session_state:
    st.session_state.total_tokens = 0

if 'total_cost' not in st.session_state:
    st.session_state.total_cost = 0.0

if 'client' not in st.session_state:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        st.session_state.client = OpenAI(api_key=api_key)
    else:
        st.session_state.client = None

def process_function_call(function_call) -> str:
    """Process a function call from OpenAI and return the result."""
    function_name = function_call.name
    
    try:
        arguments = json.loads(function_call.arguments)
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid JSON arguments"})
    
    result = call_tool(function_name, **arguments)
    
    if isinstance(result, dict):
        return json.dumps(result, indent=2, default=str)
    else:
        return json.dumps({"result": result}, indent=2, default=str)

def display_message(message, is_user=True):
    """Display a chat message with appropriate styling."""
    if is_user:
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>🧑‍💻 You:</strong><br>
            {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 Resort Assistant:</strong><br>
            {message}
        </div>
        """, unsafe_allow_html=True)

def display_function_call(function_name, arguments, result=None):
    """Display function call information."""
    result_display = ""
    if result:
        if isinstance(result, str) and len(result) > 200:
            # Truncate long results but show they exist
            result_display = f'<br><strong>✅ Result:</strong> <details><summary>Function executed successfully (click to view result)</summary><pre>{result}</pre></details>'
        elif result:
            result_display = f'<br><strong>✅ Result:</strong> <pre>{result}</pre>'
        else:
            result_display = '<br><strong>✅ Result:</strong> Function executed successfully'
    
    st.markdown(f"""
    <div class="chat-message function-call">
        <strong>🔧 Function Call:</strong> {function_name}<br>
        <strong>Arguments:</strong> {arguments}
        {result_display}
    </div>
    """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏖️koala_chat_bot</h1>
        <p>Your AI-powered resort booking companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API key
    if not st.session_state.client:
        st.error("⚠️ OpenAI API key not found! Please set OPENAI_API_KEY environment variable.")
        return
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["type"] == "user":
            display_message(message["content"], is_user=True)
        elif message["type"] == "assistant":
            display_message(message["content"], is_user=False)
        elif message["type"] == "function_call":
            display_function_call(
                message["function_name"], 
                message["arguments"], 
                message.get("result")
            )
    
    # Initialize input value from session state
    if 'current_input' not in st.session_state:
        st.session_state.current_input = ""
    
    # Chat input at the bottom
    user_input = st.text_input(
        "Ask me anything about resort bookings:",
        value=st.session_state.current_input,
        key="chat_input",
        placeholder="Type your message here..."
    )
    
    # Process input when user presses Enter
    if user_input and user_input.strip() and user_input != st.session_state.get('last_processed_input', ''):
        # Store the input we're processing to avoid duplicate processing
        st.session_state.last_processed_input = user_input
        
        # Add user message to chat history
        st.session_state.messages.append({
            "type": "user",
            "content": user_input
        })
        
        # Add to thread
        st.session_state.thread.add_user_message(user_input)
        
        # Process with OpenAI
        with st.spinner("🤖 Processing your request..."):
            try:
                # First API call
                response = st.session_state.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.thread.get_history(),
                    tools=ALL_FUNCTION_SCHEMAS,
                    tool_choice="auto"
                )
                
                assistant_message = response.choices[0].message
                
                # Track tokens and cost
                if hasattr(response, 'usage') and response.usage:
                    st.session_state.total_tokens += response.usage.total_tokens
                    call_cost = calculate_cost(response.usage.prompt_tokens, response.usage.completion_tokens)
                    st.session_state.total_cost += call_cost
                
                # Add assistant message to thread
                st.session_state.thread.add_assistant_message({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": assistant_message.tool_calls
                })
                
                # Handle tool calls
                if assistant_message.tool_calls:
                    for tool_call in assistant_message.tool_calls:
                        function_name = tool_call.function.name
                        arguments = tool_call.function.arguments
                        
                        # Execute function
                        parsed_args = json.loads(arguments)
                        tool_result = call_tool(function_name, **parsed_args)
                        
                        # Convert result to JSON string
                        if isinstance(tool_result, dict):
                            tool_result_str = json.dumps(tool_result, indent=2, default=str)
                        else:
                            tool_result_str = json.dumps({"result": tool_result}, indent=2, default=str)
                        
                        # Add function call to chat history with actual result
                        st.session_state.messages.append({
                            "type": "function_call",
                            "function_name": function_name,
                            "arguments": arguments,
                            "result": tool_result_str
                        })
                        
                        # Add tool response to thread
                        st.session_state.thread.add_assistant_message({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_result_str
                        })
                    
                    # Get final response
                    final_response = st.session_state.client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=st.session_state.thread.get_history(),
                        tools=ALL_FUNCTION_SCHEMAS,
                        tool_choice="auto"
                    )
                    
                    final_message = final_response.choices[0].message
                    
                    # Track tokens for final response
                    if hasattr(final_response, 'usage') and final_response.usage:
                        st.session_state.total_tokens += final_response.usage.total_tokens
                        final_cost = calculate_cost(final_response.usage.prompt_tokens, final_response.usage.completion_tokens)
                        st.session_state.total_cost += final_cost
                    
                    # Add final assistant message
                    st.session_state.thread.add_assistant_message({
                        "role": "assistant",
                        "content": final_message.content
                    })
                    
                    # Add to chat history
                    if final_message.content:
                        st.session_state.messages.append({
                            "type": "assistant",
                            "content": final_message.content
                        })
                else:
                    # No function calls, just add the response
                    if assistant_message.content:
                        st.session_state.messages.append({
                            "type": "assistant",
                            "content": assistant_message.content
                        })
                
                # Clear the input for next message
                st.session_state.current_input = ""
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()