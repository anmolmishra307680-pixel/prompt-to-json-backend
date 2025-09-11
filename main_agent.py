import json
from typing import Optional
from pathlib import Path
from datetime import datetime
from schema import DesignSpec, MaterialSpec, DimensionSpec
from extractor import PromptExtractor

class MainAgent:
    def __init__(self):
        self.extractor = PromptExtractor()
        self.spec_outputs_dir = Path("spec_outputs")
        self.spec_outputs_dir.mkdir(exist_ok=True)
    
    def generate_spec(self, prompt: str, use_llm: bool = False) -> DesignSpec:
        """Generate design specification from prompt"""
        if use_llm:
            return self._generate_with_llm(prompt)
        else:
            return self._generate_with_rules(prompt)
    
    def _generate_with_rules(self, prompt: str) -> DesignSpec:
        """Generate specification using rule-based extraction"""
        base_spec = self.extractor.extract_spec(prompt)
        
        # Enhance with additional logic
        enhanced_spec = self._enhance_specification(base_spec, prompt)
        
        return enhanced_spec
    
    def _generate_with_llm(self, prompt: str) -> DesignSpec:
        """Generate specification using LLM (stub implementation)"""
        # Stub LLM implementation - in real scenario, use transformers pipeline
        base_spec = self.extractor.extract_spec(prompt)
        
        # Simulate LLM enhancement
        llm_enhanced = self._simulate_llm_enhancement(base_spec, prompt)
        
        return llm_enhanced
    
    def _enhance_specification(self, spec: DesignSpec, prompt: str) -> DesignSpec:
        """Enhance specification with additional logic"""
        # Add default materials if none specified
        if not spec.materials:
            if 'steel' in prompt.lower():
                spec.materials.append(MaterialSpec(type="steel", grade="A36"))
            elif 'concrete' in prompt.lower():
                spec.materials.append(MaterialSpec(type="concrete", grade="C30"))
            else:
                spec.materials.append(MaterialSpec(type="steel", grade="standard"))
        
        # Estimate dimensions if not provided
        if spec.dimensions.length is None and spec.dimensions.width is None:
            # Default dimensions based on building type and stories
            if spec.building_type == 'warehouse' or spec.building_type == 'industrial':
                spec.dimensions.length = 40.0
                spec.dimensions.width = 30.0
            elif spec.stories <= 2:
                spec.dimensions.length = 20.0
                spec.dimensions.width = 15.0
            else:
                spec.dimensions.length = 30.0
                spec.dimensions.width = 25.0
            
            spec.dimensions.height = spec.stories * 3.5  # 3.5m per story
            spec.dimensions.area = spec.dimensions.length * spec.dimensions.width
        
        # Add default features based on building type
        if not spec.features:
            if spec.building_type == 'residential':
                spec.features.extend(['balcony', 'parking'])
            elif spec.building_type == 'commercial' or spec.building_type == 'office':
                spec.features.extend(['elevator', 'parking'])
            elif spec.building_type == 'warehouse' or spec.building_type == 'industrial':
                spec.features.extend(['parking', 'loading'])
            else:
                spec.features.append('parking')
        
        return spec
    
    def _simulate_llm_enhancement(self, spec: DesignSpec, prompt: str) -> DesignSpec:
        """Simulate LLM enhancement (placeholder for actual LLM integration)"""
        # This would be replaced with actual LLM calls
        enhanced_spec = spec.model_copy()
        
        # Simulate intelligent material selection
        if 'modern' in prompt.lower() or 'contemporary' in prompt.lower():
            enhanced_spec.materials.append(MaterialSpec(type="glass", properties={"transparency": "high"}))
        
        # Simulate feature enhancement
        if 'luxury' in prompt.lower() or 'premium' in prompt.lower():
            enhanced_spec.features.extend(['elevator', 'terrace', 'garden'])
        
        return enhanced_spec
    
    def save_spec(self, spec: DesignSpec, prompt: str = "") -> str:
        """Save specification to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"design_spec_{timestamp}.json"
        filepath = self.spec_outputs_dir / filename
        
        output_data = {
            "prompt": prompt,
            "specification": spec.model_dump(),
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator": "MainAgent"
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)
        
        return str(filepath)
    
    def improve_spec_with_feedback(self, spec: DesignSpec, feedback: list, suggestions: list) -> DesignSpec:
        """Improve specification based on feedback"""
        improved_spec = spec.model_copy()
        
        # Apply improvements based on feedback
        for suggestion in suggestions:
            if "materials" in suggestion.lower():
                if not improved_spec.materials:
                    improved_spec.materials.append(MaterialSpec(type="steel"))
            
            elif "dimensions" in suggestion.lower():
                if not improved_spec.dimensions.length:
                    improved_spec.dimensions.length = 25.0
                    improved_spec.dimensions.width = 20.0
            
            elif "features" in suggestion.lower():
                if len(improved_spec.features) < 3:
                    improved_spec.features.extend(['elevator', 'parking', 'balcony'])
        
        return improved_spec