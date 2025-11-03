"""Interactive CLI for the A2A Client Agent.

This script provides an interactive interface to test the client agent
that communicates with the A2A server.
"""
import asyncio
import logging
from uuid import uuid4

import click
from dotenv import load_dotenv

from app.client_agent import create_client_agent
from app.a2a_tool import get_manager


load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def interactive_session(base_url: str):
    """Run an interactive session with the client agent."""
    
    print("=" * 80)
    print("🤖 A2A Client Agent - Interactive Session")
    print("=" * 80)
    print(f"\nConnecting to A2A server at: {base_url}")
    print("\nThis agent can delegate tasks to the A2A agent which has:")
    print("  • Web search capabilities (Tavily)")
    print("  • Academic paper search (ArXiv)")
    print("  • Document retrieval (RAG)")
    print("\nType 'quit' or 'exit' to end the session")
    print("Type 'help' for examples")
    print("=" * 80)
    print()
    
    # Create the client agent
    try:
        agent = create_client_agent(base_url)
        logger.info("Client agent created successfully")
    except Exception as e:
        print(f"\n❌ Error creating client agent: {e}")
        return
    
    # Create a conversation thread
    thread_id = uuid4().hex
    config = {"configurable": {"thread_id": thread_id}}
    
    conversation_count = 0
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
                
            if user_input.lower() == 'help':
                print_help()
                continue
            
            conversation_count += 1
            print(f"\n🤖 Agent (thinking...)")
            
            # Stream the agent's response
            inputs = {"messages": [("user", user_input)]}
            
            agent_response = ""
            tool_used = False
            
            async for event in agent.astream(inputs, config, stream_mode="values"):
                if "messages" in event:
                    last_message = event["messages"][-1]
                    
                    # Check if it's an AI message with content
                    if hasattr(last_message, 'content') and last_message.content:
                        if last_message.type == "ai":
                            agent_response = last_message.content
                        elif last_message.type == "tool":
                            tool_used = True
                            print(f"   🔧 Using tool: {last_message.name}")
            
            # Print the final response
            if agent_response:
                print(f"\n🤖 Agent: {agent_response}")
            else:
                print("\n🤖 Agent: [No response generated]")
                
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            logger.error(f"Error in interactive session: {e}", exc_info=True)
    
    # Cleanup
    try:
        manager = get_manager()
        await manager.close()
        logger.info("Cleaned up A2A client connections")
    except Exception as e:
        logger.warning(f"Error during cleanup: {e}")


def print_help():
    """Print help information with example queries."""
    print("\n" + "=" * 80)
    print("📚 Example Queries")
    print("=" * 80)
    print("\n🌐 Web Search Examples:")
    print("  • What are the latest developments in artificial intelligence?")
    print("  • What happened in the tech industry today?")
    print("  • Tell me about recent breakthroughs in quantum computing")
    
    print("\n📄 Academic Paper Examples:")
    print("  • Find recent papers on transformer architectures")
    print("  • Search for research on large language models")
    print("  • What are the latest papers about multimodal AI?")
    
    print("\n📚 Document Retrieval Examples:")
    print("  • What do the documents say about [topic]?")
    print("  • Find information about [specific topic] in the documents")
    
    print("\n💬 Follow-up Questions:")
    print("  • Can you provide more details?")
    print("  • What are the key findings?")
    print("  • Can you summarize that?")
    
    print("\n🎯 Mixed Queries:")
    print("  • Compare recent research papers with current industry trends")
    print("  • What do academic papers say about AI, and what's happening now?")
    print("=" * 80)


async def single_query(query: str, base_url: str):
    """Run a single query without interactive mode."""
    print(f"\n🤖 Querying A2A agent: {query}\n")
    
    # Create the client agent
    agent = create_client_agent(base_url)
    
    # Run the query
    thread_id = uuid4().hex
    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [("user", query)]}
    
    print("Response:\n" + "=" * 80)
    
    async for event in agent.astream(inputs, config, stream_mode="values"):
        if "messages" in event:
            last_message = event["messages"][-1]
            if hasattr(last_message, 'content') and last_message.content and last_message.type == "ai":
                print(last_message.content)
    
    print("=" * 80)
    
    # Cleanup
    manager = get_manager()
    await manager.close()


@click.command()
@click.option(
    '--base-url',
    default='http://localhost:10000',
    help='Base URL of the A2A server'
)
@click.option(
    '--query',
    '-q',
    help='Single query to run (non-interactive mode)'
)
@click.option(
    '--interactive',
    '-i',
    is_flag=True,
    default=False,
    help='Run in interactive mode (default if no query provided)'
)
def main(base_url: str, query: str, interactive: bool):
    """Run the A2A Client Agent.
    
    Examples:
    
        # Interactive mode
        python app/run_client_agent.py -i
        
        # Single query
        python app/run_client_agent.py -q "What are the latest AI developments?"
        
        # With custom server URL
        python app/run_client_agent.py --base-url http://localhost:8080 -i
    """
    
    if query:
        # Single query mode
        asyncio.run(single_query(query, base_url))
    else:
        # Interactive mode (default)
        asyncio.run(interactive_session(base_url))


if __name__ == '__main__':
    main()

