import json

def loadJSON(file_path: str) -> dict:
    """Load and parse a JSON file.
    
    Args:
        file_path (str): Path to the JSON file.
    
    Returns:
        dict: Parsed JSON data.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in '{file_path}': {e.msg}", e.doc, e.pos)