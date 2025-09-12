"""Universal schema for any prompt type"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime

class UniversalSpec(BaseModel):
    """Universal specification that adapts to any prompt type"""
    prompt_type: str = Field(description="Type of prompt (email, task, building, product, etc.)")
    title: str = Field(description="Main title or subject")
    description: str = Field(description="Detailed description")
    components: List[Dict[str, Any]] = Field(default_factory=list, description="Main components or parts")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Key properties and attributes")
    requirements: List[str] = Field(default_factory=list, description="Requirements or constraints")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    timestamp: datetime = Field(default_factory=datetime.now)

class PromptClassifier:
    """Classify prompts into different types"""
    
    PROMPT_TYPES = {
        'email': ['email', 'message', 'letter', 'communication', 'send', 'write'],
        'task': ['task', 'todo', 'action', 'complete', 'do', 'perform'],
        'building': ['building', 'house', 'office', 'construction', 'architect'],
        'product': ['product', 'device', 'gadget', 'create', 'build', 'design'],
        'event': ['event', 'meeting', 'schedule', 'plan', 'organize'],
        'document': ['document', 'report', 'proposal', 'specification', 'manual'],
        'software': ['app', 'software', 'system', 'platform', 'code', 'program'],
        'process': ['process', 'workflow', 'procedure', 'method', 'steps'],
        'creative': ['story', 'poem', 'creative', 'write', 'compose'],
        'analysis': ['analyze', 'research', 'study', 'investigate', 'examine']
    }
    
    @classmethod
    def classify(cls, prompt: str) -> str:
        """Classify prompt into most likely type"""
        prompt_lower = prompt.lower()
        
        scores = {}
        for prompt_type, keywords in cls.PROMPT_TYPES.items():
            score = sum(1 for keyword in keywords if keyword in prompt_lower)
            if score > 0:
                scores[prompt_type] = score
        
        if scores:
            return max(scores, key=scores.get)
        return 'general'

class UniversalExtractor:
    """Extract structured data from any prompt type"""
    
    def extract_spec(self, prompt: str) -> UniversalSpec:
        """Extract universal specification from any prompt"""
        prompt_type = PromptClassifier.classify(prompt)
        
        if prompt_type == 'email':
            return self._extract_email_spec(prompt)
        elif prompt_type == 'task':
            return self._extract_task_spec(prompt)
        elif prompt_type == 'building':
            return self._extract_building_spec(prompt)
        elif prompt_type == 'product':
            return self._extract_product_spec(prompt)
        elif prompt_type == 'event':
            return self._extract_event_spec(prompt)
        elif prompt_type == 'software':
            return self._extract_software_spec(prompt)
        else:
            return self._extract_general_spec(prompt, prompt_type)
    
    def _extract_email_spec(self, prompt: str) -> UniversalSpec:
        """Extract email specification"""
        import re
        
        # Extract recipient
        recipient_match = re.search(r'to (?:the )?(\w+(?:\s+\w+)*)', prompt.lower())
        recipient = recipient_match.group(1) if recipient_match else "recipient"
        
        # Extract subject/topic
        subject_keywords = ['about', 'regarding', 'announcing', 'informing']
        subject = "Email Communication"
        for keyword in subject_keywords:
            if keyword in prompt.lower():
                parts = prompt.lower().split(keyword)
                if len(parts) > 1:
                    subject = parts[1].strip()[:50]
                    break
        
        return UniversalSpec(
            prompt_type="email",
            title=f"Email to {recipient}",
            description=prompt,
            components=[
                {"type": "recipient", "value": recipient},
                {"type": "subject", "value": subject},
                {"type": "body", "value": "email content"}
            ],
            properties={
                "format": "professional" if "professional" in prompt.lower() else "casual",
                "urgency": "high" if any(word in prompt.lower() for word in ['urgent', 'asap', 'immediately']) else "normal",
                "length": "short" if "short" in prompt.lower() or "brief" in prompt.lower() else "medium"
            },
            requirements=[prompt]
        )
    
    def _extract_task_spec(self, prompt: str) -> UniversalSpec:
        """Extract task specification"""
        # Extract action verbs
        action_verbs = ['create', 'build', 'write', 'design', 'develop', 'implement', 'plan']
        action = next((verb for verb in action_verbs if verb in prompt.lower()), "complete")
        
        # Extract deadline if mentioned
        import re
        deadline_match = re.search(r'by (\w+\s+\d+)', prompt.lower())
        deadline = deadline_match.group(1) if deadline_match else "not specified"
        
        return UniversalSpec(
            prompt_type="task",
            title=f"Task: {action.title()}",
            description=prompt,
            components=[
                {"type": "action", "value": action},
                {"type": "deliverable", "value": "task output"},
                {"type": "deadline", "value": deadline}
            ],
            properties={
                "priority": "high" if any(word in prompt.lower() for word in ['urgent', 'important', 'critical']) else "medium",
                "complexity": "high" if len(prompt.split()) > 20 else "medium"
            },
            requirements=[prompt]
        )
    
    def _extract_building_spec(self, prompt: str) -> UniversalSpec:
        """Extract building specification (legacy compatibility)"""
        from extractor import PromptExtractor
        
        extractor = PromptExtractor()
        old_spec = extractor.extract_spec(prompt)
        
        return UniversalSpec(
            prompt_type="building",
            title=f"{old_spec.building_type.title()} Building",
            description=prompt,
            components=[
                {"type": "structure", "stories": old_spec.stories},
                {"type": "materials", "list": [m.type for m in old_spec.materials]},
                {"type": "dimensions", "value": old_spec.dimensions.model_dump()}
            ],
            properties={
                "building_type": old_spec.building_type,
                "total_area": old_spec.dimensions.area,
                "features": old_spec.features
            },
            requirements=[prompt]
        )
    
    def _extract_product_spec(self, prompt: str) -> UniversalSpec:
        """Extract product specification"""
        # Extract product type
        product_types = ['device', 'gadget', 'tool', 'system', 'controller', 'sensor']
        product_type = next((ptype for ptype in product_types if ptype in prompt.lower()), "product")
        
        # Extract features
        features = []
        feature_keywords = ['smart', 'wireless', 'automatic', 'digital', 'portable', 'rechargeable']
        for keyword in feature_keywords:
            if keyword in prompt.lower():
                features.append(keyword)
        
        return UniversalSpec(
            prompt_type="product",
            title=f"{product_type.title()} Specification",
            description=prompt,
            components=[
                {"type": "hardware", "value": product_type},
                {"type": "features", "list": features},
                {"type": "interface", "value": "user interface"}
            ],
            properties={
                "category": product_type,
                "smart_features": len([f for f in features if f in ['smart', 'automatic', 'digital']]),
                "connectivity": "wireless" if "wireless" in features else "wired"
            },
            requirements=[prompt]
        )
    
    def _extract_event_spec(self, prompt: str) -> UniversalSpec:
        """Extract event specification"""
        import re
        
        # Extract date/time
        date_match = re.search(r'(\w+\s+\d+|\d+/\d+|\d+-\d+-\d+)', prompt)
        event_date = date_match.group(1) if date_match else "TBD"
        
        # Extract event type
        event_types = ['meeting', 'conference', 'workshop', 'presentation', 'training']
        event_type = next((etype for etype in event_types if etype in prompt.lower()), "event")
        
        return UniversalSpec(
            prompt_type="event",
            title=f"{event_type.title()} Event",
            description=prompt,
            components=[
                {"type": "schedule", "date": event_date},
                {"type": "agenda", "value": "event agenda"},
                {"type": "participants", "value": "attendees"}
            ],
            properties={
                "event_type": event_type,
                "duration": "1 hour" if "hour" in prompt.lower() else "TBD",
                "location": "virtual" if any(word in prompt.lower() for word in ['online', 'virtual', 'zoom']) else "physical"
            },
            requirements=[prompt]
        )
    
    def _extract_software_spec(self, prompt: str) -> UniversalSpec:
        """Extract software specification"""
        # Extract platform
        platforms = ['web', 'mobile', 'desktop', 'api', 'cloud']
        platform = next((p for p in platforms if p in prompt.lower()), "application")
        
        # Extract functionality
        functions = []
        function_keywords = ['login', 'search', 'payment', 'notification', 'analytics', 'chat']
        for keyword in function_keywords:
            if keyword in prompt.lower():
                functions.append(keyword)
        
        return UniversalSpec(
            prompt_type="software",
            title=f"{platform.title()} Application",
            description=prompt,
            components=[
                {"type": "frontend", "platform": platform},
                {"type": "backend", "value": "server logic"},
                {"type": "database", "value": "data storage"}
            ],
            properties={
                "platform": platform,
                "features": functions,
                "architecture": "client-server" if platform in ['web', 'mobile'] else "standalone"
            },
            requirements=[prompt]
        )
    
    def _extract_general_spec(self, prompt: str, prompt_type: str) -> UniversalSpec:
        """Extract general specification for unknown types"""
        # Extract key entities (simple NLP)
        words = prompt.split()
        entities = [word for word in words if len(word) > 4 and word.isalpha()][:5]
        
        return UniversalSpec(
            prompt_type=prompt_type,
            title=f"{prompt_type.title()} Specification",
            description=prompt,
            components=[
                {"type": "main_entity", "value": entities[0] if entities else "unknown"},
                {"type": "context", "value": " ".join(entities[1:3]) if len(entities) > 1 else "general"}
            ],
            properties={
                "complexity": "high" if len(words) > 20 else "medium",
                "entities": entities
            },
            requirements=[prompt]
        )