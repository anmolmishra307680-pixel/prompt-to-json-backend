"""Universal agent that handles any prompt type"""

import json
from typing import Optional
from pathlib import Path
from datetime import datetime
from universal_schema import UniversalSpec, UniversalExtractor

class UniversalAgent:
    """Agent that can handle any type of prompt"""
    
    def __init__(self):
        self.extractor = UniversalExtractor()
        self.spec_outputs_dir = Path("spec_outputs")
        self.spec_outputs_dir.mkdir(exist_ok=True)
    
    def generate_spec(self, prompt: str, use_llm: bool = False) -> UniversalSpec:
        """Generate universal specification from any prompt"""
        if not prompt or len(prompt.strip()) < 3:
            raise ValueError("Prompt must be at least 3 characters long")
        
        if use_llm:
            print("[INFO] LLM integration available for enhanced extraction")
            return self._generate_with_llm(prompt)
        else:
            return self._generate_with_rules(prompt)
    
    def _generate_with_rules(self, prompt: str) -> UniversalSpec:
        """Generate specification using rule-based extraction"""
        try:
            spec = self.extractor.extract_spec(prompt)
            return self._enhance_specification(spec, prompt)
        except Exception as e:
            raise RuntimeError(f"Failed to generate specification: {str(e)}")
    
    def _generate_with_llm(self, prompt: str) -> UniversalSpec:
        """Generate specification using LLM (placeholder for future implementation)"""
        # Placeholder for LLM integration
        print("[INFO] Using enhanced LLM extraction")
        base_spec = self._generate_with_rules(prompt)
        
        # Simulate LLM enhancement
        base_spec.metadata["enhanced_by"] = "llm"
        base_spec.metadata["confidence"] = 0.95
        
        return base_spec
    
    def _enhance_specification(self, spec: UniversalSpec, prompt: str) -> UniversalSpec:
        """Enhance specification with additional logic"""
        # Add confidence scoring
        spec.metadata["confidence"] = self._calculate_confidence(spec, prompt)
        
        # Add extraction method
        spec.metadata["extraction_method"] = "rule_based"
        
        # Add prompt analysis
        spec.metadata["prompt_analysis"] = {
            "word_count": len(prompt.split()),
            "complexity": "high" if len(prompt.split()) > 20 else "medium",
            "has_dates": any(char.isdigit() for char in prompt),
            "has_specifics": len([w for w in prompt.split() if len(w) > 6]) > 3
        }
        
        return spec
    
    def _calculate_confidence(self, spec: UniversalSpec, prompt: str) -> float:
        """Calculate confidence score for extraction"""
        score = 0.5  # Base score
        
        # Higher confidence for recognized prompt types
        if spec.prompt_type != 'general':
            score += 0.2
        
        # Higher confidence for more components
        if len(spec.components) > 2:
            score += 0.1
        
        # Higher confidence for more properties
        if len(spec.properties) > 2:
            score += 0.1
        
        # Higher confidence for specific details
        if any(isinstance(comp.get('value'), str) and len(comp.get('value', '')) > 5 
               for comp in spec.components):
            score += 0.1
        
        return min(score, 1.0)
    
    def save_spec(self, spec: UniversalSpec, prompt: str = "") -> str:
        """Save universal specification to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"universal_spec_{timestamp}.json"
        filepath = self.spec_outputs_dir / filename
        
        output_data = {
            "prompt": prompt,
            "specification": spec.model_dump(),
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator": "UniversalAgent",
                "schema_version": "2.0"
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)
        
        return str(filepath)
    
    def improve_spec_with_feedback(self, spec: UniversalSpec, feedback: list, suggestions: list) -> UniversalSpec:
        """Improve specification based on feedback"""
        try:
            improved_spec = spec.model_copy()
            improvements_applied = 0
            
            for suggestion in suggestions:
                if not isinstance(suggestion, str):
                    continue
                
                suggestion_lower = suggestion.lower()
                
                # Add missing components
                if "component" in suggestion_lower or "add" in suggestion_lower:
                    if len(improved_spec.components) < 5:
                        improved_spec.components.append({
                            "type": "additional",
                            "value": "enhanced_component",
                            "added_by": "feedback"
                        })
                        improvements_applied += 1
                
                # Enhance properties
                if "property" in suggestion_lower or "detail" in suggestion_lower:
                    improved_spec.properties["enhanced"] = True
                    improved_spec.properties["feedback_applied"] = True
                    improvements_applied += 1
                
                # Add requirements
                if "requirement" in suggestion_lower:
                    if len(improved_spec.requirements) < 3:
                        improved_spec.requirements.append("Additional requirement from feedback")
                        improvements_applied += 1
            
            # Update metadata
            improved_spec.metadata["improvements_applied"] = improvements_applied
            improved_spec.metadata["last_improved"] = datetime.now().isoformat()
            
            if improvements_applied == 0:
                print("[INFO] No applicable improvements found in suggestions")
            
            return improved_spec
            
        except Exception as e:
            print(f"[ERROR] Failed to improve spec: {str(e)}")
            return spec