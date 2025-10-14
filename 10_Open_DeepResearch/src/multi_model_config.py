# multi_model_config.py - Simple 3-model configuration

from typing import Optional
from dataclasses import dataclass
from model_registry import ModelRegistry, ModelSpec

@dataclass
class MultiModelConfig:
    """Simple configuration - choose one of 3 models per stage"""
    
    # Model assignments (must be: "opus", "sonnet", or "haiku")
    clarification_model: str = "haiku"        # Fast clarification
    research_brief_model: str = "sonnet"      # Planning
    research_model: str = "sonnet"            # Main research
    supervisor_model: str = "sonnet"          # Coordination
    compression_model: str = "haiku"          # Fast compression
    summarization_model: str = "haiku"        # Fast summaries
    final_report_model: str = "opus"          # Best quality report
    
    # Budget controls
    total_cost_budget: Optional[float] = None

class MultiModelManager:
    """Manage the 3 models across workflow stages"""
    
    def __init__(self, config: Optional[MultiModelConfig] = None):
        self.config = config or MultiModelConfig()
        self.registry = ModelRegistry()
        
        # Validate all model names
        self._validate_config()
        
        # Track costs
        self.total_cost = 0.0
        self.stage_costs = {}
        self.model_usage = {"opus": 0, "sonnet": 0, "haiku": 0}
    
    def _validate_config(self):
        """Ensure all model names are valid"""
        valid_models = {"opus", "sonnet", "haiku"}
        
        for field in [
            "clarification_model", "research_brief_model", "research_model",
            "supervisor_model", "compression_model", "summarization_model",
            "final_report_model"
        ]:
            model_name = getattr(self.config, field)
            if model_name not in valid_models:
                raise ValueError(
                    f"Invalid model '{model_name}' for {field}. "
                    f"Must be one of: {valid_models}"
                )
    
    def get_model_for_stage(self, stage: str) -> ModelSpec:
        """Get model for a workflow stage"""
        stage_map = {
            "clarification": self.config.clarification_model,
            "research_brief": self.config.research_brief_model,
            "research": self.config.research_model,
            "supervisor": self.config.supervisor_model,
            "compression": self.config.compression_model,
            "summarization": self.config.summarization_model,
            "final_report": self.config.final_report_model
        }
        
        model_name = stage_map.get(stage, "sonnet")
        return self.registry.get_model(model_name)
    
    def record_usage(self, stage: str, model_name: str, cost: float, tokens: int):
        """Record model usage"""
        # Track by stage
        if stage not in self.stage_costs:
            self.stage_costs[stage] = {"cost": 0, "tokens": 0}
        self.stage_costs[stage]["cost"] += cost
        self.stage_costs[stage]["tokens"] += tokens
        
        # Track by model
        self.model_usage[model_name] += 1
        
        # Track total
        self.total_cost += cost
    
    def check_budget(self, estimated_cost: float) -> tuple[bool, str]:
        """Check if next operation is within budget"""
        if not self.config.total_cost_budget:
            return True, "No budget limit set"
        
        projected_total = self.total_cost + estimated_cost
        if projected_total > self.config.total_cost_budget:
            return False, (
                f"Budget exceeded: ${projected_total:.2f} > "
                f"${self.config.total_cost_budget:.2f}"
            )
        
        return True, f"Within budget (${projected_total:.2f}/${self.config.total_cost_budget:.2f})"
    
    def get_cost_summary(self) -> dict:
        """Get cost breakdown"""
        return {
            "total_cost": self.total_cost,
            "by_stage": {
                stage: {
                    "cost": data["cost"],
                    "tokens": data["tokens"],
                    "percentage": (data["cost"] / self.total_cost * 100) if self.total_cost > 0 else 0
                }
                for stage, data in self.stage_costs.items()
            },
            "by_model": self.model_usage,
            "budget": {
                "limit": self.config.total_cost_budget,
                "used": self.total_cost,
                "remaining": (
                    self.config.total_cost_budget - self.total_cost
                    if self.config.total_cost_budget else None
                ),
                "percentage_used": (
                    (self.total_cost / self.config.total_cost_budget * 100)
                    if self.config.total_cost_budget else None
                )
            }
        }
    
    def print_configuration(self):
        """Print current model configuration"""
        print("\n" + "="*70)
        print("RESEARCH WORKFLOW - MODEL CONFIGURATION")
        print("="*70)
        print("\nStage Assignments:")
        print(f"  📋 Clarification:    {self.config.clarification_model.upper():8s} (fast initial questions)")
        print(f"  📝 Research Brief:   {self.config.research_brief_model.upper():8s} (planning)")
        print(f"  🔍 Research:         {self.config.research_model.upper():8s} (main analysis)")
        print(f"  👔 Supervisor:       {self.config.supervisor_model.upper():8s} (coordination)")
        print(f"  📦 Compression:      {self.config.compression_model.upper():8s} (data reduction)")
        print(f"  📊 Summarization:    {self.config.summarization_model.upper():8s} (summaries)")
        print(f"  📄 Final Report:     {self.config.final_report_model.upper():8s} (final output)")
        
        if self.config.total_cost_budget:
            print(f"\n💰 Budget Limit: ${self.config.total_cost_budget:.2f}")
        
        print("="*70 + "\n")
    
    def print_cost_summary(self):
        """Print detailed cost breakdown"""
        summary = self.get_cost_summary()
        
        print("\n" + "="*70)
        print("COST SUMMARY")
        print("="*70)
        print(f"\n💵 Total Cost: ${summary['total_cost']:.4f}")
        
        if summary['by_stage']:
            print("\n📊 By Stage:")
            for stage, data in sorted(
                summary['by_stage'].items(),
                key=lambda x: x[1]['cost'],
                reverse=True
            ):
                print(
                    f"  {stage:20s} ${data['cost']:8.4f} "
                    f"({data['percentage']:5.1f}%)  "
                    f"[{data['tokens']:,} tokens]"
                )
        
        print("\n🤖 Model Usage Count:")
        total_calls = sum(summary['by_model'].values())
        for model, count in sorted(summary['by_model'].items(), key=lambda x: x[1], reverse=True):
            pct = (count / total_calls * 100) if total_calls > 0 else 0
            print(f"  {model.upper():8s} {count:4d} calls ({pct:5.1f}%)")
        
        if summary['budget']['limit']:
            print("\n💰 Budget Status:")
            print(f"  Limit:      ${summary['budget']['limit']:.2f}")
            print(f"  Used:       ${summary['budget']['used']:.4f}")
            print(f"  Remaining:  ${summary['budget']['remaining']:.4f}")
            print(f"  Utilized:   {summary['budget']['percentage_used']:.1f}%")
        
        print("="*70 + "\n")