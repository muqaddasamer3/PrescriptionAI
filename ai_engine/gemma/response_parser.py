import json
import re
from typing import Optional, Dict


def parse_gemma_response(raw_response: str) -> Optional[Dict]:
    """
    Gemma ke response se JSON nikaal kar Python dict mein convert karta hai,
    chahe response mein JSON se pehle/baad extra text ho.
    """
    try:
        return json.loads(raw_response.strip())
    except json.JSONDecodeError:
        pass

    match = re.search(r'\{.*\}', raw_response, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None

    return None


if __name__ == "__main__":
    sample = '''Some thinking text here...
    {
        "medicines": [{"name": "Panadol", "dosage": "500mg"}]
    }
    More text after...'''
    result = parse_gemma_response(sample)
    print(result)
