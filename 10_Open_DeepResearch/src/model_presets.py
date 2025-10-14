# model_presets.py - 3 simple preset configurations

from multi_model_config import MultiModelConfig

class ModelPresets:
    """3 preset configurations to choose from"""
    
    # Preset 1: QUALITY FIRST - Use Opus for critical stages
    QUALITY = MultiModelConfig(
        clarification_model="haiku",      # Fast questions
        research_brief_model="sonnet",    # Good planning
        research_model="opus",            # 🏆 Best research
        supervisor_model="sonnet",        # Good coordination
        compression_model="haiku",        # Fast compression
        summarization_model="haiku",      # Fast summaries
        final_report_model="opus",        # 🏆 Best final output
        total_cost_budget=50.0            # Higher budget
    )
    
    # Preset 2: BALANCED - Mix of all 3 (RECOMMENDED)
    BALANCED = MultiModelConfig(
        clarification_model="haiku",      # ⚡ Fast questions
        research_brief_model="sonnet",    # ⚖️  Good planning
        research_model="sonnet",          # ⚖️  Main workhorse
        supervisor_model="sonnet",        # ⚖️  Coordination
        compression_model="haiku",        # ⚡ Fast compression
        summarization_model="haiku",      # ⚡ Fast summaries
        final_report_model="opus",        # 🏆 Best final output
        total_cost_budget=25.0            # Moderate budget
    )
    
    # Preset 3: ECONOMICAL - Minimize costs
    ECONOMICAL = MultiModelConfig(
        clarification_model="haiku",      # ⚡ Fast questions
        research_brief_model="haiku",     # ⚡ Fast planning
        research_model="sonnet",          # ⚖️  Adequate research
        supervisor_model="haiku",         # ⚡ Fast coordination
        compression_model="haiku",        # ⚡ Fast compression
        summarization_model="haiku",      # ⚡ Fast summaries
        final_report_model="sonnet",      # ⚖️  Good final output
        total_cost_budget=10.0            # Lower budget
    )
    
    @classmethod
    def get_preset(cls, name: str) -> MultiModelConfig:
        """Get preset by name"""
        presets = {
            "quality": cls.QUALITY,
            "balanced": cls.BALANCED,
            "economical": cls.ECONOMICAL,
            "eco": cls.ECONOMICAL,  # Alias
            "default": cls.BALANCED  # Default
        }
        return presets.get(name.lower(), cls.BALANCED)
    
    @classmethod
    def print_presets(cls):
        """Print all available presets"""
        print("\n" + "="*70)
        print("AVAILABLE PRESETS")
        print("="*70)
        
        print("\n🏆 QUALITY - Best results, higher cost")
        print("   Research: Opus | Final Report: Opus")
        print("   Budget: $50")
        print("   Use when: Quality matters most, complex research")
        
        print("\n⚖️  BALANCED - Recommended for most users (DEFAULT)")
        print("   Research: Sonnet | Final Report: Opus")
        print("   Budget: $25")
        print("   Use when: Standard research tasks, good balance")
        
        print("\n⚡ ECONOMICAL - Minimize costs")
        print("   Research: Sonnet | Final Report: Sonnet")
        print("   Budget: $10")
        print("   Use when: Budget-conscious, simpler tasks")
        
        print("="*70 + "\n")