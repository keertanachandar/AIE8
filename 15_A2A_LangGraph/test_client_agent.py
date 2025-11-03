"""Test script for the A2A Client Agent.

This script runs automated tests to verify the client agent functionality.
"""
import asyncio
import logging
from uuid import uuid4

from dotenv import load_dotenv

from app.client_agent import create_client_agent
from app.a2a_tool import get_manager


load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_client_agent():
    """Run tests on the client agent."""
    
    print("=" * 80)
    print("🧪 Testing A2A Client Agent")
    print("=" * 80)
    
    # Test 1: Agent Creation
    print("\n📋 Test 1: Creating client agent...")
    try:
        agent = create_client_agent()
        print("✅ Test 1 PASSED: Client agent created successfully")
    except Exception as e:
        print(f"❌ Test 1 FAILED: {e}")
        return
    
    # Test 2: Simple Query (might use A2A or respond directly)
    print("\n📋 Test 2: Running simple query...")
    try:
        thread_id = uuid4().hex
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [("user", "What is 2 + 2?")]}
        
        response_found = False
        async for event in agent.astream(inputs, config, stream_mode="values"):
            if "messages" in event:
                last_message = event["messages"][-1]
                if hasattr(last_message, 'content') and last_message.content and last_message.type == "ai":
                    response_found = True
                    print(f"   Response: {last_message.content[:100]}...")
        
        if response_found:
            print("✅ Test 2 PASSED: Agent responded successfully")
        else:
            print("❌ Test 2 FAILED: No response generated")
    except Exception as e:
        print(f"❌ Test 2 FAILED: {e}")
        logger.error("Test 2 error", exc_info=True)
    
    # Test 3: A2A Tool Call (requires server running)
    print("\n📋 Test 3: Testing A2A tool call (requires server at localhost:10000)...")
    print("   ⚠️  Make sure the A2A server is running: uv run python -m app")
    try:
        thread_id = uuid4().hex
        config = {"configurable": {"thread_id": thread_id}}
        inputs = {"messages": [("user", "Search for recent news about artificial intelligence")]}
        
        tool_call_detected = False
        response_found = False
        
        async for event in agent.astream(inputs, config, stream_mode="values"):
            if "messages" in event:
                last_message = event["messages"][-1]
                
                # Check for tool calls
                if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                    tool_call_detected = True
                    tool_name = last_message.tool_calls[0].get('name', 'unknown')
                    print(f"   🔧 Tool call detected: {tool_name}")
                
                # Check for response
                if hasattr(last_message, 'content') and last_message.content and last_message.type == "ai":
                    response_found = True
                    print(f"   Response preview: {last_message.content[:150]}...")
        
        if tool_call_detected and response_found:
            print("✅ Test 3 PASSED: A2A tool used successfully")
        elif not tool_call_detected:
            print("⚠️  Test 3 WARNING: No tool call detected (agent may have responded directly)")
        else:
            print("❌ Test 3 FAILED: Tool called but no response")
    except Exception as e:
        print(f"❌ Test 3 FAILED: {e}")
        print("   💡 Tip: Make sure the A2A server is running on localhost:10000")
        logger.error("Test 3 error", exc_info=True)
    
    # Test 4: Graph Visualization
    print("\n📋 Test 4: Testing graph visualization...")
    try:
        mermaid = agent.get_graph().draw_mermaid()
        if mermaid and "graph" in mermaid.lower():
            print("✅ Test 4 PASSED: Graph visualization generated")
            print(f"   Mermaid diagram preview: {mermaid[:100]}...")
        else:
            print("❌ Test 4 FAILED: Invalid mermaid output")
    except Exception as e:
        print(f"❌ Test 4 FAILED: {e}")
    
    # Cleanup
    print("\n📋 Cleanup: Closing connections...")
    try:
        manager = get_manager()
        await manager.close()
        print("✅ Cleanup successful")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")
    
    print("\n" + "=" * 80)
    print("🎉 Testing Complete!")
    print("=" * 80)
    print("\n💡 Next Steps:")
    print("   1. Start the A2A server: uv run python -m app")
    print("   2. Run the interactive client: uv run python app/run_client_agent.py -i")
    print("   3. See CLIENT_AGENT.md for full documentation")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_client_agent())

