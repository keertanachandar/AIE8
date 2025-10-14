# integrated_research.py - Complete integration

from tools import ResearchTools
from prompts import ResearchType, get_research_prompts
from error_handler import ErrorHandler, with_error_handling, RateLimitError
from logger import ResearchLogger
from rate_limiter import RateLimiter, RateLimitConfig
import uuid
import asyncio
import time
from typing import Optional

class IntegratedResearchWorkflow:
    """Research workflow with error handling, logging, and rate limiting"""
    
    def __init__(
        self,
        research_type: ResearchType = ResearchType.USER_RESEARCH,
        rate_limit_config: Optional[RateLimitConfig] = None,
        log_dir: str = "logs"
    ):
        # Initialize components
        self.research_type = research_type
        self.logger = ResearchLogger(
            name=f"research_{research_type.value}",
            log_dir=log_dir
        )
        self.error_handler = ErrorHandler(self.logger.logger)
        self.rate_limiter = RateLimiter(
            config=rate_limit_config or RateLimitConfig(),
            logger=self.logger.logger
        )
        
        # Initialize tools and prompts
        self.tools = ResearchTools()
        self.prompts = get_research_prompts(research_type)
        
        # Create config
        self.config = self._create_config()
        
        self.logger.info(f"Initialized research workflow for {research_type.value}")
    
    def _create_config(self) -> dict:
        """Create configuration with all components"""
        return {
            "configurable": {
                # Model configuration
                "research_model": "anthropic:claude-sonnet-4-20250514",
                "research_model_max_tokens": 10000,
                "compression_model": "anthropic:claude-sonnet-4-20250514",
                "compression_model_max_tokens": 8192,
                "final_report_model": "anthropic:claude-sonnet-4-20250514",
                "final_report_model_max_tokens": 10000,
                "summarization_model": "anthropic:claude-sonnet-4-20250514",
                "summarization_model_max_tokens": 8192,
                
                # Research behavior
                "allow_clarification": True,
                "max_concurrent_research_units": 10,
                "max_researcher_iterations": 2,
                "max_react_tool_calls": 5,
                
                # Search configuration
                "search_api": "anthropic",
                "max_content_length": 50000,
                
                # Custom components
                "custom_tools": self.tools.get_tool_definitions(),
                "tool_executor": self.tools.execute_tool,
                "enable_tools": True,
                "research_type": self.research_type.value,
                "system_prompt": self.prompts["system"],
                "clarification_prompt": self.prompts["clarification"],
                "supervisor_prompt": self.prompts["supervisor"],
                "final_report_prompt": self.prompts["final_report"],
                
                # Logging and error handling
                "logger": self.logger,
                "error_handler": self.error_handler,
                "rate_limiter": self.rate_limiter,
                
                # Thread ID
                "thread_id": str(uuid.uuid4())
            }
        }
    
    @with_error_handling(component="api_call", fallback_value=None)
    async def make_api_call(
        self,
        model: str,
        messages: list,
        estimated_tokens: int = 1000
    ):
        """Make API call with rate limiting and error handling"""
        
        # Check rate limits
        permission = await self.rate_limiter.acquire(
            estimated_tokens=estimated_tokens,
            model=model
        )
        
        if not permission["allowed"]:
            if permission["reason"] == "cost_limit":
                raise RateLimitError(
                    permission["message"],
                    retry_after=permission["retry_after"]
                )
            elif permission["reason"] in ["rate_limit", "token_rate_limit"]:
                # Wait and retry
                wait_time = permission["retry_after"]
                self.logger.warning(f"Rate limited, waiting {wait_time:.1f}s")
                await asyncio.sleep(wait_time)
                return await self.make_api_call(model, messages, estimated_tokens)
        
        # Make the actual API call
        start_time = time.time()
        
        try:
            # Your actual API call here
            # response = await client.messages.create(...)
            response = None  # Placeholder
            
            duration = time.time() - start_time
            
            # Record usage
            if response:
                input_tokens = getattr(response.usage, 'input_tokens', 0)
                output_tokens = getattr(response.usage, 'output_tokens', 0)
                cost = self.rate_limiter.calculate_cost(model, input_tokens, output_tokens)
                
                self.rate_limiter.record_usage(model, input_tokens, output_tokens)
                self.logger.log_api_call(
                    model=model,
                    tokens_used=input_tokens + output_tokens,
                    cost=cost,
                    duration=duration,
                    success=True
                )
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.log_api_call(
                model=model,
                tokens_used=0,
                cost=0,
                duration=duration,
                success=False,
                metadata={"error": str(e)}
            )
            raise
    
    @with_error_handling(component="tool_execution", fallback_value=None)
    async def execute_tool(self, tool_name: str, params: dict):
        """Execute tool with error handling and logging"""
        start_time = time.time()
        
        try:
            result = self.tools.execute_tool(tool_name, params)
            duration = time.time() - start_time
            
            self.logger.log_tool_usage(
                tool_name=tool_name,
                success=result.success,
                duration=duration,
                result=result.data
            )
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.log_tool_usage(
                tool_name=tool_name,
                success=False,
                duration=duration
            )
            raise
    
    async def run_research(self, query: str, pdf_content: Optional[str] = None):
        """Run complete research workflow with all protections"""
        
        self.logger.info(f"Starting research: {query[:100]}...")
        self.logger.log_research_stage("initialization", "started")
        
        try:
            # Build research request
            research_request = self._build_research_request(query, pdf_content)
            
            # Log stage
            self.logger.log_research_stage("clarification", "started")
            
            # Execute workflow (placeholder - integrate with your graph)
            # async for event in graph.astream(...):
            #     await self._process_event(event)
            
            self.logger.log_research_stage("completion", "success")
            
            # Print summaries
            self.logger.print_summary()
            self.rate_limiter.print_status()
            
            error_summary = self.error_handler.get_error_summary()
            if error_summary["total_errors"] > 0:
                print("\n⚠️  Errors occurred during research:")
                print(f"   Total: {error_summary['total_errors']}")
                for error in error_summary["recent_errors"]:
                    print(f"   - [{error['severity']}] {error['message']}")
            
        except Exception as e:
            self.logger.log_research_stage("completion", "failed", {"error": str(e)})
            self.logger.error(f"Research failed: {str(e)}")
            raise
    
    def _build_research_request(self, query: str, pdf_content: Optional[str] = None) -> str:
        """Build research request with proper formatting"""
        request = f"""
{query}

Available Tools:
{[tool['name'] for tool in self.tools.get_tool_definitions()]}

Research Type: {self.research_type.value}
"""
        
        if pdf_content:
            request += f"\n\nDocument Content:\n{pdf_content[:10000]}"
        
        return request
    
    async def _process_event(self, event: dict):
        """Process workflow event with logging"""
        for node_name, node_output in event.items():
            self.logger.log_research_stage(node_name, "processing")
            
            # Handle tool calls
            if "tool_calls" in node_output:
                for tool_call in node_output["tool_calls"]:
                    await self.execute_tool(
                        tool_call.get("name"),
                        tool_call.get("input", {})
                    )