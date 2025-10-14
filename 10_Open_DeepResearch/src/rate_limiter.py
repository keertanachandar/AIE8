# rate_limiter.py - Rate limiting and cost control

import time
import asyncio
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import threading

@dataclass
class RateLimitConfig:
    """Configuration for rate limiting"""
    requests_per_minute: int = 50
    tokens_per_minute: int = 100_000
    cost_limit_per_hour: float = 10.0  # USD
    cost_limit_per_day: float = 100.0  # USD
    max_retries: int = 3
    backoff_factor: float = 2.0
    initial_retry_delay: float = 1.0

@dataclass
class TokenBucket:
    """Token bucket for rate limiting"""
    capacity: int
    refill_rate: float  # tokens per second
    tokens: float = field(init=False)
    last_refill: float = field(init=False)
    
    def __post_init__(self):
        self.tokens = float(self.capacity)
        self.last_refill = time.time()
    
    def _refill(self):
        """Refill tokens based on time elapsed"""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(
            self.capacity,
            self.tokens + (elapsed * self.refill_rate)
        )
        self.last_refill = now
    
    def consume(self, tokens: int) -> bool:
        """Try to consume tokens"""
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def wait_time(self, tokens: int) -> float:
        """Calculate wait time for tokens"""
        self._refill()
        if self.tokens >= tokens:
            return 0.0
        needed = tokens - self.tokens
        return needed / self.refill_rate

@dataclass
class CostTracker:
    """Track API costs"""
    hourly_limit: float
    daily_limit: float
    hourly_costs: deque = field(default_factory=lambda: deque(maxlen=60))
    daily_costs: deque = field(default_factory=lambda: deque(maxlen=24))
    total_cost: float = 0.0
    
    def add_cost(self, cost: float):
        """Add a cost entry"""
        now = datetime.now()
        self.total_cost += cost
        self.hourly_costs.append((now, cost))
        self.daily_costs.append((now, cost))
        self._cleanup_old_entries()
    
    def _cleanup_old_entries(self):
        """Remove old cost entries"""
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        
        # Clean hourly
        while self.hourly_costs and self.hourly_costs[0][0] < hour_ago:
            self.hourly_costs.popleft()
        
        # Clean daily
        while self.daily_costs and self.daily_costs[0][0] < day_ago:
            self.daily_costs.popleft()
    
    def get_hourly_cost(self) -> float:
        """Get cost in last hour"""
        self._cleanup_old_entries()
        return sum(cost for _, cost in self.hourly_costs)
    
    def get_daily_cost(self) -> float:
        """Get cost in last 24 hours"""
        self._cleanup_old_entries()
        return sum(cost for _, cost in self.daily_costs)
    
    def check_limits(self) -> tuple[bool, str]:
        """Check if within cost limits"""
        hourly = self.get_hourly_cost()
        daily = self.get_daily_cost()
        
        if hourly >= self.hourly_limit:
            return False, f"Hourly cost limit reached: ${hourly:.2f}/${self.hourly_limit:.2f}"
        
        if daily >= self.daily_limit:
            return False, f"Daily cost limit reached: ${daily:.2f}/${self.daily_limit:.2f}"
        
        return True, "Within limits"

class RateLimiter:
    """Comprehensive rate limiter with cost control"""
    
    # Anthropic pricing (as of 2025)
    MODEL_COSTS = {
        "claude-sonnet-4-20250514": {
            "input": 3.00 / 1_000_000,   # $3 per MTok
            "output": 15.00 / 1_000_000   # $15 per MTok
        },
        "claude-opus-4-20250514": {
            "input": 15.00 / 1_000_000,   # $15 per MTok
            "output": 75.00 / 1_000_000   # $75 per MTok
        }
    }
    
    def __init__(self, config: Optional[RateLimitConfig] = None, logger=None):
        self.config = config or RateLimitConfig()
        self.logger = logger
        
        # Token buckets
        self.request_bucket = TokenBucket(
            capacity=self.config.requests_per_minute,
            refill_rate=self.config.requests_per_minute / 60.0
        )
        
        self.token_bucket = TokenBucket(
            capacity=self.config.tokens_per_minute,
            refill_rate=self.config.tokens_per_minute / 60.0
        )
        
        # Cost tracker
        self.cost_tracker = CostTracker(
            hourly_limit=self.config.cost_limit_per_hour,
            daily_limit=self.config.cost_limit_per_day
        )
        
        # Metrics
        self.metrics = {
            "total_requests": 0,
            "rate_limited": 0,
            "cost_limited": 0,
            "retries": 0
        }
        
        self._lock = threading.Lock()
    
    def calculate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calculate cost for API call"""
        if model not in self.MODEL_COSTS:
            # Default to Sonnet pricing if model unknown
            model = "claude-sonnet-4-20250514"
        
        pricing = self.MODEL_COSTS[model]
        cost = (
            input_tokens * pricing["input"] +
            output_tokens * pricing["output"]
        )
        return cost
    
    async def acquire(
        self,
        estimated_tokens: int = 1000,
        model: str = "claude-sonnet-4-20250514"
    ) -> Dict[str, Any]:
        """
        Acquire permission to make API call
        
        Returns:
            Dict with 'allowed' boolean and metadata
        """
        with self._lock:
            self.metrics["total_requests"] += 1
            
            # Check cost limits
            within_limits, limit_msg = self.cost_tracker.check_limits()
            if not within_limits:
                self.metrics["cost_limited"] += 1
                if self.logger:
                    self.logger.warning(f"Cost limit hit: {limit_msg}")
                return {
                    "allowed": False,
                    "reason": "cost_limit",
                    "message": limit_msg,
                    "retry_after": 3600  # 1 hour
                }
            
            # Check rate limits
            if not self.request_bucket.consume(1):
                wait_time = self.request_bucket.wait_time(1)
                self.metrics["rate_limited"] += 1
                if self.logger:
                    self.logger.warning(f"Request rate limit hit, wait {wait_time:.1f}s")
                return {
                    "allowed": False,
                    "reason": "rate_limit",
                    "message": f"Request rate limit, wait {wait_time:.1f}s",
                    "retry_after": wait_time
                }
            
            if not self.token_bucket.consume(estimated_tokens):
                wait_time = self.token_bucket.wait_time(estimated_tokens)
                self.metrics["rate_limited"] += 1
                if self.logger:
                    self.logger.warning(f"Token rate limit hit, wait {wait_time:.1f}s")
                return {
                    "allowed": False,
                    "reason": "token_rate_limit",
                    "message": f"Token rate limit, wait {wait_time:.1f}s",
                    "retry_after": wait_time
                }
            
            return {
                "allowed": True,
                "remaining_hourly_cost": self.config.cost_limit_per_hour - self.cost_tracker.get_hourly_cost(),
                "remaining_daily_cost": self.config.cost_limit_per_day - self.cost_tracker.get_daily_cost()
            }
    
    def record_usage(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ):
        """Record actual API usage"""
        cost = self.calculate_cost(model, input_tokens, output_tokens)
        with self._lock:
            self.cost_tracker.add_cost(cost)
        
        if self.logger:
            self.logger.info(
                f"Recorded usage: {input_tokens} in + {output_tokens} out = ${cost:.4f}"
            )
    
    async def with_retry(
        self,
        func,
        *args,
        **kwargs
    ):
        """Execute function with retry logic"""
        last_exception = None
        delay = self.config.initial_retry_delay
        
        for attempt in range(self.config.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                self.metrics["retries"] += 1
                
                if attempt < self.config.max_retries - 1:
                    if self.logger:
                        self.logger.warning(
                            f"Attempt {attempt + 1} failed, retrying in {delay}s: {str(e)}"
                        )
                    await asyncio.sleep(delay)
                    delay *= self.config.backoff_factor
        
        raise last_exception
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get rate limiter metrics"""
        return {
            **self.metrics,
            "current_hourly_cost": self.cost_tracker.get_hourly_cost(),
            "current_daily_cost": self.cost_tracker.get_daily_cost(),
            "total_cost": self.cost_tracker.total_cost,
            "hourly_limit": self.config.cost_limit_per_hour,
            "daily_limit": self.config.cost_limit_per_day
        }
    
    def print_status(self):
        """Print current rate limiter status"""
        metrics = self.get_metrics()
        print("\n" + "="*60)
        print("RATE LIMITER STATUS")
        print("="*60)
        print(f"Total Requests:     {metrics['total_requests']}")
        print(f"Rate Limited:       {metrics['rate_limited']}")
        print(f"Cost Limited:       {metrics['cost_limited']}")
        print(f"Retries:            {metrics['retries']}")
        print(f"\nCost Tracking:")
        print(f"  Hourly:  ${metrics['current_hourly_cost']:.2f} / ${metrics['hourly_limit']:.2f}")
        print(f"  Daily:   ${metrics['current_daily_cost']:.2f} / ${metrics['daily_limit']:.2f}")
        print(f"  Total:   ${metrics['total_cost']:.4f}")
        print("="*60 + "\n")