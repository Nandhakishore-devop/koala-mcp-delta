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
import base64

# Load environment variables
load_dotenv()

# OpenAI pricing (as of 2024) - prices per 1K tokens
GPT4_TURBO_PROMPT_PRICE = 0.0015  # $0.0015 per 1K prompt tokens 3.5
GPT4_TURBO_COMPLETION_PRICE = 0.002  # $0.002 per 1K completion tokens 3.5

def calculate_cost(prompt_tokens: int, completion_tokens: int) -> float:
    """Calculate the cost of OpenAI API usage."""
    prompt_cost = (prompt_tokens / 1000) * GPT4_TURBO_PROMPT_PRICE
    completion_cost = (completion_tokens / 1000) * GPT4_TURBO_COMPLETION_PRICE
    return prompt_cost + completion_cost

def display_cost_info():
    """Display cost information in a fixed position on the right side."""
    st.markdown(f"""
    <div style="
        position: fixed;
        top: 100px;
        right: 20px;
        background-color: #2d2d2d;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4ECDC4;
        z-index: 1000;
        min-width: 200px;
        color: #ffffff;
        font-size: 0.9em;
    ">
        <h4 style="margin: 0 0 0.5rem 0; color: #4ECDC4;">💰 Usage Stats</h4>
        <div style="margin: 0.3rem 0;">
            <strong>Tokens:</strong> {st.session_state.total_tokens:,}
        </div>
        <div style="margin: 0.3rem 0;">
            <strong>Cost:</strong> ${st.session_state.total_cost:.4f}
        </div>
        <div style="margin: 0.3rem 0;">
            <strong>Messages:</strong> {len([m for m in st.session_state.messages if m['type'] == 'user'])}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="🏖️ koala_chat_bot_DM",
    page_icon="🏖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for black background and white text
import streamlit as st

st.markdown(
    """
    <link rel="stylesheet" href="https://use.typekit.net/huc7jof.css">
    <style>
        .main {
            background-color: #000000;
            color: #ffffff;
            font-family: proxima-nova, sans-serif;
        }

        .stApp {
            background-color: #F8F7F6;
            font-family: proxima-nova, sans-serif;
        }

        .main-header {
            background-color: transparent;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
            margin-top: -80px;
        }

        .chat-message {
            padding: 1rem;
            border-radius: 20px; /* ✅ fixed */
            margin: 1rem 0; 
            border-left: 4px solid #4ECDC4;
            background-color: green;
            color: #ffffff;
            font-family: proxima-nova, sans-serif;
        }

        .user-message {
            background-color: white;
            border-left: 4px solid #FF6B6B;
            margin-top: 10px;
            margin-left: 150px;
            color: black;
            border: 1px solid #e8e8e8;
            border-radius: 24px;
            border-bottom-right-radius: 3px;
            font-family: proxima-nova, sans-serif;
            display:inline-flex;
            align-items: flex-start;
            flex-direction: row-reverse;
            justify-content: end;
            gap: 20px;
            padding-left: 20px;
            max-width:90%;
            float:right;
            font-size:17px;
            line-height:24px;
            
        }
        .user-message strong{
            flex: 0 0 40px;
            max-width: 40px;
        }

        

        .assistant-message {
            background-color: transparent;
            border:0;
            color: black;
            border-radius: 0px;
            padding: 10px;
            font-family: proxima-nova, sans-serif;
        }

        .function-call {
            background-color: white;
            border-left: 4px solid #ffc107;
            font-family: monospace;
            font-size: 0.8em;
            color: black;
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
            margin-top: 0.3rem;
        }

        .function-call summary {
            cursor: pointer;
            font-weight: bold;
            color: #28a745;
        }

        .stTextArea > div > div > textarea {
            color: #000;
            font-size:17px;
            resize:none;
            max-width: 650px;
        }
    

        .stTextArea > div {
           width: 720px;
            height: 100px;
            position: fixed;
            left: 0;
            right: 0;
            bottom: 40px;
            margin: 0 auto;
            background: #fff;
            border-color: transparent;
            overflow: visible;
            box-shadow: none;
            background: transparent;   
        }

        .stTextArea > div > div  {
            background: #fff;
            box-shadow: 0 0 20px rgba(0, 0, 0, .05);
            border-radius: 20px;
            border: 1px solid #e8e8e8;
        }

        .stTextArea > div::after {
            content: "";
            width: 100%;
            background: #F8F7F6;
            left: 0;
            right: 0;
            boo: 0;
            bottom: -42px;
            position: absolute;
            height: 42px;
            z-index: 17;
        }
  
        .stFormSubmitButton {
            position: fixed;
            bottom: 63px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            left: 0;
            margin: 0 auto;
            right: -620px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 0;
            background-color: #FFF;
        }
        
        .stFormSubmitButton:focus, .stFormSubmitButton:hover {
            border: 0;
            box-shadow: inherit;
        }

        .stFormSubmitButton button{
            width: 50px;
            height: 50px;
            text-indent: -9999px;
            background-color: #FFF;
            background-image: url("https://koalaadmin-prod.s3.us-east-2.amazonaws.com/images/send-black.svg");
            background-repeat: no-repeat;
            background-size: 49px;
            border-radius: 50%;
        }
        .stFormSubmitButton button:hover, .stFormSubmitButton button:focus(:active), .st-emotion-cache-z8vbw2:hover{
            border-color: transparent;
        }

        .stFormSubmitButton button:hover{
            border:0;
        }

      

        .chat-message.assistant-message img{ 
            border-radius: 10px; margin: 20px 0 10px;
        }

        .chat-message.assistant-message a{ 
             color: #0B6E4F;
        }

        .stTextInput > div > div > input:focus {
            border-color: red;
            outline: none;
        }

        .stTextArea textarea::placeholder {
            color: gray;
            opacity: 8;
        }

        textarea::placeholder {
           color: #888888;
           opacity: 1;
        }
        textarea:-ms-input-placeholder { 
           color: #888888;
        }
        textarea::-ms-input-placeholder { 
           color: #888888;
        }


        .chat-textarea::placeholder {
           font-size: 28px;
        
        }


        .chat-message * {
           font-size: 18px;
        }

        .stTextInput label {
            color: #ffffff !important;
        }

        .stMarkdown {
            color: #ffffff;
            font-family: proxima-nova, sans-serif;
        }

        .stSpinner > div {
            border-color: blue !important; /* ✅ force blue spinner */
        }

        .stError {
            background-color: #2d1a1a;
            color: #ff6b6b;
            border: 1px solid #ff6b6b;
        }

        div[data-testid="stSidebar"] {
            display: none;
        }

        .stAppHeader {
            display: none;
        }

       
        .assistant-message{ 
           background-color: transparent; 
         }

        .st-bx{
            caret-color:black;       
        } 

        .st-emotion-cache-z8vbw2:hover {
            border-color: gray;
            color: gray;
        }
        
    </style>
    """,
    unsafe_allow_html=True
)

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

def handle_simple_greetings(user_input: str) -> str:
    """Handle simple greetings and common phrases without calling LLM."""
    user_input_lower = user_input.lower().strip()
    
    # Define greeting patterns and responses
    greeting_responses = {
        # Basic greetings
        
        'hey': "Hey! 😊 Ready to plan your next vacation? I'm here to help you find amazing resorts!",
        'good morning': "Good morning! ☀️ What a beautiful day to plan a resort getaway! How can I assist you?",
        'good afternoon': "Good afternoon! 🌅 Hope you're having a great day! Let's find you an amazing resort experience.",
        'good evening': "Good evening! 🌙 Perfect time to plan your next vacation! What can I help you with?",
        
        # # Thank you responses
        # 'thank you': "You're very welcome! 😊 Is there anything else I can help you with for your resort booking?",
        # 'thanks': "My pleasure! 🌟 Feel free to ask if you need help with anything else!",
        # 'thank u': "You're welcome! 💫 Happy to help with your resort needs anytime!",
        
        
        # # Other common phrases
        # 'how are you': "I'm doing great, thank you for asking! 🤖 I'm here and ready to help you find the perfect resort. How are you doing?",
        # 'what\'s up': "Not much, just here to help you plan an amazing vacation! 🏝️ What resort experience are you looking for?",
        # 'whats up': "Just ready to help you book your dream resort! ✨ What destination interests you?",
        
        # 'okay': "Perfect! 🌴 How can I help you with your resort booking today?",
        # 'bye': "Goodbye! 👋 Thanks for using our resort booking service. Have a wonderful day!",
        # 'goodbye': "Farewell! 🌊 Hope to help you plan your next amazing vacation soon!",
        # 'see you': "See you later! 🏖️ Don't hesitate to come back when you're ready to book that perfect resort!",
        
    }
    
    # Check for exact matches first
    if user_input_lower in greeting_responses:
        return greeting_responses[user_input_lower]
    
    # Check for partial matches
    for greeting, response in greeting_responses.items():
        if greeting in user_input_lower:
            return response
    
    # Return None if no greeting pattern matches
    return None
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
            <strong>
            <img width="40" height="40" src="https://koalaadmin-prod.s3.us-east-2.amazonaws.com/static/assets/img/availablity-koala-icon.svg" />
            </strong>
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
    # Display cost information in sidebar
    display_cost_info()
    
    # Header
    st.markdown(
        """
        <div class="main-header" style="text-align:center;">
            <img src="https://koalaadmin-prod.s3.us-east-2.amazonaws.com/static/assets/img/Koala-Home-hero-logo.svg" 
                alt="Header Image" width="200">
        </div>
        """,
        unsafe_allow_html=True
    )
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

    

    if 'schema_limit_counter' not in st.session_state:
        st.session_state.schema_limit_counter = 0

    if 'thread' not in st.session_state:
        st.session_state.thread = Thread()

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'input_counter' not in st.session_state:
        st.session_state.input_counter = 0


    # # --- Hide all form submit buttons ---
    # hide_submit_css = """
    # <style>
    # form > div.stButton > button {
    #     display: none;
    #     c
    # }

    # .stForm button{
    #     display: none;
        
    # }
    # .stForm{
    #     border: none;
    #     margin-top :-200 px;

    # }
    # </style>
    # """
    # st.markdown(hide_submit_css, unsafe_allow_html=True)






    st.markdown(
        """
        <style>
        /* Target only our custom chat input */
        div[data-testid="stTextInput"] input {
            background-image: url("https://koalaadmin-prod.s3.us-east-2.amazonaws.com/images/send-black.svg");
            background-repeat: no-repeat;
            background-position: 10px center;  /* left padding */
            background-size: 40px;        /* resize image */
            padding-right: 40px;  
            background-position: 97% 28px;
                          /* leave space for the image */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Chat input at the bottom with Submit button
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "I can guide you with resort options and availability to make your vacation planning easier:",
            placeholder="Type your message here..."
            
        )
        submit_button = st.form_submit_button("Submit")
        


    # # Chat input at the bottom with Submit button
    # with st.form(key=f"chat_form_{st.session_state.input_counter}", clear_on_submit=True):
    #     user_input = st.text_input(
    #         "I can guide you with resort options and availability to make your vacation planning easier:",
    #         placeholder="Type your message here..."
    #     )
    #     submit_button = st.form_submit_button("Submit")

    # ✅ Process input only when button is clicked AND text is not empty
    if submit_button:
        if user_input and user_input.strip() and user_input != st.session_state.get('last_processed_input', ''):
            # Store the input we're processing to avoid duplicate processing
            st.session_state.last_processed_input = user_input

            # Add user message to chat history
            st.session_state.messages.append({
                "type": "user",
                "content": user_input
            }) 

        else:
            st.warning("⚠️ Please type a question before submitting.")



        
        # Check if this is a simple greeting first
        greeting_response = handle_simple_greetings(user_input)
        
        if greeting_response:
            # Handle greeting locally without LLM call
            st.session_state.messages.append({
                "type": "assistant",
                "content": greeting_response
            })
            
            # Clear the input for next message by incrementing counter
            st.session_state.input_counter += 1
            st.rerun()
            return
        
        # Add to thread for LLM processing
        st.session_state.thread.add_user_message(user_input)
        
        # Process with OpenAI
        with st.spinner("🐨 Thinking..."):
            try:
                # Decide whether to include schemas
                include_schema = st.session_state.schema_limit_counter < 2

                # Get message history
                history = st.session_state.thread.get_history()

                if include_schema:
                    messages_to_send = history
                    tools_to_send = ALL_FUNCTION_SCHEMAS
                    st.session_state.schema_limit_counter += 1
                else:
                    schema_messages = history[:3]
                    recent_messages = history[-6:]  # Last 3 user-assistant pairs
                    messages_to_send = schema_messages + recent_messages
                    tools_to_send = []

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

                    # Use same schema rule for final response (don’t include after limit)
                    if st.session_state.schema_limit_counter < 2:
                        final_messages_to_send = st.session_state.thread.get_history()
                        final_tools_to_send = ALL_FUNCTION_SCHEMAS
                    else:
                        schema_messages = st.session_state.thread.get_history()[:3]
                        recent_messages = st.session_state.thread.get_history()[-6:]
                        final_messages_to_send = schema_messages + recent_messages
                        final_tools_to_send = []
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
                
                # Clear the input for next message by incrementing counter
                st.session_state.input_counter += 1
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()





# def main():
#     # Display cost information in sidebar
#     display_cost_info()
#     st.markdown(
#         """
#         <div class="main-header" style="text-align:center;">
#             <img src="https://koalaadmin-prod.s3.us-east-2.amazonaws.com/static/assets/img/Koala-Home-hero-logo.svg" 
#                 alt="Header Image" width="200">
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
#     # Check API key
#     if not st.session_state.client:
#         st.error("⚠️ OpenAI API key not found! Please set OPENAI_API_KEY environment variable.")
#         return
    
#     # Display chat messages
#     for message in st.session_state.messages:
#         if message["type"] == "user":
#             display_message(message["content"], is_user=True)
#         elif message["type"] == "assistant":
#             display_message(message["content"], is_user=False)
#         elif message["type"] == "function_call":
#             display_function_call(
#                 message["function_name"], 
#                 message["arguments"], 
#                 message.get("result")
#             )

    

#     if 'schema_limit_counter' not in st.session_state:
#         st.session_state.schema_limit_counter = 0

#     if 'thread' not in st.session_state:
#         st.session_state.thread = Thread()

#     if 'chat_history' not in st.session_state:
#         st.session_state.chat_history = []

#     if 'input_counter' not in st.session_state:
#         st.session_state.input_counter = 0

#     # ... continue your app logic

    
#     # Chat input at the bottom
#     user_input = st.chat_input(
#         "I can guide you with resort options and availability to make your vacation planning easier:",
#         # value="",
#         key=f"chat_input_{st.session_state.input_counter}",
#         # placeholder="Type your message here..."
#     )

    
    
#     # Process input when user presses Enter
#     if user_input and user_input.strip() and user_input != st.session_state.get('last_processed_input', ''):
#         # Store the input we're processing to avoid duplicate processing
#         st.session_state.last_processed_input = user_input
        
#         # Add user message to chat history
#         st.session_state.messages.append({
#             "type": "user",
#             "content": user_input
#         })
        
#         # Check if this is a simple greeting first
#         greeting_response = handle_simple_greetings(user_input)
        
#         if greeting_response:
#             # Handle greeting locally without LLM call
#             st.session_state.messages.append({
#                 "type": "assistant",
#                 "content": greeting_response
#             })
            
#             # Clear the input for next message by incrementing counter
#             st.session_state.input_counter += 1
#             st.rerun()
#             return
        
#         # Add to thread for LLM processing
#         st.session_state.thread.add_user_message(user_input)
        
#         # Process with OpenAI
#         with st.spinner("🐨 Thinking..."):
#             try:
#                 # Decide whether to include schemas
#                 include_schema = st.session_state.schema_limit_counter < 2

#                 # Get message history
#                 history = st.session_state.thread.get_history()

#                 if include_schema:
#                     messages_to_send = history
#                     tools_to_send = ALL_FUNCTION_SCHEMAS
#                     st.session_state.schema_limit_counter += 1
#                 else:
#                     schema_messages = history[:3]
#                     recent_messages = history[-6:]  # Last 3 user-assistant pairs
#                     messages_to_send = schema_messages + recent_messages
#                     tools_to_send = []

#                 # First API call
#                 response = st.session_state.client.chat.completions.create(
#                     model="gpt-3.5-turbo",
#                     messages=st.session_state.thread.get_history(),
#                     tools=ALL_FUNCTION_SCHEMAS,
#                     tool_choice="auto"
#                 )
                
#                 assistant_message = response.choices[0].message
                
#                 # Track tokens and cost
#                 if hasattr(response, 'usage') and response.usage:
#                     st.session_state.total_tokens += response.usage.total_tokens
#                     call_cost = calculate_cost(response.usage.prompt_tokens, response.usage.completion_tokens)
#                     st.session_state.total_cost += call_cost
                
#                 # Add assistant message to thread
#                 st.session_state.thread.add_assistant_message({
#                     "role": "assistant",
#                     "content": assistant_message.content,
#                     "tool_calls": assistant_message.tool_calls
#                 })
                
#                 # Handle tool calls
#                 if assistant_message.tool_calls:
#                     for tool_call in assistant_message.tool_calls:
#                         function_name = tool_call.function.name
#                         arguments = tool_call.function.arguments
                        
#                         # Execute function
#                         parsed_args = json.loads(arguments)
#                         tool_result = call_tool(function_name, **parsed_args)
                        
#                         # Convert result to JSON string
#                         if isinstance(tool_result, dict):
#                             tool_result_str = json.dumps(tool_result, indent=2, default=str)
#                         else:
#                             tool_result_str = json.dumps({"result": tool_result}, indent=2, default=str)
                        
#                         # Add function call to chat history with actual result
#                         st.session_state.messages.append({
#                             "type": "function_call",
#                             "function_name": function_name,
#                             "arguments": arguments,
#                             "result": tool_result_str
#                         })
                        
#                         # Add tool response to thread
#                         st.session_state.thread.add_assistant_message({
#                             "role": "tool",
#                             "tool_call_id": tool_call.id,
#                             "content": tool_result_str
#                         })

#                     # Use same schema rule for final response (don’t include after limit)
#                     if st.session_state.schema_limit_counter < 2:
#                         final_messages_to_send = st.session_state.thread.get_history()
#                         final_tools_to_send = ALL_FUNCTION_SCHEMAS
#                     else:
#                         schema_messages = st.session_state.thread.get_history()[:3]
#                         recent_messages = st.session_state.thread.get_history()[-6:]
#                         final_messages_to_send = schema_messages + recent_messages
#                         final_tools_to_send = []
#                     # Get final response
#                     final_response = st.session_state.client.chat.completions.create(
#                         model="gpt-3.5-turbo",
#                         messages=st.session_state.thread.get_history(),
#                         tools=ALL_FUNCTION_SCHEMAS,
#                         tool_choice="auto"
#                     )
                    
#                     final_message = final_response.choices[0].message
                    
#                     # Track tokens for final response
#                     if hasattr(final_response, 'usage') and final_response.usage:
#                         st.session_state.total_tokens += final_response.usage.total_tokens
#                         final_cost = calculate_cost(final_response.usage.prompt_tokens, final_response.usage.completion_tokens)
#                         st.session_state.total_cost += final_cost
                    
#                     # Add final assistant message
#                     st.session_state.thread.add_assistant_message({
#                         "role": "assistant",
#                         "content": final_message.content
#                     })
                    
#                     # Add to chat history
#                     if final_message.content:
#                         st.session_state.messages.append({
#                             "type": "assistant",
#                             "content": final_message.content
#                         })
#                 else:
#                     # No function calls, just add the response
#                     if assistant_message.content:
#                         st.session_state.messages.append({
#                             "type": "assistant",
#                             "content": assistant_message.content
#                         })
                
#                 # Clear the input for next message by incrementing counter
#                 st.session_state.input_counter += 1
#                 st.rerun()
                
#             except Exception as e:
#                 st.error(f"❌ Error: {str(e)}")

# if __name__ == "__main__":
#     main()
