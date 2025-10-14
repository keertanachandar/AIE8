# quick_research_setup.py - Easy switching between research types

from prompts import ResearchType, get_research_prompts
from tools import ResearchTools
import uuid

def setup_research_config(
    research_type: ResearchType,
    max_iterations: int = 2,
    max_tools_calls: int = 5
) -> dict:
    """Quick setup for any research type"""
    
    research_tools = ResearchTools()
    research_prompts = get_research_prompts(research_type)
    
    config = {
        "configurable": {
            "research_model": "anthropic:claude-sonnet-4-20250514",
            "research_model_max_tokens": 10000,
            "compression_model": "anthropic:claude-sonnet-4-20250514",
            "compression_model_max_tokens": 8192,
            "final_report_model": "anthropic:claude-sonnet-4-20250514",
            "final_report_model_max_tokens": 10000,
            "summarization_model": "anthropic:claude-sonnet-4-20250514",
            "summarization_model_max_tokens": 8192,
            "allow_clarification": True,
            "max_concurrent_research_units": 10,
            "max_researcher_iterations": max_iterations,
            "max_react_tool_calls": max_tools_calls,
            "search_api": "anthropic",
            "max_content_length": 50000,
            "custom_tools": research_tools.get_tool_definitions(),
            "tool_executor": research_tools.execute_tool,
            "enable_tools": True,
            "research_type": research_type.value,
            "system_prompt": research_prompts["system"],
            "clarification_prompt": research_prompts["clarification"],
            "supervisor_prompt": research_prompts["supervisor"],
            "final_report_prompt": research_prompts["final_report"],
            "thread_id": str(uuid.uuid4())
        }
    }
    
    print(f"✓ Research configuration ready for: {research_type.value}")
    return config

# Usage examples:

# For analyzing your ChatGPT usage PDF
config_user_research = setup_research_config(ResearchType.USER_RESEARCH)

# For academic paper analysis
config_academic = setup_research_config(ResearchType.ACADEMIC)

# For market analysis
config_market = setup_research_config(ResearchType.MARKET)

# For technical evaluation
config_technical = setup_research_config(ResearchType.TECHNICAL)