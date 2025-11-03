"""A2A Tool for LangGraph Client Agent.

This tool allows a LangGraph agent to make API calls to an A2A-compliant agent server.
"""
import logging
from typing import Optional
from uuid import uuid4

import httpx
from langchain_core.tools import tool
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
)


logger = logging.getLogger(__name__)


class A2AToolManager:
    """Manager for A2A client connections and state."""
    
    def __init__(self, base_url: str = "http://localhost:10000"):
        self.base_url = base_url
        self.httpx_client: Optional[httpx.AsyncClient] = None
        self.a2a_client: Optional[A2AClient] = None
        self.agent_card: Optional[AgentCard] = None
        self.context_id: Optional[str] = None
        self.task_id: Optional[str] = None
        
    async def initialize(self):
        """Initialize the A2A client by fetching the agent card."""
        if self.a2a_client:
            return  # Already initialized
            
        logger.info(f"Initializing A2A client for {self.base_url}")
        
        # Create HTTP client with longer timeout for LLM responses
        self.httpx_client = httpx.AsyncClient(timeout=httpx.Timeout(60.0))
        
        # Fetch agent card
        resolver = A2ACardResolver(
            httpx_client=self.httpx_client,
            base_url=self.base_url,
        )
        
        try:
            self.agent_card = await resolver.get_agent_card()
            logger.info(f"Successfully fetched agent card: {self.agent_card.name}")
            
            # Initialize A2A client
            self.a2a_client = A2AClient(
                httpx_client=self.httpx_client,
                agent_card=self.agent_card
            )
            logger.info("A2A client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize A2A client: {e}")
            raise
            
    async def send_message(self, message: str, continue_conversation: bool = False) -> str:
        """Send a message to the A2A agent and return the response.
        
        Args:
            message: The message to send
            continue_conversation: If True, continues the previous conversation using stored context_id and task_id
            
        Returns:
            The agent's response as a string
        """
        await self.initialize()
        
        # Build message payload
        message_payload = {
            'message': {
                'role': 'user',
                'parts': [{'kind': 'text', 'text': message}],
                'message_id': uuid4().hex,
            }
        }
        
        # If continuing conversation, add context
        if continue_conversation and self.context_id and self.task_id:
            message_payload['message']['context_id'] = self.context_id
            message_payload['message']['task_id'] = self.task_id
            logger.info(f"Continuing conversation with context_id: {self.context_id}")
        
        # Create and send request
        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(**message_payload)
        )
        
        logger.info(f"Sending message to A2A agent: {message[:50]}...")
        response = await self.a2a_client.send_message(request)
        
        # Store context for multi-turn conversations
        if hasattr(response.root, 'result'):
            self.task_id = response.root.result.id
            self.context_id = response.root.result.context_id
            logger.info(f"Stored context_id: {self.context_id}, task_id: {self.task_id}")
        
        # Extract response text
        response_text = self._extract_response_text(response)
        logger.info(f"Received response: {response_text[:100]}...")
        
        return response_text
        
    def _extract_response_text(self, response) -> str:
        """Extract text from the A2A response."""
        try:
            # Navigate the response structure to get the text
            if hasattr(response.root, 'result'):
                result = response.root.result
                
                # Check for artifacts
                if hasattr(result, 'artifacts') and result.artifacts:
                    for artifact in result.artifacts:
                        if hasattr(artifact, 'parts') and artifact.parts:
                            for part in artifact.parts:
                                if hasattr(part.root, 'text'):
                                    return part.root.text
                
                # Check for messages
                if hasattr(result, 'messages') and result.messages:
                    for message in result.messages:
                        if hasattr(message, 'parts') and message.parts:
                            for part in message.parts:
                                if hasattr(part.root, 'text'):
                                    return part.root.text
                
                # Fallback: convert entire result to string
                return str(result)
            
            return str(response)
        except Exception as e:
            logger.error(f"Error extracting response text: {e}")
            return f"Error extracting response: {str(e)}"
    
    async def close(self):
        """Close the HTTP client."""
        if self.httpx_client:
            await self.httpx_client.aclose()


# Global manager instance (will be initialized on first use)
_manager: Optional[A2AToolManager] = None


def get_manager(base_url: str = "http://localhost:10000") -> A2AToolManager:
    """Get or create the global A2A tool manager."""
    global _manager
    if _manager is None:
        _manager = A2AToolManager(base_url)
    return _manager


@tool
async def query_a2a_agent(query: str) -> str:
    """Query the A2A agent with a question or request.
    
    This tool sends a message to an AI agent running on a server via the A2A protocol.
    The agent has access to web search, academic paper search, and document retrieval.
    
    Use this tool when you need to:
    - Search the web for current information
    - Find academic papers on arXiv
    - Retrieve information from documents
    - Get comprehensive answers that require multiple tools or sources
    
    Args:
        query: The question or request to send to the agent
        
    Returns:
        The agent's response as a string
        
    Example:
        query_a2a_agent("What are the latest developments in artificial intelligence?")
    """
    manager = get_manager()
    try:
        response = await manager.send_message(query, continue_conversation=False)
        return response
    except Exception as e:
        logger.error(f"Error querying A2A agent: {e}")
        return f"Error: Failed to query A2A agent - {str(e)}"


@tool
async def continue_a2a_conversation(follow_up: str) -> str:
    """Continue the conversation with the A2A agent with a follow-up question.
    
    This tool sends a follow-up message in the same conversation context.
    Use this when you want to ask follow-up questions about the previous response.
    
    Args:
        follow_up: The follow-up question or request
        
    Returns:
        The agent's response as a string
        
    Example:
        continue_a2a_conversation("Can you provide more details about that?")
    """
    manager = get_manager()
    try:
        response = await manager.send_message(follow_up, continue_conversation=True)
        return response
    except Exception as e:
        logger.error(f"Error continuing A2A conversation: {e}")
        return f"Error: Failed to continue conversation - {str(e)}"

