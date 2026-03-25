from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from .base_agent import BaseAgent
from minion.types.agent_response import AgentResponse
from minion.types.agent_state import AgentState
from minion.main.input import Input

@dataclass
class ChatAgent(BaseAgent):
    """
    A lightweight chat-only agent that handles simple conversations without tools.
    
    This agent is designed to handle straightforward chat requests that don't require
    tool usage. It can determine if a request can be handled with just chat, and
    if not, it will indicate that the request should be forwarded to a more
    capable agent like AssistantAgent.
    """
    
    name: str = "chat_agent"
    
    # System prompt to guide the agent's behavior
    system_prompt: str = """
    You are a helpful chat assistant. Your task is to determine if the user's request
    can be handled with just a direct chat response, or if it requires the use of
    tools or more complex processing.
    
    If the request is a simple question, conversation, or request that you can answer
    directly based on your knowledge, provide a helpful response.
    
    If the request requires using tools, accessing external resources, or performing
    complex tasks, respond with exactly "NEEDS_ASSISTANT_AGENT" to indicate that
    the request should be forwarded to a more capable agent.
    """
    
    async def execute_step(self, state: AgentState, stream: bool = False, **kwargs) -> AgentResponse:
        """
        Execute a chat-only step without tools.
        
        Args:
            state: Agent state
            stream: Whether to stream the response
            **kwargs: Additional parameters
            
        Returns:
            AgentResponse: Response indicating whether to use chat or forward to assistant agent
        """
        # Use brain.step without tools to get a direct response
        result = await self.brain.step(
            state, 
            tools=[],  # No tools for chat agent
            stream=stream, 
            system_prompt=self.system_prompt, 
            **kwargs
        )
        
        # Ensure return value is an AgentResponse
        if not isinstance(result, AgentResponse):
            result = AgentResponse.from_tuple(result)
        
        return result
