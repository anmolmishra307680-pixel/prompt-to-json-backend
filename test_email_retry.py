"""Test email retry logic."""

from src.retry_logic import run_with_retry, save_before_after_comparison

# Test with poor email prompt
print("Testing email retry with 'send message'...")
results = run_with_retry('send message', 'email', max_retries=1)

print(f"Attempts: {len(results['attempts'])}")
print(f"Improved: {results['improved']}")
print(f"Score before: {results['attempts'][0]['scores'].get('format_score', 0):.1f}")

if len(results['attempts']) > 1:
    print(f"Score after: {results['attempts'][1]['scores'].get('format_score', 0):.1f}")
    print(f"Prompt before: {results['attempts'][0]['prompt']}")
    print(f"Prompt after: {results['attempts'][1]['prompt']}")
    
    path = save_before_after_comparison(results)
    if path:
        print(f"Saved to: {path}")
else:
    print("No retry triggered")