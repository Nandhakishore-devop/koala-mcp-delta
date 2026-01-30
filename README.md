Koala Chat Bot (Koala MCP Delta)

A sophisticated AI-powered chatbot designed for resort booking and vacation planning. This application leverages Streamlit for the user interface and OpenAI's GPT models with function calling (MCP tools) to provide real-time resort availability, listings, and detailed information.

Features

- Intelligent Assistant ("Myles AI"): A persona-driven AI that guides users through the booking process, from discovery to reservation.
- Resort Search & Discovery:
  - Search for resorts by name, location, or amenities.
  - View detailed listings including unit types, sleeping capacity, and prices.
  - "Book Now" and "Visit Resort" integration.
- Smart Formatting: Dynamically formats responses with emojis, lists, and tables for better readability.
- OpenAI Function Calling: seamless integration with backend tools to fetch real-time data (SQL/Database integration).
- Cost Tracking: Real-time display of token usage and estimated API costs.
- Modern UI: Custom-styled Streamlit interface with dark/light mode aesthetics.

Installation

1.  Clone the repository (if applicable).
2.  Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
Configuration

1.  Create a `.env` file in the root directory.
2.  Add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_api_key_here
    ```
  

 Usage

Run the Streamlit application:

```bash
streamlit run streamlit_app.py
```

The application will open in your default web browser (usually at `http://localhost:8501`).

Project Structure

- `streamlit_app.py`: The main application entry point. Handles the UI, chat loop, and session state.
- `assistant_thread.py`: Manages the AI assistant's persona, system prompts, and message history.
- `tools/`: Contains the tools available to the AI (Function Definitions).
  - `booking_tools.py`
  - `resort_tools.py`
  - `search_tools.py`
- `requirements.txt`: List of Python dependencies.

 System Prompt Highlights

The assistant is configured to:
- Act as a customer support agent for "Koala".
- Prioritize user conversion to booking.
- Handle fallback scenarios for unclear or out-of-scope queries.
- Use specific emojis and formatting styles based on the context (Resorts, Pricing, Amenities, etc.).
