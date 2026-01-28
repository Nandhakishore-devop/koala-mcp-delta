# Koala MCP Project - Full Workflow Guide

This document provides a comprehensive guide to understanding, running, and developing the Koala Resort Chatbot system.

---

## 1. System Architecture

The project follows a modular AI architecture:

-   **Frontend**: Streamlit Chatbot (`streamlit_app.py`)
-   **Backend Tools**: Centralized Python functions (`tools/` directory)
-   **MCP Server**: FastMCP server (`server.py`) for standard tool access.
-   **Database**: MySQL (`koala_dev`) with high-performance ORM (SQLAlchemy).
-   **Schema Engine**: Automatic reflection-based generation (`tools/schema_utils.py`).

---

## 2. Setup & Installation

### Prerequisites
- Python 3.10+
- MySQL Server installed and running.

### Environment Setup
1.  **Activate Virtual Environment**:
    ```powershell
    .\venv\Scripts\activate
    ```
2.  **Install Dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```
3.  **Configure Environment Variables**:
    Edit your `.env` file with your MySQL credentials:
    ```env
    MYSQL_HOST=localhost
    MYSQL_USER=root
    MYSQL_PASSWORD=your_password
    MYSQL_DATABASE=koala_dev
    OPENAI_API_KEY=your_key
    ```

---

## 3. Running the Application

To run the full system, you need TWO terminal windows open:

### Terminal 1: The Backend (MCP Server)
This manages the tool execution and database connection.
```powershell
python server.py
```
> [!TIP]
> Always check for the "✅ Database initialized successfully" message.

### Terminal 2: The UI (Streamlit Chatbot)
This is the interface you interact with.
```powershell
streamlit run streamlit_app.py
```

---

## 4. Development Workflow: Adding New Tools

The project uses **Automatic Schema Generation**. You NO LONGER need to manually edit JSON schemas.

### Step A: Write the logic
Add a function to `tools/resort_tools.py` (or a relevant file in `tools/`).
- **DO** use type hints (`str`, `int`, etc.).
- **DO** provide a clear docstring. The AI uses this to understand "Why" to use the tool.

```python
def get_resort_rating(resort_id: int) -> dict:
    """Get the average star rating for a specific resort."""
    # Your database logic here
    return {"rating": 4.8}
```

### Step B: Register the tool
Open [tools/__init__.py](file:///d:/DM/koala-mcp-delta/tools/__init__.py) and add the function to the `AVAILABLE_TOOLS` dictionary.

```python
AVAILABLE_TOOLS = {
    "get_resort_rating": get_resort_rating,  # Register here
}
```

### Step C: Verify
Restart both the server and chatbot. The AI will automatically detect the new tool and its parameters.

---

## 5. Maintenance & Troubleshooting

### Database Issues
- If you see "Connection failed," ensure the **MySQL80** service is started in Windows Services.
- **Service Command**: `Start-Service -Name MySQL80` (Run as Admin).

### Tool Call Errors
- If the AI says "Resort not found," it might be using a name that doesn't match exactly. I have implemented **Fuzzy Matching**, but for new tools, ensure your queries use the `.ilike()` operator in SQLAlchemy.

### Schema Conflicts
- If the AI is passing the wrong data types, check the **Type Hints** in your tool functions. Our schema generator uses these hints to tell the AI what to send.
