"""Universal evaluator for any specification type"""

from typing import Dict, List
from datetime import datetime
from universal_schema import UniversalSpec
from schema import EvaluationResult

class UniversalEvaluator:
    """Evaluator that works with any specification type"""
    
    def __init__(self):
        self.evaluation_criteria = {
            'email': self._evaluate_email,
            'task': self._evaluate_task,
            'building': self._evaluate_building,
            'product': self._evaluate_product,
            'event': self._evaluate_event,
            'software': self._evaluate_software,
            'general': self._evaluate_general
        }
    
    def evaluate_spec(self, spec: UniversalSpec, prompt: str) -> EvaluationResult:
        """Evaluate universal specification"""
        # Get type-specific evaluator
        evaluator = self.evaluation_criteria.get(spec.prompt_type, self._evaluate_general)
        
        # Perform evaluation
        scores = evaluator(spec, prompt)
        
        # Calculate overall score
        overall_score = (scores['completeness'] + scores['accuracy'] + scores['relevance']) / 3
        
        # Generate feedback
        feedback = self._generate_feedback(spec, scores)
        suggestions = self._generate_suggestions(spec, scores)
        
        return EvaluationResult(
            score=overall_score,
            completeness=scores['completeness'],
            format_validity=scores['accuracy'],
            feedback=feedback,
            suggestions=suggestions,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        )
    
    def _evaluate_email(self, spec: UniversalSpec, prompt: str) -> Dict[str, float]:
        """Evaluate email specification"""
        completeness = 0
        accuracy = 100  # Always valid format
        relevance = 0
        
        # Check completeness
        if any(comp.get('type') == 'recipient' for comp in spec.components):
            completeness += 30
        if any(comp.get('type') == 'subject' for comp in spec.components):
            completeness += 30
        if spec.properties.get('format'):
            completeness += 20
        if spec.properties.get('length'):
            completeness += 20
        
        # Check relevance to prompt
        if 'email' in prompt.lower():
            relevance += 40
        if any(word in prompt.lower() for word in ['send', 'write', 'message']):
            relevance += 30
        if spec.properties.get('format') == 'professional' and 'professional' in prompt.lower():
            relevance += 30
        
        return {
            'completeness': min(completeness, 100),
            'accuracy': accuracy,
            'relevance': min(relevance, 100)
        }
    
    def _evaluate_task(self, spec: UniversalSpec, prompt: str) -> Dict[str, float]:
        """Evaluate task specification"""
        completeness = 0
        accuracy = 100
        relevance = 0
        
        # Check completeness
        if any(comp.get('type') == 'action' for comp in spec.components):
            completeness += 40
        if any(comp.get('type') == 'deliverable' for comp in spec.components):
            completeness += 30
        if spec.properties.get('priority'):
            completeness += 15
        if spec.properties.get('complexity'):
            completeness += 15
        
        # Check relevance
        if any(word in prompt.lower() for word in ['task', 'do', 'complete', 'create']):
            relevance += 50
        if spec.properties.get('priority') and any(word in prompt.lower() for word in ['urgent', 'important']):
            relevance += 25
        if len(spec.components) >= 3:
            relevance += 25
        
        return {
            'completeness': min(completeness, 100),
            'accuracy': accuracy,
            'relevance': min(relevance, 100)
        }
    
    def _evaluate_building(self, spec: UniversalSpec, prompt: str) -> Dict[str, float]:
        """Evaluate building specification (legacy compatibility)"""
        completeness = 0
        accuracy = 100
        relevance = 0
        
        # Check completeness
        if spec.properties.get('building_type'):
            completeness += 25
        if any(comp.get('type') == 'materials' for comp in spec.components):
            completeness += 25
        if any(comp.get('type') == 'dimensions' for comp in spec.components):
            completeness += 25
        if spec.properties.get('features'):
            completeness += 25
        
        # Check relevance
        if any(word in prompt.lower() for word in ['building', 'house', 'office', 'construction']):
            relevance += 60
        if spec.properties.get('building_type') != 'general':
            relevance += 40
        
        return {
            'completeness': min(completeness, 100),
            'accuracy': accuracy,
            'relevance': min(relevance, 100)
        }
    
    def _evaluate_product(self, spec: UniversalSpec, prompt: str) -> Dict[str, float]:
        """Evaluate product specification"""
        completeness = 0
        accuracy = 100
        relevance = 0
        
        # Check completeness
        if any(comp.get('type') == 'hardware' for comp in spec.components):
            completeness += 30
        if any(comp.get('type') == 'features' for comp in spec.components):
            completeness += 30
        if spec.properties.get('category'):
            completeness += 20
        if spec.properties.get('connectivity'):
            completeness += 20
        
        # Check relevance
        if any(word in prompt.lower() for word in ['product', 'device', 'gadget']):
            relevance += 50
        if spec.properties.get('smart_features', 0) > 0 and 'smart' in prompt.lower():
            relevance += 30
        if len(spec.components) >= 3:
            relevance += 20
        
        return {
            'completeness': min(completeness, 100),
            'accuracy': accuracy,
            'relevance': min(relevance, 100)
        }
    
    def _evaluate_software(self, spec: UniversalSpec, prompt: str) -> Dict[str, float]:
        """Evaluate software specification"""
        completeness = 0
        accuracy = 100
        relevance = 0
        
        # Check completeness
        if any(comp.get('type') == 'frontend' for comp in spec.components):
            completeness += 25
        if any(comp.get('type') == 'backend' for comp in spec.components):
            completeness += 25
        if spec.properties.get('platform'):
            completeness += 25
        if spec.properties.get('features'):
            completeness += 25
        
        # Check relevance
        if any(word in prompt.lower() for word in ['app', 'software', 'system', 'platform']):
            relevance += 60
        if spec.properties.get('platform') in prompt.lower():
            relevance += 40
        
        return {
            'completeness': min(completeness, 100),
            'accuracy': accuracy,
            'relevance': min(relevance, 100)
        }
    
    def _evaluate_event(self, spec: UniversalSpec, prompt: str) -> Dict[str, float]:
        """Evaluate event specification"""
        completeness = 0
        accuracy = 100
        relevance = 0
        
        # Check completeness
        if any(comp.get('type') == 'schedule' for comp in spec.components):
            completeness += 40
        if any(comp.get('type') == 'agenda' for comp in spec.components):
            completeness += 30
        if spec.properties.get('event_type'):
            completeness += 30
        
        # Check relevance
        if any(word in prompt.lower() for word in ['event', 'meeting', 'schedule']):
            relevance += 70
        if spec.properties.get('location') and any(word in prompt.lower() for word in ['online', 'virtual', 'office']):
            relevance += 30
        
        return {
            'completeness': min(completeness, 100),
            'accuracy': accuracy,
            'relevance': min(relevance, 100)
        }
    
    def _evaluate_general(self, spec: UniversalSpec, prompt: str) -> Dict[str, float]:
        """Evaluate general specification"""
        completeness = 0
        accuracy = 100
        relevance = 0
        
        # Basic completeness check
        if spec.title and len(spec.title) > 5:
            completeness += 30
        if len(spec.components) > 0:
            completeness += 30
        if len(spec.properties) > 0:
            completeness += 20
        if len(spec.requirements) > 0:
            completeness += 20
        
        # Basic relevance check
        if spec.description and len(spec.description) > 10:
            relevance += 40
        if len(spec.components) >= 2:
            relevance += 30
        if spec.metadata.get('confidence', 0) > 0.7:
            relevance += 30
        
        return {
            'completeness': min(completeness, 100),
            'accuracy': accuracy,
            'relevance': min(relevance, 100)
        }
    
    def _generate_feedback(self, spec: UniversalSpec, scores: Dict[str, float]) -> List[str]:
        """Generate feedback based on evaluation scores"""
        feedback = []
        
        if scores['completeness'] < 80:
            feedback.append("Specification could be more complete")
        
        if scores['relevance'] < 70:
            feedback.append("Specification may not fully match prompt intent")
        
        if len(spec.components) < 2:
            feedback.append("Consider adding more components")
        
        if len(spec.properties) < 2:
            feedback.append("Consider adding more properties")
        
        return feedback
    
    def _generate_suggestions(self, spec: UniversalSpec, scores: Dict[str, float]) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        if scores['completeness'] < 90:
            suggestions.append("Add more detailed components")
        
        if len(spec.properties) < 3:
            suggestions.append("Include additional properties")
        
        if not spec.metadata.get('confidence') or spec.metadata.get('confidence', 0) < 0.8:
            suggestions.append("Enhance specification with more specific details")
        
        return suggestions