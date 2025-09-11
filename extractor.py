import re
from typing import Dict, List, Any
from schema import MaterialSpec, DimensionSpec, DesignSpec

class PromptExtractor:
    def __init__(self):
        self.material_keywords = {
            'steel': ['steel', 'metal', 'iron'],
            'concrete': ['concrete', 'cement'],
            'wood': ['wood', 'timber', 'lumber'],
            'glass': ['glass', 'glazed', 'transparent']
        }
        
        self.feature_keywords = [
            'facade', 'balcony', 'terrace', 'parking', 'elevator', 
            'stairs', 'roof', 'basement', 'garden', 'pool'
        ]
    
    def extract_stories(self, prompt: str) -> int:
        """Extract number of stories from prompt"""
        if not prompt or not prompt.strip():
            return 1
            
        # Handle written numbers first
        number_words = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
        }
        
        prompt_lower = prompt.lower().strip()
        
        # Check for written numbers + story/floor
        for word, num in number_words.items():
            if f'{word}-story' in prompt_lower or f'{word} story' in prompt_lower:
                return num
            if f'{word}-floor' in prompt_lower or f'{word} floor' in prompt_lower:
                return num
        
        # Check for digit patterns
        story_patterns = [
            r'(\d+)[-\s]*story',
            r'(\d+)[-\s]*storey', 
            r'(\d+)[-\s]*floor',
            r'(\d+)[-\s]*level'
        ]
        
        for pattern in story_patterns:
            match = re.search(pattern, prompt_lower)
            if match:
                return int(match.group(1))
        return 1
    
    def extract_materials(self, prompt: str) -> List[MaterialSpec]:
        """Extract materials from prompt"""
        materials = []
        prompt_lower = prompt.lower()
        
        for material_type, keywords in self.material_keywords.items():
            for keyword in keywords:
                if keyword in prompt_lower:
                    materials.append(MaterialSpec(type=material_type))
                    break
        
        return materials
    
    def extract_dimensions(self, prompt: str) -> DimensionSpec:
        """Extract dimensions from prompt"""
        dimensions = DimensionSpec()
        
        # Extract numeric values with units
        dimension_patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:m|meter|metre)s?\s*(?:x|by|\*)\s*(\d+(?:\.\d+)?)\s*(?:m|meter|metre)s?',
            r'(\d+(?:\.\d+)?)\s*(?:ft|feet|foot)\s*(?:x|by|\*)\s*(\d+(?:\.\d+)?)\s*(?:ft|feet|foot)'
        ]
        
        for pattern in dimension_patterns:
            match = re.search(pattern, prompt.lower())
            if match:
                dimensions.length = float(match.group(1))
                dimensions.width = float(match.group(2))
                break
        
        return dimensions
    
    def extract_features(self, prompt: str) -> List[str]:
        """Extract building features from prompt"""
        features = []
        prompt_lower = prompt.lower()
        
        for feature in self.feature_keywords:
            if feature in prompt_lower:
                features.append(feature)
        
        return features
    
    def extract_building_type(self, prompt: str) -> str:
        """Extract building type from prompt"""
        if not prompt or not prompt.strip():
            return 'general'
            
        building_types = ['residential', 'commercial', 'office', 'warehouse', 'retail', 'industrial']
        prompt_lower = prompt.lower().strip()
        
        for building_type in building_types:
            if building_type in prompt_lower:
                return building_type
        
        return 'general'
    
    def extract_spec(self, prompt: str) -> DesignSpec:
        """Extract complete design specification from prompt with enhanced error handling"""
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
            
        try:
            # Extract each component with individual error handling
            building_type = self.extract_building_type(prompt)
            stories = self.extract_stories(prompt)
            materials = self.extract_materials(prompt)
            dimensions = self.extract_dimensions(prompt)
            features = self.extract_features(prompt)
            
            # Validate extracted data
            if stories < 1:
                stories = 1
            if not materials:
                materials = [MaterialSpec(type="steel", grade="standard")]
            if not features:
                features = ["parking"]
                
            return DesignSpec(
                building_type=building_type,
                stories=stories,
                materials=materials,
                dimensions=dimensions,
                features=features,
                requirements=[prompt.strip()]
            )
        except Exception as e:
            print(f"[ERROR] Extraction failed for prompt '{prompt[:50]}...': {str(e)}")
            print(f"[RECOVERY] Generating fallback specification with default values")
            # Return minimal valid spec on error
            fallback_spec = DesignSpec(
                building_type="general",
                stories=1,
                materials=[MaterialSpec(type="steel")],
                dimensions=DimensionSpec(length=20.0, width=15.0, height=3.5, area=300.0),
                features=["parking"],
                requirements=[prompt.strip()]
            )
            print(f"[RECOVERY] Fallback specification created successfully")
            return fallback_spec