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
        """Generate specification using LLM (EXPERIMENTAL STUB)
        
        NOTE: This is a basic implementation using GPT-2 for demonstration.
        For production use, integrate with larger models like GPT-4, LLaMA, etc.
        """
        try:
            from transformers import pipeline
            print("[EXPERIMENTAL] Using basic GPT-2 for LLM generation")
            
            # Basic GPT-2 pipeline (experimental)
            generator = pipeline("text-generation", model="gpt2", max_length=100)
            
            # Generate enhanced prompt for building extraction
            llm_prompt = f"Building description: {prompt}. Type:"
            result = generator(llm_prompt, max_new_tokens=30, pad_token_id=50256)
            
            # Parse LLM output and enhance rule-based extraction
            llm_text = result[0]['generated_text'].lower()
            spec = self._generate_with_rules(prompt)
            
            # Basic LLM-based building type enhancement
            if "office" in llm_text and spec.building_type == "general":
                spec.building_type = "office"
            elif "residential" in llm_text and spec.building_type == "general":
                spec.building_type = "residential"
            elif "commercial" in llm_text and spec.building_type == "general":
                spec.building_type = "commercial"
                
            return spec
            
        except ImportError:
            print("[FALLBACK] Transformers not available, using rule-based generation")
            return self._generate_with_rules(prompt)
        except Exception as e:
            print(f"[FALLBACK] LLM error ({str(e)}), using rule-based generation")
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
        """Improve specification based on feedback with enhanced error handling"""
        try:
            improved_spec = spec.model_copy()
            
            # Validate inputs
            if not isinstance(feedback, list) or not isinstance(suggestions, list):
                raise ValueError("Feedback and suggestions must be lists")
            
            # Apply improvements based on feedback
            improvements_applied = 0
            for suggestion in suggestions:
                if not isinstance(suggestion, str):
                    continue
                    
                suggestion_lower = suggestion.lower()
                
                if "materials" in suggestion_lower or "material" in suggestion_lower:
                    if not improved_spec.materials:
                        improved_spec.materials.append(MaterialSpec(type="steel"))
                        improvements_applied += 1
                
                elif "dimensions" in suggestion_lower or "size" in suggestion_lower:
                    if not improved_spec.dimensions.length:
                        improved_spec.dimensions.length = 25.0
                        improved_spec.dimensions.width = 20.0
                        improved_spec.dimensions.area = 500.0
                        improvements_applied += 1
                
                elif "features" in suggestion_lower or "feature" in suggestion_lower:
                    if len(improved_spec.features) < 3:
                        new_features = ['elevator', 'parking', 'balcony']
                        for feature in new_features:
                            if feature not in improved_spec.features:
                                improved_spec.features.append(feature)
                        improvements_applied += 1
            
            if improvements_applied == 0:
                print("[INFO] No applicable improvements found in suggestions")
            
            return improved_spec
            
        except Exception as e:
            print(f"[ERROR] Failed to improve spec: {str(e)}")
            return spec  # Return original spec on error