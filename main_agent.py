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
        if not prompt or len(prompt.strip()) < 3:
            raise ValueError("Prompt must be at least 3 characters long")
            
        try:
            if use_llm:
                return self._generate_with_llm(prompt)
            else:
                return self._generate_with_rules(prompt)
        except Exception as e:
            raise RuntimeError(f"Failed to generate specification: {str(e)}")
    
    def _generate_with_rules(self, prompt: str) -> DesignSpec:
        """Generate specification using rule-based extraction"""
        base_spec = self.extractor.extract_spec(prompt)
        
        # Enhance with additional logic
        enhanced_spec = self._enhance_specification(base_spec, prompt)
        
        return enhanced_spec
    
    def _generate_with_llm(self, prompt: str) -> DesignSpec:
        """Generate specification using LLM"""
        try:
            from transformers import pipeline
            
            # Initialize text generation pipeline
            generator = pipeline("text-generation", model="gpt2", max_length=100)
            
            # Generate enhanced prompt for building extraction
            llm_prompt = f"Building description: {prompt}. Type:"
            result = generator(llm_prompt, max_new_tokens=30, pad_token_id=50256)
            
            # Parse LLM output and enhance rule-based extraction
            llm_text = result[0]['generated_text'].lower()
            spec = self._generate_with_rules(prompt)
            
            # LLM-based building type enhancement
            if "office" in llm_text and spec.building_type == "general":
                spec.building_type = "office"
            elif "residential" in llm_text and spec.building_type == "general":
                spec.building_type = "residential"
            elif "commercial" in llm_text and spec.building_type == "general":
                spec.building_type = "commercial"
                
            return spec
            
        except ImportError:
            # Fallback to rule-based if transformers not available
            return self._generate_with_rules(prompt)
        except Exception:
            # Fallback on any LLM error
            return self._generate_with_rules(prompt)
    
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