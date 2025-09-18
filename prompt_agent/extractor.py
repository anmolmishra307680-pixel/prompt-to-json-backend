"""Prompt extraction utilities"""

import re
from typing import List
from schema import DesignSpec, MaterialSpec, DimensionSpec

class PromptExtractor:
    def __init__(self):
        self.building_types = {
            'office': ['office', 'corporate', 'business'],
            'residential': ['house', 'home', 'apartment', 'residential', 'modern residential'],
            'warehouse': ['warehouse', 'storage', 'industrial'],
            'hospital': ['hospital', 'medical', 'clinic'],
            'school': ['school', 'university', 'education']
        }
    
    def extract_spec(self, prompt: str) -> DesignSpec:
        """Extract design specification from prompt"""
        building_type = self.extract_building_type(prompt)
        stories = self.extract_stories(prompt)
        materials = self.extract_materials(prompt)
        dimensions = self.extract_dimensions(prompt, stories)
        features = self.extract_features(prompt)
        
        return DesignSpec(
            building_type=building_type,
            stories=stories,
            materials=materials,
            dimensions=dimensions,
            features=features,
            requirements=[prompt]
        )
    
    def extract_building_type(self, prompt: str) -> str:
        """Extract building type from prompt"""
        prompt_lower = prompt.lower()
        
        # Check for residential first (more specific patterns)
        residential_keywords = ['residential', 'apartment', 'house', 'home']
        if any(keyword in prompt_lower for keyword in residential_keywords):
            return "residential"
        
        # Check for compound phrases
        if 'modern residential' in prompt_lower or 'apartment complex' in prompt_lower:
            return "residential"
        
        # Then check other types
        for building_type, keywords in self.building_types.items():
            if building_type != 'residential':  # Skip residential as we handled it above
                if any(keyword in prompt_lower for keyword in keywords):
                    return building_type
        
        return "general"
    
    def extract_stories(self, prompt: str) -> int:
        """Extract number of stories from prompt"""
        story_patterns = [
            r'(\d+)[\s-]*story',
            r'(\d+)[\s-]*floor',
            r'(\d+)[\s-]*level'
        ]
        
        for pattern in story_patterns:
            match = re.search(pattern, prompt.lower())
            if match:
                return int(match.group(1))
        
        return 1
    
    def extract_materials(self, prompt: str) -> List[MaterialSpec]:
        """Extract materials from prompt"""
        materials = []
        material_keywords = {
            'steel': ['steel', 'metal'],
            'concrete': ['concrete', 'cement'],
            'glass': ['glass', 'glazed'],
            'wood': ['wood', 'timber']
        }
        
        prompt_lower = prompt.lower()
        for material, keywords in material_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                materials.append(MaterialSpec(type=material))
        
        return materials
    
    def extract_dimensions(self, prompt: str, stories: int) -> DimensionSpec:
        """Extract dimensions from prompt"""
        # Simple dimension extraction
        length = width = area = None
        height = stories * 3.5  # Default height per story
        
        # Look for dimension patterns
        dim_pattern = r'(\d+)[\s]*(?:x|by)[\s]*(\d+)'
        match = re.search(dim_pattern, prompt)
        if match:
            length = float(match.group(1))
            width = float(match.group(2))
            area = length * width
        
        return DimensionSpec(
            length=length,
            width=width,
            height=height,
            area=area
        )
    
    def extract_features(self, prompt: str) -> List[str]:
        """Extract features from prompt"""
        features = []
        feature_keywords = {
            'parking': ['parking', 'garage'],
            'elevator': ['elevator', 'lift'],
            'balcony': ['balcony', 'terrace'],
            'garden': ['garden', 'landscape']
        }
        
        prompt_lower = prompt.lower()
        for feature, keywords in feature_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                features.append(feature)
        
        return features