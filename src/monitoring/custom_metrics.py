"""Custom business metrics for advanced monitoring"""

from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry
import time
from functools import wraps

# Custom registry for business metrics
business_registry = CollectorRegistry()

# Business Metrics
spec_generation_counter = Counter(
    'spec_generations_total',
    'Total number of specifications generated',
    ['agent_type', 'success'],
    registry=business_registry
)

evaluation_score_histogram = Histogram(
    'evaluation_scores',
    'Distribution of evaluation scores',
    buckets=[0, 2, 4, 6, 8, 10],
    registry=business_registry
)

rl_training_duration = Histogram(
    'rl_training_duration_seconds',
    'Time taken for RL training sessions',
    ['iterations'],
    registry=business_registry
)

active_sessions_gauge = Gauge(
    'active_sessions_current',
    'Current number of active user sessions',
    registry=business_registry
)

agent_response_time = Histogram(
    'agent_response_time_seconds',
    'Response time for each agent',
    ['agent_name'],
    registry=business_registry
)

def track_generation(agent_type='MainAgent'):
    """Decorator to track spec generation metrics"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                spec_generation_counter.labels(agent_type=agent_type, success='true').inc()
                return result
            except Exception as e:
                spec_generation_counter.labels(agent_type=agent_type, success='false').inc()
                raise
            finally:
                duration = time.time() - start_time
                agent_response_time.labels(agent_name=agent_type).observe(duration)
        return wrapper
    return decorator

def track_evaluation_score(score: float):
    """Track evaluation score distribution"""
    evaluation_score_histogram.observe(score)

def track_rl_training(iterations: int, duration: float):
    """Track RL training metrics"""
    rl_training_duration.labels(iterations=str(iterations)).observe(duration)

def update_active_sessions(count: int):
    """Update active sessions count"""
    active_sessions_gauge.set(count)

def get_business_metrics():
    """Get all business metrics in Prometheus format"""
    from prometheus_client import generate_latest
    return generate_latest(business_registry)
