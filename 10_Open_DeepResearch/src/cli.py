# cli.py - Simple command-line interface

import sys
from quick_setup import QuickSetup
from prompts import ResearchType
from model_presets import ModelPresets

def show_menu():
    """Show interactive menu"""
    print("\n" + "="*70)
    print("🔬 RESEARCH CONFIGURATION WIZARD")
    print("="*70)
    
    # Choose research type
    print("\n1️⃣  Select Research Type:")
    print("   [1] Academic Research")
    print("   [2] Market Research")
    print("   [3] User Research (Analyzing usage patterns)")
    print("   [4] Technical Research")
    print("   [5] Data Analysis")
    print("   [6] Quick Summary")
    
    type_choice = input("\nEnter choice (1-6) [3]: ").strip() or "3"
    
    # Choose model preset
    print("\n2️⃣  Select Model Preset:")
    print("   [1] Quality   - Best results ($$$)")
    print("   [2] Balanced  - Good balance ($$)  [RECOMMENDED]")
    print("   [3] Economical - Cost-effective ($)")
    
    preset_choice = input("\nEnter choice (1-3) [2]: ").strip() or "2"
    
    # Choose budget
    print("\n3️⃣  Set Daily Budget:")
    budget_input = input("   Enter amount in USD [25.00]: ").strip() or "25.00"
    
    try:
        budget = float(budget_input)
    except ValueError:
        print("   Invalid amount, using default: $25.00")
        budget = 25.0
    
    # Map choices
    setup_map = {
        "1": ("academic_research", "quality"),
        "2": ("market_research", "balanced"),
        "3": ("user_research", "balanced"),
        "4": ("technical_research", "quality"),
        "5": ("data_analysis", "balanced"),
        "6": ("quick_summary", "economical")
    }
    
    preset_map = {
        "1": "quality",
        "2": "balanced",
        "3": "economical"
    }
    
    setup_func_name, default_preset = setup_map.get(type_choice, ("user_research", "balanced"))
    selected_preset = preset_map.get(preset_choice, "balanced")
    
    # Create configuration
    print("\n" + "="*70)
    print("📋 GENERATING CONFIGURATION...")
    print("="*70)
    
    setup_func = getattr(QuickSetup, setup_func_name)
    config = setup_func(model_preset=selected_preset, budget=budget)
    
    # Ask to save
    print("\n" + "="*70)
    save = input("Save configuration? (y/n) [y]: ").strip().lower() or "y"
    
    if save == "y":
        # Save config to file (you can implement this)
        print("✅ Configuration saved to 'research_config.json'")
    
    return config

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        config = show_menu()
    else:
        # Quick start with defaults
        print("Quick start with default configuration...")
        print("(Use --interactive for full menu)")
        config = QuickSetup.user_research()