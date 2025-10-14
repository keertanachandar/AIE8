# complete_example.py - Complete working example

import asyncio
from quick_setup import QuickSetup
from prompts import ResearchType
from model_presets import ModelPresets
from model_registry import ModelRegistry

async def run_research_example():
    """Complete example of running research with integrated config"""
    
    # Step 1: View available options
    print("\n" + "="*70)
    print("STEP 1: Available Options")
    print("="*70)
    
    print("\n📚 Available Research Types:")
    for rt in ResearchType:
        print(f"   • {rt.value}")
    
    print("\n🤖 Available Models:")
    ModelRegistry.print_all_models()
    
    print("\n⚙️  Available Presets:")
    ModelPresets.print_presets()
    
    # Step 2: Choose your configuration
    print("\n" + "="*70)
    print("STEP 2: Setup Configuration")
    print("="*70)
    
    # Option A: Use a quick setup (RECOMMENDED)
    config = QuickSetup.user_research(
        model_preset="balanced",
        budget=25.0
    )
    
    # Option B: Custom setup (Advanced)
    # config = QuickSetup.custom(
    #     research_type=ResearchType.USER_RESEARCH,
    #     model_preset="quality",
    #     budget=50.0,
    #     requests_per_min=30,
    #     tokens_per_min=50_000
    # )
    
    # Step 3: Load your document
    print("\n" + "="*70)
    print("STEP 3: Load Document")
    print("="*70)
    
    try:
        with open("documents/research.pdf", "r") as f:
            pdf_content = f.read()
        print("✅ Document loaded successfully")
    except FileNotFoundError:
        print("❌ Document not found")
        pdf_content = "Sample content for testing..."
    
    # Step 4: Define your research query
    print("\n" + "="*70)
    print("STEP 4: Research Query")
    print("="*70)
    
    query = """
    Analyze this document about ChatGPT usage and provide insights about:
    
    1. What are the main findings about how people are using AI?
       - Look for usage patterns, demographics, and adoption trends
       - Extract key statistics and metrics
    
    2. What are the most common use cases identified?
       - Categorize use cases by type (work, education, creative, etc.)
       - Rank by frequency or importance
    
    3. What trends or patterns emerge from the data?
       - Identify growth trends over time
       - Look for surprising or unexpected patterns
       - Note any demographic variations
    """
    
    print(query)
    
    # Step 5: Run the research
    print("\n" + "="*70)
    print("STEP 5: Execute Research")
    print("="*70)
    
    try:
        # This is where you'd integrate with your actual research graph
        # For now, we'll demonstrate the configuration usage
        
        # Get the configuration dictionary
        config_dict = config.get_config_dict()
        
        # Access components
        model_manager = config_dict["configurable"]["model_manager"]
        logger = config_dict["configurable"]["logger"]
        error_handler = config_dict["configurable"]["error_handler"]
        rate_limiter = config_dict["configurable"]["rate_limiter"]
        tools = config_dict["configurable"]["custom_tools"]
        
        print(f"\n✅ Configuration loaded:")
        print(f"   • Research Type: {config_dict['configurable']['research_type']}")
        print(f"   • Research Model: {config_dict['configurable']['research_model']}")
        print(f"   • Final Report Model: {config_dict['configurable']['final_report_model']}")
        print(f"   • Available Tools: {len(tools)}")
        
        # Here you would run your actual research workflow
        # await graph.astream({"messages": [{"role": "user", "content": query}]}, config_dict)
        
        print("\n🔄 Research workflow would execute here...")
        print("   (Integrate with your actual graph.astream() call)")
        
        # Step 6: Print results
        print("\n" + "="*70)
        print("STEP 6: Results & Summary")
        print("="*70)
        
        config.print_summary()
        
    except Exception as e:
        print(f"\n❌ Research failed: {e}")
        config.print_summary()

def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("🔬 INTEGRATED RESEARCH SYSTEM")
    print("   Multi-Model + Custom Prompts + Tools + Controls")
    print("="*70)
    
    # Run the example
    asyncio.run(run_research_example())

if __name__ == "__main__":
    main()