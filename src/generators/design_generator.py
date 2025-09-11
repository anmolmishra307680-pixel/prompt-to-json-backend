"""Design generator using existing extractor logic."""

import re
from typing import Dict, Any
from .base_generator import BaseGenerator

class DesignGenerator(BaseGenerator):
    """Generator for furniture/design specifications."""
    
    def __init__(self):
        self.known_materials = [
            'wood', 'wooden', 'oak', 'pine', 'mahogany',
            'metal', 'steel', 'aluminum', 'iron', 'stainless steel',
            'glass', 'crystal', 'plastic', 'polymer', 'fabric', 'cloth',
            'leather', 'hide', 'concrete', 'cement', 'carbon fiber'
        ]
    
    def generate_spec(self, prompt: str) -> Dict[str, Any]:
        """Generate design specification from prompt."""
        extracted = self._extract_fields(prompt)
        
        # Apply smart defaults
        spec = {
            "type": extracted.get('type') or 'furniture',
            "material": extracted.get('material') or ['wood'],
            "color": self._get_smart_color(extracted),
            "dimensions": extracted.get('dimensions') or {},
            "purpose": extracted.get('purpose') or 'general',
            "metadata": {
                "generated_by": "design_generator",
                "confidence": 0.8
            }
        }
        
        return {
            "spec": spec,
            "llm_output": f"Extracted design specification for {spec['type']}",
            "method": "rules"
        }
    
    def _extract_fields(self, prompt: str) -> Dict[str, Any]:
        """Extract fields using rule-based patterns."""
        prompt_lower = prompt.lower()
        
        # Type extraction
        type_patterns = {
            'table': ['table', 'desk', 'surface'],
            'chair': ['chair', 'seat', 'stool', 'throne'],
            'shelf': ['shelf', 'shelving', 'bookcase'],
            'cabinet': ['cabinet', 'cupboard'],
            'sofa': ['sofa', 'couch'],
            'bed': ['bed', 'mattress']
        }
        
        type_match = None
        for main_type, patterns in type_patterns.items():
            if any(pattern in prompt_lower for pattern in patterns):
                type_match = main_type
                break
        
        # Material extraction
        materials = []
        for material in self.known_materials:
            if material in prompt_lower:
                if material in ['wood', 'wooden', 'oak', 'pine']:
                    if 'wood' not in materials:
                        materials.append('wood')
                elif material in ['metal', 'steel', 'aluminum']:
                    if 'metal' not in materials:
                        materials.append('metal')
                elif material in ['glass', 'crystal']:
                    if 'glass' not in materials:
                        materials.append('glass')
                else:
                    if material not in materials:
                        materials.append(material)
        
        # Color extraction
        colors = ['red', 'blue', 'green', 'black', 'white', 'brown', 'gray', 'yellow', 'gold', 'silver']
        color_match = next((c for c in colors if c in prompt_lower), None)
        
        # Dimensions
        dimensions = self._parse_dimensions(prompt_lower)
        
        # Purpose
        purpose_patterns = {
            'dining': ['dining', 'eat', 'meal'],
            'office': ['office', 'work'],
            'storage': ['storage', 'organize'],
            'seating': ['sit', 'seat']
        }
        
        purpose_match = None
        for purpose, patterns in purpose_patterns.items():
            if any(pattern in prompt_lower for pattern in patterns):
                purpose_match = purpose
                break
        
        return {
            'type': type_match,
            'material': materials,
            'color': color_match,
            'dimensions': dimensions,
            'purpose': purpose_match
        }
    
    def _parse_dimensions(self, text: str) -> Dict[str, Any]:
        """Parse dimensions from text."""
        result = {}
        
        # Look for dimensions like "6 feet", "120 cm", "4x6"
        dim_pattern = r'(\d+(?:\.\d+)?)\s?(feet|ft|cm|m|inches?|in)'
        matches = re.findall(dim_pattern, text)
        
        if matches:
            value, unit = matches[0]
            result['raw'] = f"{value} {unit}"
            
            # Convert to cm
            if unit in ['feet', 'ft']:
                result['width_cm'] = float(value) * 30.48
            elif unit == 'cm':
                result['width_cm'] = float(value)
            elif unit == 'm':
                result['width_cm'] = float(value) * 100
        
        return result
    
    def _get_smart_color(self, extracted: Dict[str, Any]) -> str:
        """Apply smart color defaults based on material."""
        if extracted.get('color'):
            return extracted['color']
        
        materials = extracted.get('material', [])
        if 'wood' in materials:
            return 'brown'
        elif 'metal' in materials:
            return 'silver'
        elif 'glass' in materials:
            return 'clear'
        
        return 'natural'