# quick_setup.py - Easy setup functions for different scenarios

from integrated_config import IntegratedResearchConfig
from prompts import ResearchType
from rate_limiter import RateLimitConfig

class QuickSetup:
    """Quick setup functions for common scenarios"""
    
    @staticmethod
    def academic_research(
        model_preset: str = "quality",
        budget: float = 50.0
    ) -> IntegratedResearchConfig:
        """
        Setup for academic research
        - Uses highest quality models
        - Focus on rigorous analysis
        """
        rate_config = RateLimitConfig(
            requests_per_minute=30,
            tokens_per_minute=50_000,
            cost_limit_per_hour=10.0,
            cost_limit_per_day=budget
        )
        
        config = IntegratedResearchConfig(
            research_type=ResearchType.ACADEMIC,
            model_preset=model_preset,
            rate_limit_config=rate_config,
            max_iterations=3,
            max_tool_calls=5
        )
        
        print("🎓 Academic Research Configuration")
        config.print_configuration()
        return config
    
    @staticmethod
    def market_research(
        model_preset: str = "balanced",
        budget: float = 25.0
    ) -> IntegratedResearchConfig:
        """
        Setup for market research
        - Balanced quality and cost
        - Focus on market intelligence
        """
        rate_config = RateLimitConfig(
            requests_per_minute=40,
            tokens_per_minute=75_000,
            cost_limit_per_hour=7.0,
            cost_limit_per_day=budget
        )
        
        config = IntegratedResearchConfig(
            research_type=ResearchType.MARKET,
            model_preset=model_preset,
            rate_limit_config=rate_config,
            max_iterations=2,
            max_tool_calls=5
        )
        
        print("📊 Market Research Configuration")
        config.print_configuration()
        return config
    
    @staticmethod
    def user_research(
        model_preset: str = "balanced",
        budget: float = 20.0
    ) -> IntegratedResearchConfig:
        """
        Setup for user research
        - Balanced approach
        - Focus on user insights
        """
        rate_config = RateLimitConfig(
            requests_per_minute=35,
            tokens_per_minute=60_000,
            cost_limit_per_hour=5.0,
            cost_limit_per_day=budget
        )
        
        config = IntegratedResearchConfig(
            research_type=ResearchType.USER_RESEARCH,
            model_preset=model_preset,
            rate_limit_config=rate_config,
            max_iterations=2,
            max_tool_calls=5
        )
        
        print("👥 User Research Configuration")
        config.print_configuration()
        return config
    
    @staticmethod
    def technical_research(
        model_preset: str = "quality",
        budget: float = 40.0
    ) -> IntegratedResearchConfig:
        """
        Setup for technical research
        - High quality for accuracy
        - Focus on technical analysis
        """
        rate_config = RateLimitConfig(
            requests_per_minute=25,
            tokens_per_minute=50_000,
            cost_limit_per_hour=8.0,
            cost_limit_per_day=budget
        )
        
        config = IntegratedResearchConfig(
            research_type=ResearchType.TECHNICAL,
            model_preset=model_preset,
            rate_limit_config=rate_config,
            max_iterations=3,
            max_tool_calls=6
        )
        
        print("🔧 Technical Research Configuration")
        config.print_configuration()
        return config
    
    @staticmethod
    def data_analysis(
        model_preset: str = "balanced",
        budget: float = 15.0
    ) -> IntegratedResearchConfig:
        """
        Setup for data analysis
        - Economical for data processing
        - Focus on extracting insights
        """
        rate_config = RateLimitConfig(
            requests_per_minute=50,
            tokens_per_minute=100_000,
            cost_limit_per_hour=4.0,
            cost_limit_per_day=budget
        )
        
        config = IntegratedResearchConfig(
            research_type=ResearchType.DATA_ANALYSIS,
            model_preset=model_preset,
            rate_limit_config=rate_config,
            max_iterations=2,
            max_tool_calls=7
        )
        
        print("📈 Data Analysis Configuration")
        config.print_configuration()
        return config
    
    @staticmethod
    def quick_summary(
        model_preset: str = "economical",
        budget: float = 5.0
    ) -> IntegratedResearchConfig:
        """
        Setup for quick summaries
        - Most economical
        - Fast processing
        """
        rate_config = RateLimitConfig(
            requests_per_minute=60,
            tokens_per_minute=150_000,
            cost_limit_per_hour=2.0,
            cost_limit_per_day=budget
        )
        
        config = IntegratedResearchConfig(
            research_type=ResearchType.LITERATURE_REVIEW,
            model_preset=model_preset,
            rate_limit_config=rate_config,
            max_iterations=1,
            max_tool_calls=3
        )
        
        print("⚡ Quick Summary Configuration")
        config.print_configuration()
        return config
    
    @staticmethod
    def custom(
        research_type: ResearchType,
        model_preset: str = "balanced",
        budget: float = 25.0,
        requests_per_min: int = 30,
        tokens_per_min: int = 50_000
    ) -> IntegratedResearchConfig:
        """
        Custom configuration
        - Full control over all parameters
        """
        rate_config = RateLimitConfig(
            requests_per_minute=requests_per_min,
            tokens_per_minute=tokens_per_min,
            cost_limit_per_hour=budget / 5,  # 1/5 of daily budget per hour
            cost_limit_per_day=budget
        )
        
        config = IntegratedResearchConfig(
            research_type=research_type,
            model_preset=model_preset,
            rate_limit_config=rate_config
        )
        
        print("⚙️  Custom Configuration")
        config.print_configuration()
        return config