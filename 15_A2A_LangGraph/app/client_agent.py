"""Client Agent Graph for A2A Protocol.

This module implements a simple LangGraph agent that uses the A2A protocol
to communicate with another agent server.
"""
import os
import logging
from typing import Annotated, List, TypedDict

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from app.a2a_tool import query_a2a_agent, continue_a2a_conversation


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClientAgentState(TypedDict):
    """State for the client agent."""
    messages: Annotated[List[BaseMessage], add_messages]


def build_client_agent_graph(base_url: str = "http://localhost:10000"):
    """Build a client agent that communicates with an A2A server.
    
    Args:
        base_url: The base URL of the A2A agent server
        
    Returns:
        A compiled LangGraph that can interact with the A2A agent
    """
    
    # Create the language model
    model = ChatOpenAI(
        model=os.getenv('OPENAI_CHAT_MODEL', 'gpt-4o-mini'),
        openai_api_key=os.getenv('OPENAI_API_KEY'),
        temperature=0.7,
    )
    
    # System instruction for the client agent
    system_instruction = """You are a helpful AI assistant that can delegate complex tasks to a specialized agent.

You have access to an A2A agent that has the following capabilities:
- Web search for current information (via Tavily)
- Academic paper search (via ArXiv)
- Document retrieval (via RAG)

When a user asks a question:
1. If the question requires real-time information, academic research, or document retrieval, use the query_a2a_agent tool
2. If the user asks a follow-up question about a previous A2A response, use the continue_a2a_conversation tool
3. For simple questions that you can answer directly, respond without using tools
4. Always provide clear, helpful responses

Remember: The A2A agent is specialized for information retrieval and research. Use it for complex queries."""
    
    # Bind tools to the model
    tools = [query_a2a_agent, continue_a2a_conversation]
    model_with_tools = model.bind_tools(tools)
    
    # Define the agent node
    def agent_node(state: ClientAgentState):
        """Main agent node that decides whether to use tools or respond directly."""
        messages = state["messages"]
        
        # Add system instruction as the first message if not present
        if not messages or messages[0].type != "system":
            messages = [("system", system_instruction)] + messages
        
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}
    
    # Define the router function
    def should_continue(state: ClientAgentState):
        """Determine if we should continue to tools or end."""
        last_message = state["messages"][-1]
        
        # If there are tool calls, continue to the action node
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "action"
        
        # Otherwise, end the conversation
        return END
    
    # Build the graph
    graph = StateGraph(ClientAgentState)
    
    # Create tool node
    tool_node = ToolNode(tools)
    
    # Add nodes
    graph.add_node("agent", agent_node)
    graph.add_node("action", tool_node)
    
    # Set entry point
    graph.set_entry_point("agent")
    
    # Add edges
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "action": "action",
            END: END
        }
    )
    
    # After action, always go back to agent
    graph.add_edge("action", "agent")
    
    # Compile with memory
    memory = MemorySaver()
    return graph.compile(checkpointer=memory)


def create_client_agent(base_url: str = "http://localhost:10000"):
    """Create and return a client agent instance.
    
    Args:
        base_url: The base URL of the A2A agent server
        
    Returns:
        A compiled client agent graph
    """
    logger.info(f"Creating client agent for A2A server at {base_url}")
    return build_client_agent_graph(base_url)

