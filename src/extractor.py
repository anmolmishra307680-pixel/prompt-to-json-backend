import re
from typing import List, Dict

MATERIALS = ["steel", "glass", "concrete", "wood", "aluminum", "carbon fiber", "carbon-fiber", "brick"]
OBJECTS = ["building", "gearbox", "throne", "drone", "arm", "house", "chest", "scene", "robotic hand"]

def find_keywords(prompt: str, keywords: List[str]) -> List[str]:
    p = prompt.lower()
    return [k for k in keywords if k in p]

def extract_basic_fields(prompt: str) -> Dict:
    p = prompt.lower()
    fields = {
        "type": None,
        "material": [],
        "color": None,
        "dimensions": None,
        "purpose": None,
        "extras": None
    }
    
    # type
    found = find_keywords(p, OBJECTS)
    fields["type"] = found[0] if found else None
    
    # materials
    fields["material"] = find_keywords(p, MATERIALS)
    
    # color
    m = re.search(r"\b(red|blue|green|black|white|brown|gold|silver)\b", p)
    if m: 
        fields["color"] = m.group(1)
    
    # simple dimension pattern (e.g., 15x15cm or 2-floor)
    d = re.search(r"(\d+(\.\d+)?\s?(x|\sby\s)\s?\d+(\.\d+)?\s?(cm|mm|m)?)|(\d+\s?-?\s?floor|\d+\s?storey)", p)
    if d: 
        fields["dimensions"] = d.group(0)
    
    # purpose / extras heuristics
    if "for" in p:
        parts = p.split("for", 1)[1].strip()
        fields["purpose"] = parts.split(".")[0][:80]
    
    return fields