"""Structured logging and prompt memory utilities."""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any

def log_prompt(prompt: str, spec_path: str = "", llm_output: str = "", timestamp: str = "", **kwargs) -> None:
    """Log prompt interaction to structured JSONL file."""
    
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Use provided timestamp or generate new one
    if not timestamp:
        timestamp = datetime.now().isoformat()
    
    # Create log entry
    log_entry = {
        "timestamp": timestamp,
        "prompt": prompt,
        "spec_path": spec_path,
        "llm_output": llm_output,
        **kwargs  # Additional fields like evaluation, score, etc.
    }
    
    # Append to interaction logs
    with open("logs/interaction_logs.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

def get_last_prompts(n: int = 5) -> List[Dict[str, Any]]:
    """Retrieve last n prompt entries from interaction logs."""
    
    log_file = "logs/interaction_logs.jsonl"
    
    if not os.path.exists(log_file):
        return []
    
    entries = []
    
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue
        
        # Return last n entries
        return entries[-n:] if entries else []
        
    except Exception as e:
        print(f"Error reading logs: {e}")
        return []

def get_prompt_stats() -> Dict[str, Any]:
    """Get statistics about logged prompts."""
    
    entries = get_last_prompts(n=1000)  # Get more entries for stats
    
    if not entries:
        return {"total_prompts": 0}
    
    # Calculate basic stats
    total_prompts = len(entries)
    
    # Count by type if available
    types = {}
    materials = {}
    
    for entry in entries:
        # Try to extract type from spec_path or other fields
        if "type" in entry:
            type_val = entry["type"]
            types[type_val] = types.get(type_val, 0) + 1
        
        if "material" in entry:
            material_val = entry["material"]
            if isinstance(material_val, list):
                for mat in material_val:
                    materials[mat] = materials.get(mat, 0) + 1
            else:
                materials[material_val] = materials.get(material_val, 0) + 1
    
    return {
        "total_prompts": total_prompts,
        "most_recent": entries[-1]["timestamp"] if entries else None,
        "oldest": entries[0]["timestamp"] if entries else None,
        "top_types": dict(sorted(types.items(), key=lambda x: x[1], reverse=True)[:5]),
        "top_materials": dict(sorted(materials.items(), key=lambda x: x[1], reverse=True)[:5])
    }

def create_log_snapshot(n: int = 10, output_file: str = "reports/day5_log_snapshot.json") -> str:
    """Create snapshot of last n logs and save to file."""
    
    # Get last n entries
    entries = get_last_prompts(n)
    
    # Get stats
    stats = get_prompt_stats()
    
    # Create snapshot
    snapshot = {
        "snapshot_timestamp": datetime.now().isoformat(),
        "entries_count": len(entries),
        "requested_count": n,
        "statistics": stats,
        "entries": entries
    }
    
    # Save snapshot
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    
    print(f"Log snapshot saved to: {output_file}")
    return output_file

if __name__ == "__main__":
    # Demo logging functionality
    print("=== Logger Demo ===")
    
    # Test logging
    log_prompt(
        prompt="Design a wooden table",
        spec_path="spec_outputs/test.json",
        llm_output="Generated spec successfully",
        evaluation_score=8.5,
        validation_passed=True
    )
    
    log_prompt(
        prompt="Create a steel chair",
        spec_path="spec_outputs/chair.json",
        evaluation_score=7.2,
        validation_passed=False
    )
    
    # Test retrieval
    print("\nLast 3 prompts:")
    recent = get_last_prompts(3)
    for i, entry in enumerate(recent, 1):
        print(f"{i}. {entry['prompt']} ({entry['timestamp']})")
    
    # Test stats
    print("\nPrompt statistics:")
    stats = get_prompt_stats()
    print(json.dumps(stats, indent=2))
    
    # Create snapshot
    print("\nCreating log snapshot...")
    create_log_snapshot(10)