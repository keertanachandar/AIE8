# model_registry.py - Simplified 3-model system

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

class ModelTier(Enum):
    """Simple model tiers"""
    PREMIUM = "premium"      # Best quality, highest cost
    STANDARD = "standard"    # Balanced performance
    EFFICIENT = "efficient"  # Fast and economical

@dataclass
class ModelSpec:
    """Specification for a Claude model"""
    model_id: str
    name: str
    short_name: str
    tier: ModelTier
    max_tokens: int
    context_window: int
    
    # Pricing per million tokens
    input_cost: float
    output_cost: float
    
    # Simple characteristics
    speed: str
    quality: str
    best_for: List[str]
    description: str

class ModelRegistry:
    """Registry of 3 available Claude models"""
    
    # The 3 models we offer
    OPUS = ModelSpec(
        model_id="claude-opus-4-20250514",
        name="Claude Opus 4",
        short_name="opus",
        tier=ModelTier.PREMIUM,
        max_tokens=16384,
        context_window=200000,
        input_cost=15.00,
        output_cost=75.00,
        speed="medium",
        quality="highest",
        best_for=[
            "Complex research requiring deep reasoning",
            "Critical analysis and decision-making",
            "Final reports where quality matters most"
        ],
        description="🏆 Highest quality - Use for complex analysis and final outputs"
    )
    
    SONNET = ModelSpec(
        model_id="claude-sonnet-4-20250514",
        name="Claude Sonnet 4.5",
        short_name="sonnet",
        tier=ModelTier.STANDARD,
        max_tokens=16384,
        context_window=200000,
        input_cost=3.00,
        output_cost=15.00,
        speed="fast",
        quality="high",
        best_for=[
            "Most research tasks and analysis",
            "General-purpose workflows",
            "Best balance of quality and cost"
        ],
        description="⚖️  Balanced - Recommended for most tasks (default)"
    )
    
    HAIKU = ModelSpec(
        model_id="claude-haiku-4-20250514",
        name="Claude Haiku 4",
        short_name="haiku",
        tier=ModelTier.EFFICIENT,
        max_tokens=8192,
        context_window=200000,
        input_cost=0.80,
        output_cost=4.00,
        speed="fastest",
        quality="good",
        best_for=[
            "Quick summaries and extraction",
            "High-volume processing",
            "Cost-sensitive workflows"
        ],
        description="⚡ Fast & economical - Use for simple tasks and summaries"
    )
    
    @classmethod
    def get_all_models(cls) -> Dict[str, ModelSpec]:
        """Get all 3 models"""
        return {
            "opus": cls.OPUS,
            "sonnet": cls.SONNET,
            "haiku": cls.HAIKU
        }
    
    @classmethod
    def get_model(cls, name: str) -> Optional[ModelSpec]:
        """Get model by name (opus, sonnet, or haiku)"""
        models = cls.get_all_models()
        return models.get(name.lower())
    
    @classmethod
    def get_default(cls) -> ModelSpec:
        """Get default model (Sonnet)"""
        return cls.SONNET
    
    @classmethod
    def print_all_models(cls):
        """Print information about all 3 models"""
        print("\n" + "="*70)
        print("AVAILABLE MODELS")
        print("="*70)
        
        for name, model in cls.get_all_models().items():
            print(f"\n{model.description}")
            print(f"Name:      {model.name}")
            print(f"Speed:     {model.speed}")
            print(f"Quality:   {model.quality}")
            print(f"Cost:      ${model.input_cost}/M input, ${model.output_cost}/M output")
            print(f"Best for:")
            for use in model.best_for:
                print(f"  • {use}")
        
        print("="*70 + "\n")
    