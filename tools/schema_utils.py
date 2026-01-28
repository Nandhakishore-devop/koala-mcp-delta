import inspect
from typing import get_type_hints, Any, Dict, List, Optional, Union

def get_openai_type(py_type: Any) -> str:
    """Map Python types to JSON schema types, handling Optional/Union."""
    # Handle Optional/Union by taking the first non-None type
    origin = getattr(py_type, "__origin__", None)
    if origin is Union:
        args = getattr(py_type, "__args__", [])
        # Find the first type that isn't None
        for arg in args:
            if arg is not type(None):
                py_type = arg
                break
    
    if py_type is str:
        return "string"
    if py_type is int:
        return "integer"
    if py_type is float:
        return "number"
    if py_type is bool:
        return "boolean"
    
    origin = getattr(py_type, "__origin__", None)
    if origin is list:
        return "array"
    if origin is dict:
        return "object"
    return "string"  # Default fallback

def generate_schema(func: callable) -> Dict[str, Any]:
    """
    Generate an OpenAI-compatible function schema from a Python function.
    Uses docstrings for descriptions and type hints for parameter types.
    """
    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    docstring = inspect.getdoc(func) or "No description provided."
    
    # Simple docstring parsing: first line as description
    description = docstring.split('\n')[0]
    
    parameters = {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
    }
    
    for name, param in signature.parameters.items():
        if name == 'session' or name == 'args' or name == 'kwargs':
            continue
            
        param_type = type_hints.get(name, str)
        json_type = get_openai_type(param_type)
        
        param_info = {"type": json_type}
        
        # Add items description if it's an array
        if json_type == "array":
            param_info["items"] = {"type": "string"}
            
        # Try to find parameter description in docstring
        # Look for ":param name: description" or similar
        description_lines = [line.strip() for line in docstring.split('\n') if f":param {name}:" in line or f"{name}" in line.split(':')[0]]
        if description_lines:
            # Simple heuristic: take the first line that looks like a param description
            param_info["description"] = description_lines[0].split(':')[-1].strip()
        else:
            param_info["description"] = f"The {name} parameter"

        parameters["properties"][name] = param_info
        
        if param.default is inspect.Parameter.empty:
            parameters["required"].append(name)
            
    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": description,
            "parameters": parameters
        }
    }
