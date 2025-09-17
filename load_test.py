"""Load testing for 50 concurrent users"""

import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor

async def make_request(session, url, data, headers=None):
    """Make HTTP request"""
    try:
        async with session.post(url, json=data, headers=headers) as response:
            return await response.json()
    except Exception as e:
        return {"error": str(e)}

async def load_test_50_users():
    """Simulate 50 concurrent users"""
    url = "http://localhost:8000/generate"
    data = {"prompt": "Modern office building"}
    headers = {"X-API-Key": "bhiv-secret-key-2024"}
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(50):
            task = make_request(session, url, data, headers)
            tasks.append(task)
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        success_count = sum(1 for r in results if "error" not in r)
        
        print(f"Load Test Results:")
        print(f"Total requests: 50")
        print(f"Successful: {success_count}")
        print(f"Failed: {50 - success_count}")
        print(f"Total time: {end_time - start_time:.2f}s")
        print(f"Requests/second: {50 / (end_time - start_time):.2f}")

async def comprehensive_load_test():
    """Test system under 1000+ concurrent users"""
    from statistics import mean
    
    results = {
        'response_times': [],
        'successful_requests': 0,
        'failed_requests': 0
    }
    
    url = "https://prompt-to-json-backend.onrender.com/generate"
    data = {"prompt": "Modern office building"}
    headers = {"X-API-Key": "bhiv-secret-key-2024"}
    
    async def test_single_request():
        start_time = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, headers=headers) as resp:
                    if resp.status == 200:
                        results['successful_requests'] += 1
                    else:
                        results['failed_requests'] += 1
                    
                    response_time = time.time() - start_time
                    results['response_times'].append(response_time)
        except Exception:
            results['failed_requests'] += 1
    
    # Run 1000 concurrent requests
    tasks = [test_single_request() for _ in range(1000)]
    start_time = time.time()
    await asyncio.gather(*tasks)
    total_time = time.time() - start_time
    
    # Calculate metrics
    if results['response_times']:
        avg_response_time = mean(results['response_times'])
        p95_response_time = sorted(results['response_times'])[int(0.95 * len(results['response_times']))]
    else:
        avg_response_time = 0
        p95_response_time = 0
    
    print(f"""
🔥 LOAD TEST RESULTS - 1000 CONCURRENT USERS
═══════════════════════════════════════════
✅ Successful Requests: {results['successful_requests']}
❌ Failed Requests: {results['failed_requests']}
📊 Success Rate: {results['successful_requests']/1000*100:.1f}%
⏱️  Average Response Time: {avg_response_time:.3f}s
📈 95th Percentile: {p95_response_time:.3f}s
🚀 Requests/Second: {1000/total_time:.0f}
""")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--comprehensive":
        asyncio.run(comprehensive_load_test())
    else:
        asyncio.run(load_test_50_users())