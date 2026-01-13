import json
import re

def extract_json(text: str) -> dict:
    """
    Robustly extract and parse a JSON object from LLM output.

    Handles:
    - Markdown code fences (```json ... ```)
    - Extra text before or after JSON
    - Multiline JSON
    """

    if not text or not isinstance(text, str):
        raise ValueError("LLM output is empty or not a string")

    # Remove markdown code fences but keep inner JSON
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    # Find first opening brace
    start = text.find("{")
    if start == -1:
        raise ValueError("No opening '{' found in LLM output")

    # Find last closing brace
    end = text.rfind("}")
    if end == -1 or end <= start:
        raise ValueError("No valid closing '}' found in LLM output")

    json_str = text[start:end + 1]

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Extracted text is not valid JSON: {e}")