"""Prompt extraction utilities"""

import re
from typing import List
from src.schema import DesignSpec, MaterialSpec, DimensionSpec

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
        # Validate if prompt is building-related
        if not self.is_building_related(prompt):
            raise ValueError(f"Prompt does not appear to be building/construction related. Please provide a prompt about building design, construction, or architecture.")

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

    def is_building_related(self, prompt: str) -> bool:
        """Check if prompt is related to building/construction"""
        prompt_lower = prompt.lower()

        # Building-related keywords
        building_keywords = [
            'building', 'construction', 'house', 'office', 'warehouse', 'hospital',
            'school', 'apartment', 'residential', 'commercial', 'structure',
            'floor', 'story', 'room', 'wall', 'roof', 'foundation', 'architect',
            'design', 'blueprint', 'plan', 'concrete', 'steel', 'brick', 'cement',
            'material', 'dimension', 'height', 'width', 'length', 'area', 'square',
            'meter', 'feet', 'parking', 'elevator', 'balcony', 'basement'
        ]

        # Non-building keywords that indicate other content types
        non_building_keywords = [
            'story', 'tale', 'character', 'plot', 'chapter', 'novel', 'book',
            'recipe', 'cooking', 'ingredient', 'food', 'meal', 'dish',
            'movie', 'film', 'actor', 'director', 'scene',
            'song', 'music', 'lyrics', 'album', 'artist'
        ]

        # Count building-related keywords
        building_score = sum(1 for keyword in building_keywords if keyword in prompt_lower)

        # Count non-building keywords
        non_building_score = sum(1 for keyword in non_building_keywords if keyword in prompt_lower)

        # If we have strong non-building indicators and weak building indicators
        if non_building_score > 0 and building_score <= 1:
            return False

        # Require at least one building-related keyword
        return building_score > 0

    def extract_building_type(self, prompt: str) -> str:
        """Extract building type from prompt with enhanced detection"""
        prompt_lower = prompt.lower()

        # Enhanced building type patterns
        building_patterns = {
            'residential': ['residential', 'apartment', 'house', 'home', 'villa', 'condo'],
            'office': ['office', 'corporate', 'business', 'commercial building'],
            'warehouse': ['warehouse', 'storage', 'industrial', 'factory'],
            'hospital': ['hospital', 'medical', 'clinic', 'healthcare'],
            'school': ['school', 'university', 'education', 'college'],
            'retail': ['shop', 'store', 'mall', 'retail'],
            'hotel': ['hotel', 'resort', 'lodge'],
            'mixed_use': ['mixed use', 'multi-purpose']
        }

        # Check for specific building types
        for building_type, keywords in building_patterns.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return building_type

        # If no specific type found, try to infer from context
        if any(word in prompt_lower for word in ['floor', 'story', 'building']):
            return "commercial"  # Generic building

        return "commercial"  # Default to commercial instead of general

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
        """Extract materials from prompt with precise matching"""
        materials = []
        material_keywords = {
            'steel': ['steel', 'metal', 'iron'],
            'concrete': ['concrete'],
            'cement': ['cement'],
            'brick': ['brick', 'bricks'],
            'glass': ['glass', 'glazed'],
            'wood': ['wood', 'timber'],
            'stone': ['stone', 'marble', 'granite']
        }

        prompt_lower = prompt.lower()
        for material, keywords in material_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                grade = self._extract_material_grade(prompt_lower, material)
                materials.append(MaterialSpec(type=material, grade=grade))

        # Default material if none found
        if not materials:
            materials.append(MaterialSpec(type="concrete", grade="standard"))

        return materials

    def _extract_material_grade(self, prompt: str, material: str) -> str:
        """Extract material grade/specification"""
        grade_patterns = {
            'steel': r'(a36|a572|grade\s*\d+)',
            'concrete': r'(c\d+|m\d+|grade\s*\d+)',
            'cement': r'(opc|ppc|grade\s*\d+)',
            'brick': r'(red|clay|standard|grade\s*\d+)'
        }

        if material in grade_patterns:
            match = re.search(grade_patterns[material], prompt)
            if match:
                return match.group(1).upper()

        return "standard"

    def extract_dimensions(self, prompt: str, stories: int) -> DimensionSpec:
        """Extract dimensions from prompt with precise parsing"""
        length = width = height = area = None

        # Extract height specifically
        height_patterns = [
            r'height[\s:]*([\d.]+)[\s]*(?:m|meter|metres?)',
            r'([\d.]+)[\s]*(?:m|meter|metres?)[\s]*(?:high|height)',
            r'([\d.]+)[\s]*(?:m|meter|metres?)[\s]*tall'
        ]

        for pattern in height_patterns:
            match = re.search(pattern, prompt.lower())
            if match:
                height = float(match.group(1))
                break

        # Extract length
        length_patterns = [
            r'length[\s:]*([\d.]+)[\s]*(?:m|meter|metres?)',
            r'([\d.]+)[\s]*(?:m|meter|metres?)[\s]*(?:long|length)'
        ]

        for pattern in length_patterns:
            match = re.search(pattern, prompt.lower())
            if match:
                length = float(match.group(1))
                break

        # Extract width/breadth
        width_patterns = [
            r'(?:width|breadth)[\s:]*([\d.]+)[\s]*(?:m|meter|metres?)',
            r'([\d.]+)[\s]*(?:m|meter|metres?)[\s]*(?:wide|width|breadth)'
        ]

        for pattern in width_patterns:
            match = re.search(pattern, prompt.lower())
            if match:
                width = float(match.group(1))
                break

        # Fallback: look for dimension patterns like "15x15" or "15 by 15"
        if not length or not width:
            dim_patterns = [
                r'([\d.]+)[\s]*(?:x|by)[\s]*([\d.]+)[\s]*(?:m|meter|metres?)',
                r'([\d.]+)[\s]*(?:m|meter|metres?)[\s]*(?:x|by)[\s]*([\d.]+)[\s]*(?:m|meter|metres?)'
            ]

            for pattern in dim_patterns:
                match = re.search(pattern, prompt.lower())
                if match:
                    length = float(match.group(1))
                    width = float(match.group(2))
                    break

        # Calculate area if length and width available
        if length and width:
            area = length * width

        # Default height if not specified
        if not height:
            height = stories * 3.5

        return DimensionSpec(
            length=length,
            width=width,
            height=height,
            area=area
        )

    def extract_features(self, prompt: str) -> List[str]:
        """Extract features from prompt with comprehensive detection"""
        features = []
        feature_keywords = {
            'parking': ['parking', 'garage', 'car park'],
            'elevator': ['elevator', 'lift'],
            'balcony': ['balcony', 'terrace', 'deck'],
            'garden': ['garden', 'landscape', 'lawn'],
            'swimming_pool': ['pool', 'swimming'],
            'gym': ['gym', 'fitness', 'exercise'],
            'security': ['security', 'guard', 'cctv'],
            'air_conditioning': ['ac', 'air conditioning', 'hvac'],
            'solar_panels': ['solar', 'renewable'],
            'basement': ['basement', 'underground'],
            'rooftop': ['rooftop', 'roof access'],
            'fire_safety': ['fire', 'sprinkler', 'emergency']
        }

        prompt_lower = prompt.lower()
        for feature, keywords in feature_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                features.append(feature)

        # Add default features based on building type
        if not features:
            if any(word in prompt_lower for word in ['office', 'commercial']):
                features.extend(['parking', 'elevator'])
            elif any(word in prompt_lower for word in ['residential', 'house']):
                features.extend(['parking'])

        return features
