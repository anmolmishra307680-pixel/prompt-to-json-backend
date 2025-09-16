"""Load testing for 50 concurrent users"""

import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor

async def test_endpoint(session, url, data):
    """Test single endpoint"""
    try:
        async with session.post(url, json=data) as response:
            return await response.json()
    except Exception as e:
        return {"error": str(e)}

async def load_test_50_users():
    """Simulate 50 concurrent users"""
    url = "http://localhost:8000/generate"
    data = {"prompt": "Modern office building"}
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(50):
            task = test_endpoint(session, url, data)
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

if __name__ == "__main__":
    asyncio.run(load_test_50_users())