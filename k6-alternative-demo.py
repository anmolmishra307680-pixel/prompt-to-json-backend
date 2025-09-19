#!/usr/bin/env python3
"""k6 Alternative Load Test Demo"""

import requests
import time
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor
import json

def test_endpoint(url, headers=None, payload=None):
    """Test a single endpoint"""
    start = time.time()
    try:
        if payload:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
        else:
            response = requests.get(url, headers=headers, timeout=10)
        
        duration = (time.time() - start) * 1000
        return {
            'status': response.status_code,
            'duration': duration,
            'success': response.status_code in [200, 401],  # 401 is expected without auth
            'size': len(response.content)
        }
    except Exception as e:
        duration = (time.time() - start) * 1000
        return {
            'status': 0,
            'duration': duration,
            'success': False,
            'error': str(e),
            'size': 0
        }

def run_load_test(name, vus, duration_sec, target_url):
    """Run load test simulation"""
    print(f"\n{name}")
    print(f"Virtual Users: {vus}")
    print(f"Duration: {duration_sec}s")
    print(f"Target: {target_url}")
    print("-" * 50)
    
    results = []
    start_time = time.time()
    
    def worker():
        while time.time() - start_time < duration_sec:
            # Test different endpoints randomly
            endpoints = [
                (f"{target_url}/health", None, None),
                (f"{target_url}/basic-metrics", None, None),
                (f"{target_url}/", None, None),
            ]
            
            url, headers, payload = endpoints[int(time.time()) % len(endpoints)]
            result = test_endpoint(url, headers, payload)
            results.append(result)
            time.sleep(1)  # 1 request per second per VU
    
    # Run with thread pool
    with ThreadPoolExecutor(max_workers=vus) as executor:
        futures = [executor.submit(worker) for _ in range(vus)]
        for future in futures:
            future.result()
    
    # Calculate metrics
    if results:
        successful = [r for r in results if r['success']]
        durations = [r['duration'] for r in successful]
        
        total_requests = len(results)
        success_count = len(successful)
        success_rate = (success_count / total_requests * 100) if total_requests > 0 else 0
        
        if durations:
            avg_duration = statistics.mean(durations)
            p95_duration = sorted(durations)[int(len(durations) * 0.95)] if len(durations) > 1 else durations[0]
            min_duration = min(durations)
            max_duration = max(durations)
            rps = total_requests / duration_sec
        else:
            avg_duration = p95_duration = min_duration = max_duration = rps = 0
        
        print(f"Results:")
        print(f"   Total Requests: {total_requests}")
        print(f"   Successful: {success_count} ({success_rate:.1f}%)")
        print(f"   Failed: {total_requests - success_count}")
        print(f"   Requests/sec: {rps:.1f}")
        print(f"   Avg Response: {avg_duration:.1f}ms")
        print(f"   95th Percentile: {p95_duration:.1f}ms")
        print(f"   Min/Max: {min_duration:.1f}ms / {max_duration:.1f}ms")
        
        return {
            'total_requests': total_requests,
            'success_count': success_count,
            'success_rate': success_rate,
            'rps': rps,
            'avg_duration': avg_duration,
            'p95_duration': p95_duration
        }
    else:
        print("No results collected")
        return None

if __name__ == "__main__":
    target = "http://localhost:8000"
    
    print("k6 Alternative Load Test Demo")
    print("=" * 50)
    
    # Light Load Test
    light_results = run_load_test("Light Load (Development)", 10, 30, target)
    
    # Medium Load Test  
    medium_results = run_load_test("Medium Load (Staging)", 25, 20, target)
    
    # Summary
    print("\nLoad Test Summary")
    print("=" * 50)
    if light_results:
        print(f"Light Load:  {light_results['rps']:.1f} RPS, {light_results['avg_duration']:.1f}ms avg")
    if medium_results:
        print(f"Medium Load: {medium_results['rps']:.1f} RPS, {medium_results['avg_duration']:.1f}ms avg")
    
    print("\nTo install k6 for real testing:")
    print("   1. Download from: https://github.com/grafana/k6/releases")
    print("   2. Extract to C:\\k6\\ and add to PATH")
    print("   3. Run: k6 run load-tests/k6/generate_load_test.js")