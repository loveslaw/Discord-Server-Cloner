import re
import os
import json
from typing import Dict, Any

def sanitize_filename(name: str) -> str:
    """Sanitize strings for safe filesystem file naming."""
    return re.sub(r'[\\/*?:"<>| ]', "_", name)

def save_json(filepath: str, data: Dict[str, Any]) -> None:
    """Save dictionary data to formatted JSON file with directory auto-creation."""
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(filepath: str) -> Dict[str, Any]:
    """Load JSON file from disk."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
