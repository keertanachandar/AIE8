# integrated_config_mcp.py - Configuration with MCP

from typing import Optional
import uuid
import asyncio
from tools_mcp import MCPResearchTools  # MCP version
from tools import ResearchTools  # Regular version
from model_presets import ModelPresets
from multi_model_config import MultiModelManager
from prompts import ResearchType, get_research_prompts
from research_logger import ResearchLogger
from error_handler import ErrorHandler
from rate_limiter import RateLimiter, RateLimitConfig

class IntegratedResearchConfig:
    """Configuration with optional MCP support"""
    
    def __init__(
        self,
        research_type: ResearchType = ResearchType.USER_RESEARCH,
        model_preset: str = "balanced",
        use_mcp: bool = False,  # Enable/disable MCP
        rate_limit_config: Optional[RateLimitConfig] = None,
        log_dir: str = "logs",
        max_iterations: int = 2,
        max_tool_calls: int = 5,
        max_concurrent_researchers: int = 10
    ):
        self.research_type = research_type
        self.use_mcp = use_mcp
        
        # Model setup
        self.model_config = ModelPresets.get_preset(model_preset)
        self.model_manager = MultiModelManager(self.model_config)
        
        # Prompts
        self.prompts = get_research_prompts(research_type)
        
        # Tools - MCP or regular
        if use_mcp:
            print("🔧 Initializing MCP tools...")
            self.tools = MCPResearchTools()
            # Note: MCP tools need async initialization
            # Call await self.tools.initialize_all() separately
        else:
            print("🔧 Using regular tools...")
            self.tools = ResearchTools()
        
        # Logging and controls
        self.logger = ResearchLogger(
            name=f"research_{research_type.value}",
            log_dir=log_dir
        )
        self.error_handler = ErrorHandler(self.logger.logger)
        self.rate_limiter = RateLimiter(
            config=rate_limit_config or RateLimitConfig(),
            logger=self.logger.logger
        )
        
        self.max_iterations = max_iterations
        self.max_tool_calls = max_tool_calls
        self.max_concurrent_researchers = max_concurrent_researchers
        self.thread_id = str(uuid.uuid4())
    
    async def initialize_mcp_tools(self):
        """Initialize MCP tools if enabled"""
        if self.use_mcp and isinstance(self.tools, MCPResearchTools):
            await self.tools.initialize_all()
            print(f"✓ MCP tools initialized: {len(self.tools.tools)} tools")
    
    def get_config_dict(self) -> dict:
        """Generate complete configuration dictionary"""
        
        research_model = self.model_manager.get_model_for_stage("research")
        compression_model = self.model_manager.get_model_for_stage("compression")
        final_report_model = self.model_manager.get_model_for_stage("final_report")
        summarization_model = self.model_manager.get_model_for_stage("summarization")
        
        return {
            "configurable": {
                "research_model": f"anthropic:{research_model.model_id}",
                "research_model_max_tokens": research_model.max_tokens,
                "compression_model": f"anthropic:{compression_model.model_id}",
                "compression_model_max_tokens": compression_model.max_tokens,
                "final_report_model": f"anthropic:{final_report_model.model_id}",
                "final_report_model_max_tokens": final_report_model.max_tokens,
                "summarization_model": f"anthropic:{summarization_model.model_id}",
                "summarization_model_max_tokens": summarization_model.max_tokens,
                
                "allow_clarification": True,
                "max_concurrent_research_units": self.max_concurrent_researchers,
                "max_researcher_iterations": self.max_iterations,
                "max_react_tool_calls": self.max_tool_calls,
                
                "search_api": "anthropic",
                "max_content_length": 50000,
                
                "custom_tools": self.tools.get_tool_definitions(),
                "tool_executor": getattr(self.tools, 'execute_tool', None),
                "enable_tools": True,
                "use_mcp": self.use_mcp,
                
                "research_type": self.research_type.value,
                "system_prompt": self.prompts["system"],
                "clarification_prompt": self.prompts["clarification"],
                "supervisor_prompt": self.prompts["supervisor"],
                "final_report_prompt": self.prompts["final_report"],
                
                "model_manager": self.model_manager,
                "logger": self.logger,
                "error_handler": self.error_handler,
                "rate_limiter": self.rate_limiter,
                
                "thread_id": self.thread_id
            }
        }
    
    def print_configuration(self):
        """Print complete configuration summary"""
        print("\n" + "="*70)
        print("🔬 INTEGRATED RESEARCH CONFIGURATION")
        print("="*70)
        
        # Research Type
        print(f"\n📋 Research Type: {self.research_type.value.upper()}")
        print(f"   {self.prompts['system'][:100]}...")
        
        # Models
        print(f"\n🤖 Model Configuration:")
        print(f"   Research:      {self.model_manager.get_model_for_stage('research').name}")
        print(f"   Final Report:  {self.model_manager.get_model_for_stage('final_report').name}")
        print(f"   Compression:   {self.model_manager.get_model_for_stage('compression').name}")
        print(f"   Summarization: {self.model_manager.get_model_for_stage('summarization').name}")
        
        # Budget
        if self.model_config.total_cost_budget:
            print(f"\n💰 Budget: ${self.model_config.total_cost_budget:.2f}")
        
        # Rate Limits
        rl_config = self.rate_limiter.config
        print(f"\n🛡️  Rate Limits:")
        print(f"   Requests/min:  {rl_config.requests_per_minute}")
        print(f"   Tokens/min:    {rl_config.tokens_per_minute:,}")
        print(f"   Cost/hour:     ${rl_config.cost_limit_per_hour:.2f}")
        print(f"   Cost/day:      ${rl_config.cost_limit_per_day:.2f}")
        
        # Research Parameters
        print(f"\n⚙️  Research Parameters:")
        print(f"   Max Iterations:    {self.max_iterations}")
        print(f"   Max Tool Calls:    {self.max_tool_calls}")
        print(f"   Max Researchers:   {self.max_concurrent_researchers}")
        
        # Tools
        print(f"\n🔧 Tools: {len(self.tools.get_tool_definitions())} available")
        
        print("="*70 + "\n")
    
    def print_summary(self):
        """Print session summary after research"""
        print("\n" + "="*70)
        print("📊 RESEARCH SESSION SUMMARY")
        print("="*70)
        
        # Logging metrics
        log_metrics = self.logger.get_metrics()
        print(f"\n📈 API Usage:")
        print(f"   Total Calls:    {log_metrics['api_calls']}")
        print(f"   Tokens Used:    {log_metrics['tokens_used']:,}")
        print(f"   Total Cost:     ${log_metrics['total_cost']:.4f}")
        print(f"   Success Rate:   {log_metrics['success_rate']*100:.1f}%")
        
        # Model usage
        print(f"\n🤖 Model Usage:")
        self.model_manager.print_cost_summary()
        
        # Rate limiting
        rl_metrics = self.rate_limiter.get_metrics()
        print(f"\n🛡️  Rate Limiting:")
        print(f"   Rate Limited:   {rl_metrics['rate_limited']} times")
        print(f"   Cost Limited:   {rl_metrics['cost_limited']} times")
        print(f"   Retries:        {rl_metrics['retries']}")
        
        # Errors
        error_summary = self.error_handler.get_error_summary()
        if error_summary['total_errors'] > 0:
            print(f"\n⚠️  Errors: {error_summary['total_errors']}")
            for error in error_summary['recent_errors'][-3:]:
                print(f"   - [{error['severity']}] {error['message'][:60]}...")
        else:
            print(f"\n✅ No errors occurred")
        
        print("="*60 + "\n")