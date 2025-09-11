"""Test script for retry logic."""

from src.retry_logic import run_with_retry, save_before_after_comparison

# Test with a simple prompt that should trigger retry
print("Testing retry logic with simple 'table' prompt...")
results = run_with_retry('table', 'design', max_retries=1)

print(f"Attempts: {len(results['attempts'])}")
print(f"Improved: {results['improved']}")
print(f"First attempt score: {results['attempts'][0]['scores'].get('format_score', 0):.1f}")

if len(results['attempts']) > 1:
    print(f"Second attempt score: {results['attempts'][1]['scores'].get('format_score', 0):.1f}")
    print(f"First prompt: {results['attempts'][0]['prompt']}")
    print(f"Second prompt: {results['attempts'][1]['prompt']}")
    
    # Save comparison
    comparison_path = save_before_after_comparison(results)
    if comparison_path:
        print(f"Comparison saved to: {comparison_path}")
else:
    print("No retry was triggered")

print("\n" + "="*50)

# Test with email prompt
print("Testing retry logic with simple 'email' prompt...")
email_results = run_with_retry('email', 'email', max_retries=1)

print(f"Email attempts: {len(email_results['attempts'])}")
print(f"Email improved: {email_results['improved']}")
print(f"Email first score: {email_results['attempts'][0]['scores'].get('format_score', 0):.1f}")

if len(email_results['attempts']) > 1:
    print(f"Email second score: {email_results['attempts'][1]['scores'].get('format_score', 0):.1f}")
    comparison_path = save_before_after_comparison(email_results)
    if comparison_path:
        print(f"Email comparison saved to: {comparison_path}")