# model_strategy.py - Intelligent model selection strategies

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
from model_registry import ModelRegistry, ModelSpec, ModelTier

class TaskComplexity(Enum):
    """Complexity levels for tasks"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    CRITICAL = "critical"

class ModelSelectionStrategy(Enum):
    """Strategies for selecting models"""
    COST_OPTIMIZED = "cost_optimized"        # Minimize cost
    QUALITY_FIRST = "quality_first"          # Maximize quality
    SPEED_OPTIMIZED = "speed_optimized"      # Maximize speed
    BALANCED = "balanced"                     # Balance all factors
    ADAPTIVE = "adaptive"                     # Adapt to task
    CASCADING = "cascading"                   # Try cheaper first, upgrade if needed

@dataclass
class TaskProfile:
    """Profile of a research task"""
    name: str
    complexity: TaskComplexity
    requires_reasoning: bool = False
    requires_creativity: bool = False
    token_budget: Optional[int] = None
    cost_budget: Optional[float] = None
    time_sensitive: bool = False

class ModelSelector:
    """Intelligent model selection based on task requirements"""
    
    def __init__(self, strategy: ModelSelectionStrategy = ModelSelectionStrategy.BALANCED):
        self.strategy = strategy
        self.registry = ModelRegistry()
        self.usage_history = []
    
    def select_model(
        self,
        task_profile: TaskProfile,
        available_models: Optional[List[str]] = None
    ) -> ModelSpec:
        """Select best model for a task"""
        
        if available_models:
            models = [
                self.registry.get_model(name) 
                for name in available_models
            ]
            models = [m for m in models if m is not None]
        else:
            models = list(self.registry.get_all_models().values())
        
        if not models:
            return self.registry.SONNET_4_5  # Fallback
        
        if self.strategy == ModelSelectionStrategy.COST_OPTIMIZED:
            return self._select_cost_optimized(task_profile, models)
        elif self.strategy == ModelSelectionStrategy.QUALITY_FIRST:
            return self._select_quality_first(task_profile, models)
        elif self.strategy == ModelSelectionStrategy.SPEED_OPTIMIZED:
            return self._select_speed_optimized(task_profile, models)
        elif self.strategy == ModelSelectionStrategy.ADAPTIVE:
            return self._select_adaptive(task_profile, models)
        else:  # BALANCED
            return self._select_balanced(task_profile, models)
    
    def _select_cost_optimized(
        self,
        task_profile: TaskProfile,
        models: List[ModelSpec]
    ) -> ModelSpec:
        """Select cheapest model that meets requirements"""
        
        # Filter by complexity requirements
        if task_profile.complexity == TaskComplexity.CRITICAL:
            models = [m for m in models if m.tier in [ModelTier.FLAGSHIP, ModelTier.PREMIUM]]
        elif task_profile.complexity == TaskComplexity.COMPLEX:
            models = [m for m in models if m.tier != ModelTier.EFFICIENT]
        
        # Return cheapest
        return min(models, key=lambda m: m.output_cost)
    
    def _select_quality_first(
        self,
        task_profile: TaskProfile,
        models: List[ModelSpec]
    ) -> ModelSpec:
        """Select highest quality model"""
        quality_rank = {"highest": 0, "high": 1, "good": 2, "standard": 3}
        return min(models, key=lambda m: quality_rank.get(m.quality, 3))
    
    def _select_speed_optimized(
        self,
        task_profile: TaskProfile,
        models: List[ModelSpec]
    ) -> ModelSpec:
        """Select fastest model that meets requirements"""
        
        # Filter by complexity
        if task_profile.complexity in [TaskComplexity.CRITICAL, TaskComplexity.COMPLEX]:
            models = [m for m in models if m.quality in ["highest", "high"]]
        
        # Return fastest
        speed_rank = {"fast": 0, "medium": 1, "slow": 2}
        return min(models, key=lambda m: speed_rank.get(m.speed, 1))
    
    def _select_adaptive(
        self,
        task_profile: TaskProfile,
        models: List[ModelSpec]
    ) -> ModelSpec:
        """Adaptively select based on task characteristics"""
        
        # Critical tasks -> Opus
        if task_profile.complexity == TaskComplexity.CRITICAL:
            return self.registry.OPUS_4
        
        # Complex reasoning -> Sonnet 4.5
        if task_profile.requires_reasoning or task_profile.complexity == TaskComplexity.COMPLEX:
            return self.registry.SONNET_4_5
        
        # Simple tasks or high volume -> Haiku
        if task_profile.complexity == TaskComplexity.SIMPLE or task_profile.time_sensitive:
            return self.registry.HAIKU_4
        
        # Default to Sonnet 4.5
        return self.registry.SONNET_4_5
    
    def _select_balanced(
        self,
        task_profile: TaskProfile,
        models: List[ModelSpec]
    ) -> ModelSpec:
        """Balance quality, speed, and cost"""
        
        # Score each model
        scores = {}
        for model in models:
            score = 0
            
            # Quality score (0-3)
            quality_scores = {"highest": 3, "high": 2, "good": 1, "standard": 0}
            score += quality_scores.get(model.quality, 1) * 2
            
            # Speed score (0-3)
            speed_scores = {"fast": 3, "medium": 2, "slow": 1}
            score += speed_scores.get(model.speed, 2)
            
            # Cost score (inverse - cheaper is better)
            max_cost = max(m.output_cost for m in models)
            cost_score = 3 * (1 - model.output_cost / max_cost)
            score += cost_score
            
            # Adjust for task requirements
            if task_profile.complexity in [TaskComplexity.CRITICAL, TaskComplexity.COMPLEX]:
                if model.tier in [ModelTier.FLAGSHIP, ModelTier.PREMIUM]:
                    score += 2
            
            scores[model.model_id] = score
        
        # Return highest scoring
        best_model_id = max(scores, key=scores.get)
        return next(m for m in models if m.model_id == best_model_id)
    
    def record_usage(self, model: ModelSpec, success: bool, cost: float, duration: float):
        """Record model usage for learning"""
        self.usage_history.append({
            "model": model.model_id,
            "success": success,
            "cost": cost,
            "duration": duration,
            "timestamp": datetime.now()
        })
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get model usage statistics"""
        if not self.usage_history:
            return {"message": "No usage data yet"}
        
        stats = {}
        for entry in self.usage_history:
            model_id = entry["model"]
            if model_id not in stats:
                stats[model_id] = {
                    "count": 0,
                    "total_cost": 0,
                    "total_duration": 0,
                    "successes": 0
                }
            
            stats[model_id]["count"] += 1
            stats[model_id]["total_cost"] += entry["cost"]
            stats[model_id]["total_duration"] += entry["duration"]
            if entry["success"]:
                stats[model_id]["successes"] += 1
        
        # Calculate averages
        for model_id in stats:
            count = stats[model_id]["count"]
            stats[model_id]["avg_cost"] = stats[model_id]["total_cost"] / count
            stats[model_id]["avg_duration"] = stats[model_id]["total_duration"] / count
            stats[model_id]["success_rate"] = stats[model_id]["successes"] / count
        
        return stats