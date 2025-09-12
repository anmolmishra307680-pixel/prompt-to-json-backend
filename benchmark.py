"""Comprehensive benchmarking and stress testing"""

import time
import asyncio
import concurrent.futures
from typing import List, Dict, Any
from dataclasses import dataclass
import statistics
from main_agent import MainAgent
from universal_agent import UniversalAgent
from evaluator_agent import EvaluatorAgent
from universal_evaluator import UniversalEvaluator
from rl_loop import RLLoop
from performance_monitor import monitor

@dataclass
class BenchmarkResult:
    """Benchmark test result"""
    test_name: str
    total_time: float
    avg_time: float
    min_time: float
    max_time: float
    success_rate: float
    throughput: float
    avg_score: float
    memory_usage: float

class BenchmarkSuite:
    """Comprehensive benchmarking suite"""
    
    def __init__(self):
        self.main_agent = MainAgent()
        self.universal_agent = UniversalAgent()
        self.evaluator_agent = EvaluatorAgent()
        self.universal_evaluator = UniversalEvaluator()
        
        self.test_prompts = {
            'building': [
                "Design a modern office building with 10 floors",
                "Create a residential complex with parking",
                "Build an industrial warehouse with steel frame",
                "Design a hospital with emergency facilities",
                "Create a shopping mall with multiple levels"
            ],
            'software': [
                "Create a mobile banking application",
                "Build a social media platform",
                "Design an e-commerce website",
                "Develop a project management tool",
                "Create a video streaming service"
            ],
            'email': [
                "Write a meeting invitation email",
                "Compose a project update message",
                "Draft a client proposal email",
                "Create a team announcement",
                "Write a follow-up email"
            ],
            'task': [
                "Create a software development timeline",
                "Plan a marketing campaign strategy",
                "Design a training program schedule",
                "Organize a product launch plan",
                "Develop a quality assurance process"
            ]
        }
    
    def run_single_test(self, prompt: str, mode: str = 'universal') -> Dict[str, Any]:
        """Run a single benchmark test"""
        start_time = time.time()
        success = True
        score = 0
        
        try:
            if mode == 'universal':
                spec = self.universal_agent.generate_spec(prompt)
                evaluation = self.universal_evaluator.evaluate_spec(spec, prompt)
            else:
                spec = self.main_agent.generate_spec(prompt)
                evaluation = self.evaluator_agent.evaluate_spec(spec, prompt)
            
            score = evaluation.score
        except Exception as e:
            success = False
            print(f"Test failed: {e}")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return {
            'execution_time': execution_time,
            'success': success,
            'score': score
        }
    
    def run_concurrent_tests(self, prompts: List[str], mode: str = 'universal', 
                           max_workers: int = 5) -> List[Dict[str, Any]]:
        """Run concurrent benchmark tests"""
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_prompt = {
                executor.submit(self.run_single_test, prompt, mode): prompt 
                for prompt in prompts
            }
            
            for future in concurrent.futures.as_completed(future_to_prompt):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Concurrent test failed: {e}")
                    results.append({
                        'execution_time': 0,
                        'success': False,
                        'score': 0
                    })
        
        return results
    
    def calculate_benchmark_stats(self, results: List[Dict[str, Any]], 
                                test_name: str) -> BenchmarkResult:
        """Calculate benchmark statistics"""
        execution_times = [r['execution_time'] for r in results]
        successes = [r['success'] for r in results]
        scores = [r['score'] for r in results if r['success']]
        
        total_time = sum(execution_times)
        avg_time = statistics.mean(execution_times) if execution_times else 0
        min_time = min(execution_times) if execution_times else 0
        max_time = max(execution_times) if execution_times else 0
        success_rate = (sum(successes) / len(successes)) * 100 if successes else 0
        throughput = len(results) / total_time if total_time > 0 else 0
        avg_score = statistics.mean(scores) if scores else 0
        
        return BenchmarkResult(
            test_name=test_name,
            total_time=total_time,
            avg_time=avg_time,
            min_time=min_time,
            max_time=max_time,
            success_rate=success_rate,
            throughput=throughput,
            avg_score=avg_score,
            memory_usage=0  # Could add memory monitoring
        )
    
    def run_stress_test(self, duration_seconds: int = 60) -> Dict[str, Any]:
        """Run stress test for specified duration"""
        print(f"🔥 Running stress test for {duration_seconds} seconds...")
        
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        results = []
        test_count = 0
        
        while time.time() < end_time:
            # Rotate through different prompt types
            prompt_type = list(self.test_prompts.keys())[test_count % len(self.test_prompts)]
            prompts = self.test_prompts[prompt_type]
            prompt = prompts[test_count % len(prompts)]
            
            result = self.run_single_test(prompt, 'universal')
            results.append(result)
            test_count += 1
        
        return {
            'duration': duration_seconds,
            'total_tests': test_count,
            'results': results,
            'stats': self.calculate_benchmark_stats(results, 'stress_test')
        }
    
    def run_full_benchmark(self) -> Dict[str, Any]:
        """Run comprehensive benchmark suite"""
        print("🚀 Starting comprehensive benchmark suite...")
        
        benchmark_results = {}
        
        # Test each prompt type
        for prompt_type, prompts in self.test_prompts.items():
            print(f"📊 Testing {prompt_type} prompts...")
            
            # Sequential tests
            sequential_results = []
            for prompt in prompts:
                result = self.run_single_test(prompt, 'universal')
                sequential_results.append(result)
            
            benchmark_results[f'{prompt_type}_sequential'] = self.calculate_benchmark_stats(
                sequential_results, f'{prompt_type}_sequential'
            )
            
            # Concurrent tests
            concurrent_results = self.run_concurrent_tests(prompts, 'universal', 3)
            benchmark_results[f'{prompt_type}_concurrent'] = self.calculate_benchmark_stats(
                concurrent_results, f'{prompt_type}_concurrent'
            )
        
        # RL benchmark
        print("🤖 Testing RL performance...")
        rl_results = []
        for prompt in self.test_prompts['building'][:3]:  # Limited for time
            start_time = time.time()
            try:
                rl_loop = RLLoop(max_iterations=2)
                rl_result = rl_loop.run_training_loop(prompt)
                final_score = rl_result['iterations'][-1]['evaluation']['score'] if rl_result['iterations'] else 0
                
                rl_results.append({
                    'execution_time': time.time() - start_time,
                    'success': True,
                    'score': final_score
                })
            except Exception as e:
                rl_results.append({
                    'execution_time': time.time() - start_time,
                    'success': False,
                    'score': 0
                })
        
        benchmark_results['rl_training'] = self.calculate_benchmark_stats(
            rl_results, 'rl_training'
        )
        
        return benchmark_results
    
    def print_results(self, results: Dict[str, Any]):
        """Print formatted benchmark results"""
        print("\n" + "="*80)
        print("🎯 BENCHMARK RESULTS")
        print("="*80)
        
        for test_name, result in results.items():
            if isinstance(result, BenchmarkResult):
                print(f"\n📈 {test_name.upper()}")
                print(f"   Success Rate: {result.success_rate:.1f}%")
                print(f"   Avg Time: {result.avg_time:.3f}s")
                print(f"   Throughput: {result.throughput:.2f} ops/sec")
                print(f"   Avg Score: {result.avg_score:.1f}/100")
                print(f"   Range: {result.min_time:.3f}s - {result.max_time:.3f}s")

def main():
    """Run benchmark suite"""
    suite = BenchmarkSuite()
    
    # Run full benchmark
    results = suite.run_full_benchmark()
    suite.print_results(results)
    
    # Run stress test
    stress_results = suite.run_stress_test(30)  # 30 second stress test
    print(f"\n🔥 STRESS TEST RESULTS")
    print(f"   Duration: {stress_results['duration']}s")
    print(f"   Total Tests: {stress_results['total_tests']}")
    suite.print_results({'stress_test': stress_results['stats']})

if __name__ == "__main__":
    main()