# 🏖️ Resort Booking System with OpenAI Function Calling

A comprehensive example of using OpenAI's function calling feature with a resort booking system, featuring SQLAlchemy database integration and automatic schema generation.

## 🏗️ Project Structure

```
MCP/
├── venv/                    # Virtual environment
├── requirements.txt         # Python dependencies
├── schemas.py              # OpenAI function schemas (manual)
├── tools.py                # Tool functions with SQLAlchemy
├── main.py                 # Main application with OpenAI integration
├── schema_generator.py     # Automatic schema generation utility
├── resort_bookings.db      # SQLite database (auto-created)
└── README.md               # This file
```

## 🚀 Features

### 1. **OpenAI Function Tool Schemas**
- ✅ Manual schema creation in OpenAI format
- ✅ Automatic schema generation from function signatures
- ✅ Type-safe parameter definitions
- ✅ Proper JSON schema format

### 2. **Database Integration**
- ✅ SQLAlchemy ORM with SQLite
- ✅ Proper database models (Users, Resorts, Bookings)
- ✅ Automatic database initialization with sample data
- ✅ Relationship handling and joins

### 3. **Function Tools**
- ✅ `get_user_bookings(user_name)` - Fetch user bookings
- ✅ `get_available_resorts()` - List all resorts
- ✅ `get_resort_details(resort_name)` - Get resort details

### 4. **OpenAI Integration**
- ✅ Complete chat interface with function calling
- ✅ Proper function call routing
- ✅ Error handling and validation
- ✅ Multi-turn conversations

## 📋 Requirements

- Python 3.7+
- OpenAI API key (optional for demo mode)
- Virtual environment (recommended)

## 🛠️ Installation

1. **Clone and setup:**
```bash
cd MCP
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Set OpenAI API key (optional):**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 🎯 Usage

### Basic Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run the main application
python main.py
```

### Demo Mode (without OpenAI API)

If you don't have an OpenAI API key, the system will run in demo mode:

```bash
python main.py
```

This will show:
- Available function schemas
- Direct tool testing
- Database functionality

### Test Individual Components

```bash
# Test database and tools directly
python tools.py

# Generate schemas automatically
python schema_generator.py

# Test specific functions
python -c "from tools import get_user_bookings; print(get_user_bookings('John Doe'))"
```

## 🔧 Function Schemas

### Manual Schema (schemas.py)
```python
from schemas import ALL_FUNCTION_SCHEMAS

# Use in OpenAI API call
response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[{"role": "user", "content": "What bookings does John Doe have?"}],
    tools=ALL_FUNCTION_SCHEMAS,
    tool_choice="auto"
)
```

### Automatic Schema Generation
```python
from schema_generator import generate_function_schema

# Auto-generate schema from function signature
schema = generate_function_schema(get_user_bookings, "Fetch all bookings for a user by name")
```

## 📊 Database Schema

### Tables
- **users**: id, name, email
- **resorts**: id, name, location, price_per_night, description
- **bookings**: id, user_id, resort_id, checkin, checkout, created_at

### Sample Data
- 3 users (John Doe, Jane Smith, Alice Johnson)
- 3 resorts (Paradise Bay, Mountain View Lodge, Tropical Sunset)
- 3 bookings with different combinations

## 🎮 Example Queries

Try these queries in the chat interface:

1. **"What bookings does John Doe have?"**
   - Calls `get_user_bookings("John Doe")`
   - Returns list of bookings with resort, checkin, checkout

2. **"List all available resorts"**
   - Calls `get_available_resorts()`
   - Returns all resorts with details

3. **"Tell me about Paradise Bay Resort"**
   - Calls `get_resort_details("Paradise Bay Resort")`
   - Returns detailed resort information

4. **"What are the cheapest resorts?"**
   - Calls `get_available_resorts()`
   - AI processes and compares prices

## 🔍 Function Details

### get_user_bookings(user_name: str) → List[Dict[str, str]]
```python
# Example usage
bookings = get_user_bookings("John Doe")
# Returns: [{"resort": "Paradise Bay Resort", "checkin": "2024-03-15", "checkout": "2024-03-20"}]
```

### get_available_resorts() → List[Dict[str, Any]]
```python
# Example usage
resorts = get_available_resorts()
# Returns: [{"name": "Paradise Bay Resort", "location": "Maldives", "price_per_night": "$450.00", ...}]
```

### get_resort_details(resort_name: str) → Dict[str, Any]
```python
# Example usage
details = get_resort_details("Paradise Bay Resort")
# Returns: {"name": "Paradise Bay Resort", "location": "Maldives", "total_bookings": 1, ...}
```

## 🧪 Testing

### Test Database Functions
```bash
python -c "
from tools import *
print('Users:', get_user_bookings('John Doe'))
print('Resorts:', get_available_resorts())
print('Details:', get_resort_details('Paradise Bay Resort'))
"
```

### Test Schema Generation
```bash
python schema_generator.py
```

### Test OpenAI Integration
```bash
# Make sure OPENAI_API_KEY is set
python main.py
```

# .env

# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=""
MYSQL_DATABASE=koala_dev

# OpenAI API Configuration
OPENAI_API_KEY=REDACTED_SK_PROJ




## 📈 Advanced Features

### Automatic Schema Generation
The `schema_generator.py` utility can automatically create OpenAI function schemas from Python function signatures:

```python
from schema_generator import generate_function_schema

def my_function(name: str, age: int) -> Dict[str, Any]:
    """Get user information."""
    return {"name": name, "age": age}

schema = generate_function_schema(my_function)
# Automatically generates proper OpenAI function schema
```

### Custom Function Descriptions
```python
descriptions = {
    "get_user_bookings": "Fetch all bookings for a user by name",
    "get_available_resorts": "List all available resorts with their basic information",
    "get_resort_details": "Get detailed information about a specific resort"
}

schemas = generate_schemas_from_module(tools, descriptions)
```

## 🛡️ Error Handling

The system includes comprehensive error handling:

- **Database errors**: Proper session management and cleanup
- **OpenAI API errors**: Graceful degradation to demo mode
- **Function call errors**: Detailed error messages
- **Type validation**: Automatic parameter validation

## 📚 Key Concepts Demonstrated

1. **OpenAI Function Calling**: Complete implementation with proper schemas
2. **SQLAlchemy ORM**: Database models, relationships, and queries
3. **Type Safety**: Full type annotations and validation
4. **Automatic Schema Generation**: Reflection-based schema creation
5. **Error Handling**: Comprehensive error management
6. **Modular Design**: Clean separation of concerns

## 🤝 Contributing

Feel free to extend this example with:
- Additional booking functions
- More complex database queries
- Enhanced error handling
- Additional resort features
- Payment processing integration

## 📝 License

This project is for educational purposes and demonstrates OpenAI function calling integration patterns. 

## To run streamlit
- pip install streamlit

streamlit run streamlit_app.py