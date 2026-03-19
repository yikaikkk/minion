"""
AssistantAgent: A direct thinking agent that uses skills and tools to solve problems.

This agent extends the BaseAgent to provide:
- Direct thinking instead of code-based reasoning
- Skill and tool integration
- Reason-Act-Observe cycles
- Memory integration for learning
- Task planning and execution
"""
from copy import copy
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
import re
import logging
import uuid
from datetime import datetime

from .base_agent import BaseAgent
from minion.types.agent_response import AgentResponse
from minion.types.agent_state import AgentState, AssistantAgentState
from ..tools.base_tool import BaseTool
from ..main.input import Input
from ..tools.default_tools import FinalAnswerTool

logger = logging.getLogger(__name__)


class ThinkingEngine:
    """Engine for managing different thinking strategies."""
    
    def __init__(self, agent: 'AssistantAgent'):
        self.agent = agent
        self.reflection_triggers = {
            'error_count': 3,  # Trigger reflection after 3 errors
            'step_count': 5,   # Trigger reflection every 5 steps
            'low_confidence': 0.3,  # Trigger reflection when confidence < 0.3
        }
    
    def should_reflect(self, state: AssistantAgentState) -> bool:
        """Determine if the agent should reflect based on current state."""
        # Check triggers
        if state.error_count >= self.reflection_triggers['error_count']:
            return True
        if state.step_count > 0 and state.step_count % self.reflection_triggers['step_count'] == 0:
            return True
        if state.last_confidence < self.reflection_triggers['low_confidence']:
            return True
        
        return False
    
    async def generate_reflection(self, state: AssistantAgentState) -> str:
        """Generate a reflection prompt based on current state."""
        history = state.history
        task = state.task or ''
        error_count = state.error_count
        
        reflection_prompt = f"""
Let me think about the current situation:

**Task**: {task}

**Progress so far**: {len(history)} steps completed
**Errors encountered**: {error_count}

**Recent actions**:
{self._format_recent_history(history[-3:] if history else [])}

**Reflection questions**:
1. Am I making progress toward the goal?
2. Are there any patterns in my errors?
3. Should I try a different approach?
4. What have I learned so far?
5. What skills or tools should I use next?

Let me analyze this step by step...
"""
        return reflection_prompt
    
    def _format_recent_history(self, history: List[Any]) -> str:
        """Format recent history for reflection."""
        if not history:
            return "No recent actions"
        
        formatted = []
        for i, step in enumerate(history[-3:], 1):
            if isinstance(step, tuple) and len(step) > 0:
                action = step[0]
                formatted.append(f"{i}. {action}")
        
        return '\n'.join(formatted) if formatted else "No recent actions"


@dataclass
class AssistantAgent(BaseAgent):
    """
    A direct thinking agent that uses skills and tools to solve problems.
    
    This agent extends BaseAgent with:
    - Direct thinking instead of code-based reasoning
    - Skill and tool integration
    - Reason-Act-Observe cycles
    - Memory integration
    - Task planning and execution
    """
    
    name: str = "assistant_agent"
    thinking_engine: Optional[ThinkingEngine] = None
    enable_reflection: bool = True
    
    # State tracking and conversation history (optional)
    enable_state_tracking: bool = False  # Whether to enable persistent state tracking functionality
    conversation_history: List[Dict[str, Any]] = field(default_factory=list)
    persistent_state: Dict[str, Any] = field(default_factory=dict)
    auto_save_state: bool = True
    conversation_context_limit: int = 10  # Limit conversation history for context
    
    # Internal state management
    state: AssistantAgentState = field(default_factory=AssistantAgentState, init=False)
    
    def __post_init__(self):
        """Initialize the AssistantAgent with thinking capabilities and optional state tracking."""
        super().__post_init__()
        
        # Set agent reference in state if not already set
        if self.state and not self.state.agent:
            self.state.agent = self
        
        # Initialize thinking engine
        self.thinking_engine = ThinkingEngine(self)
        
    @property
    def history(self) -> List[Any]:
        """Get the history from internal state."""
        return self.state.history
    
    @history.setter
    def history(self, value: List[Any]):
        """Set the history in internal state."""
        self.state.history = value

    def _initialize_state(self):
        """Initialize persistent state if state tracking is enabled."""
        if not self.persistent_state:
            self.persistent_state = {
                'initialized_at': str(uuid.uuid4()),
                'conversation_count': 0,
                'variables': {},
                'memory_store': {},
                'learned_patterns': []
            }
        logger.info("State tracking initialized")

    async def setup(self):
        if self._is_setup:
            return
        await super().setup()
        self._is_setup = False #since super setting this to True, we immediately set it to False

        # Add FinalAnswerTool if not already present (avoid duplicates)
        has_final_answer = any(
            getattr(tool, 'name', None) == 'final_answer'
            for tool in self.tools
        )
        if not has_final_answer:
            self.add_tool(FinalAnswerTool())

        # Append skills prompt if SkillTool is in tools
        self._append_skills_prompt()

        # Initialize state tracking if enabled
        if self.enable_state_tracking:
            self._initialize_state()
        self._is_setup = True

    def _append_skills_prompt(self):
        """Append skills prompt to system_prompt if SkillTool is available."""
        from minion.tools.skill_tool import SkillTool, generate_skill_tool_prompt

        # Check if SkillTool is in tools
        has_skill_tool = any(isinstance(t, SkillTool) for t in self.tools)
        if not has_skill_tool:
            return

        # Generate skills prompt
        skills_prompt = generate_skill_tool_prompt()
        if not skills_prompt or "<available_skills>" not in skills_prompt:
            return

        # Append to system_prompt
        if self.system_prompt:
            self.system_prompt += "\n\n# Skills\n" + skills_prompt
        else:
            self.system_prompt = "# Skills\n" + skills_prompt

        logger.debug("Skills prompt appended to system_prompt")


    async def execute_step(self, state: AssistantAgentState, stream: bool = False, **kwargs) -> AgentResponse:
        """
        Execute a step with direct thinking.
        
        This method overrides the parent's execute_step to add:
        - Direct thinking
        - Self-reflection triggers
        - Enhanced error handling
        
        Args:
            state: Strong-typed AssistantAgentState
            **kwargs: Additional arguments
        
        Returns:
            AgentResponse: Structured response instead of 5-tuple
        """
        # Use the provided state
        self.state = state
        
        # Extract input_data from internal state
        input_data = self.state.input
        if not input_data:
            raise ValueError("No input found in state")
        
        # Check if we should reflect first
        if self.enable_reflection and self.thinking_engine and self.thinking_engine.should_reflect(self.state):
            await self._perform_reflection()
        
        # Enhance the input for direct thinking
        enhanced_input = self._enhance_input_for_direct_thinking(input_data)
        self.state.input = enhanced_input
        
        # Execute the step
        try:
            if not self.brain:
                raise ValueError("Brain is not initialized")
            
            # Get tools list from agent
            tools = self.tools
            
            # 同步state到brain，这样minion可以访问agent的状态
            self.brain.state = self.state
            
            # Call brain.step with enhanced input directly
            result = await self.brain.step(self.state, tools=tools, stream=stream, system_prompt=self.system_prompt, **kwargs)
            
            # Convert result to AgentResponse
            agent_response = AgentResponse.from_tuple(result)
            
            # Check if this is already a processed result
            if hasattr(result, '__len__') and len(result) >= 5:
                response, score, terminated, truncated, info = result
                
                # Check if final_answer was already detected by the underlying system
                if isinstance(info, dict) and (
                    info.get('is_final_answer', False) or 
                    'final_answer' in info or
                    terminated
                ):
                    # Already processed, use as-is
                    return agent_response
            
            return agent_response
            
        except Exception as e:
            logger.error(f"Step execution failed: {e}")
            raise e
    
    def _enhance_input_for_direct_thinking(self, input_data: Input) -> Input:
        # Create a new Input with enhanced query
        enhanced_input = input_data
        # Ensure route is set appropriately
        if not enhanced_input.route:
            enhanced_input.route = 'cot'  # Use 'cot' (Chain of Thought) as default route
        
        return enhanced_input
    
    async def _perform_reflection(self) -> None:
        """Perform self-reflection using the think tool."""
        if not self.thinking_engine:
            return
        
        # Use internal state for reflection
        reflection_prompt = await self.thinking_engine.generate_reflection(self.state)
        
        # Update reflection count
        self.state.reflection_count += 1
        self.state.last_reflection_step = self.state.step_count
        
        # Use the think tool
        think_tool = self.get_tool('think')
        if think_tool:
            think_tool.forward(reflection_prompt)
            
            # Add reflection to memory if available
            if hasattr(self, 'add_memory'):
                self.add_memory(
                    f"Reflection: {reflection_prompt}",
                    metadata={'type': 'reflection', 'timestamp': datetime.now().isoformat()}
                )
    
    async def update_state(self, state: AssistantAgentState, result: Any) -> AssistantAgentState:
        """Update state with Assistant-specific information."""
        # Update the internal state
        self.state = await super().update_state(state, result)

        # Extract confidence from result if available
        if isinstance(result, tuple) and len(result) >= 2:
            self.state.last_confidence = result[1]  # score/confidence

        return self.state
    
    async def solve_problem(self, problem: str, reset: bool = False, **kwargs) -> str:
        """
        Solve a problem using direct thinking.
        
        Args:
            problem: The problem to solve
            reset: If True, reset the agent state before execution (when state tracking is enabled)
            **kwargs: Additional parameters
            
        Returns:
            The solution as a string
        """
        input_obj = Input(query=problem, route='default')
        result = await self.run_async(input_obj, reset=reset, **kwargs)
        return str(result)
    
    def is_done(self, result: Any, state: AssistantAgentState) -> bool:
        """
        Check if the task is completed by detecting the is_final_answer flag.
        """
        # Use the provided state
        self.state = state
        
        # First call the parent's is_done method
        parent_done = super().is_done(result, self.state)
        if parent_done:
            return True
        
        # Check if there is a final_answer flag in the internal state
        if self.state.is_final_answer:
            return True
        
        # For AgentResponse, use its built-in check method
        if hasattr(result, 'is_done'):
            return result.is_done()
        
        # Check if there is a termination flag in the result (5-tuple format)
        if isinstance(result, tuple) and len(result) >= 3:
            terminated = result[2]
            if terminated:
                return True

        return False
    
    # State management methods
    
    def run(self, 
           task: Optional[Union[str, Input]] = None,
           max_steps: Optional[int] = None,
           reset: bool = False,
           route: Optional[str] = None,
           **kwargs) -> Any:
        """
        Synchronous interface for running the agent using internal state.
        
        Args:
            task: Task description or Input object
            max_steps: Maximum number of steps
            reset: If True, reset the agent state before execution
            route: 可选的route名称，如 "default", "cot", "plan" 等，指定使用哪个minion
            **kwargs: Additional parameters
            
        Returns:
            Final task result
        """
        import asyncio
        try:
            # Check if we're already in an event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If already in a running event loop, return the coroutine
                return self.run_async(task=task, max_steps=max_steps, reset=reset, stream=False, route=route, **kwargs)
            else:
                # If not in an event loop, run it normally
                return asyncio.run(self.run_async(task=task, max_steps=max_steps, reset=reset, stream=False, route=route, **kwargs))
        except RuntimeError:
            # No event loop exists, create one
            return asyncio.run(self.run_async(task=task, max_steps=max_steps, reset=reset, stream=False, route=route, **kwargs))

    async def run_async(self, task: Optional[Union[str, Input]] = None,
                       max_steps: Optional[int] = None,
                       reset: bool = False,
                       stream: bool = False,
                       route: Optional[str] = None,
                       **kwargs) -> Any:
        """
        Run the AssistantAgent with direct thinking capabilities using internal state.
        
        Args:
            task: Task description or Input object
            max_steps: Maximum steps to execute
            reset: If True, reset the agent state before execution
            stream: If True, return streaming generator
            route: 可选的route名称，如 "default", "cot", "plan" 等，指定使用哪个minion
            **kwargs: Additional parameters
            
        Returns:
            Agent response or async generator for streaming
        """
        # Prepare input and internal state
        enhanced_input = self._prepare_input(task, route=route)
        self._prepare_internal_state(task, reset)
        
        # Record input in state for interaction tracking
        self.state.input = enhanced_input
        
        try:
            # Use BaseAgent's logic but with our enhanced input and internal state
            result = await super().run_async(
                task=enhanced_input,
                state=self.state, 
                max_steps=max_steps, 
                stream=stream, 
                route=route,
                **kwargs
            )
            
            # Record interaction if state tracking is enabled
            if self.enable_state_tracking:
                await self._record_interaction(enhanced_input, result, reset)
                if self.auto_save_state:
                    self._save_persistent_state(self.state)
            
            return result
            
        except Exception as e:
            # Record failed interaction if state tracking is enabled
            if self.enable_state_tracking:
                await self._record_interaction(enhanced_input, f"Error: {e}", reset)
            raise
    
    def _prepare_input(self, task: Optional[Union[str, Input]], route: Optional[str] = None) -> Input:
        """
        Prepare input data for execution.
        
        Args:
            task: Task description or Input object
            route: 可选的route名称，如果提供则覆盖默认的'cot' route
            
        Returns:
            Input: Prepared Input object with enhanced query
        """
        # Convert string task to Input if needed
        if isinstance(task, str):
            # Use provided route or default to 'cot'
            default_route = route if route is not None else 'cot'
            input_data = Input(query=task, route=default_route)
        elif isinstance(task, Input):
            input_data = task
            # Set route based on priority: explicit route param > existing route > default 'cot'
            if route is not None:
                input_data.route = route
            elif not input_data.route:
                input_data.route = 'cot'
        else:
            raise ValueError(f"Task must be string or Input object, got {type(task)}")
        
        # Enhance input with direct thinking instructions
        enhanced_input = input_data

        return enhanced_input
    
    def _prepare_internal_state(self, task: Optional[Union[str, Input]], reset: bool) -> None:
        """
        Prepare internal state for execution.
        
        Args:
            task: Task description or Input object
            reset: Whether to reset state before execution
        """
        # Initialize internal state if needed
        if not hasattr(self, 'state') or self.state is None:
            self.state = AssistantAgentState(agent=self)
        
        # Handle reset functionality
        if reset:
            if self.enable_state_tracking:
                # Reset both internal state and persistent state
                self.reset_state()
                logger.info("Agent state has been reset (including persistent state)")
            else:
                # Just reset internal state
                self.state.reset()
                logger.info("Agent internal state has been reset")
        
        # Set task information
        if task is not None:
            if isinstance(task, str):
                self.state.task = task
            else:
                self.state.task = task.query
        
        # Add persistent information if state tracking is enabled
        if self.enable_state_tracking:
            # Merge persistent state into metadata
            self.state.metadata.update(self.persistent_state)
            self.state.metadata['conversation_history'] = self.get_recent_history()
    
    def reset_state(self) -> None:
        """
        Reset agent state.
        
        This clears:
        - Conversation history
        - Working variables
        - Temporary memory
        - Internal state
        But preserves:
        - Learned patterns
        - Core configuration
        """
        # Reset internal state first
        if hasattr(self, 'state') and self.state:
            self.state.reset()
        else:
            self.state = AssistantAgentState(agent=self)
        
        if self.enable_state_tracking:
            # Clear conversation history
            self.conversation_history = []
            
            # Reset session ID
            self.session_id = str(uuid.uuid4())
            
            # Reset working state but preserve learned patterns
            learned_patterns = self.persistent_state.get('learned_patterns', [])
            self.persistent_state = {
                'initialized_at': str(uuid.uuid4()),
                'conversation_count': 0,
                'variables': {},
                'memory_store': {},
                'learned_patterns': learned_patterns  # Preserve learned patterns
            }
        
        logger.info("Agent state reset completed")
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get current agent state including conversation and persistent state.
        
        Returns:
            Complete state dictionary or empty dict if state tracking is disabled
        """
        if not self.enable_state_tracking:
            return {}
            
        return {
            'conversation_history': self.conversation_history,
            'persistent_state': self.persistent_state,
            'session_id': self.session_id,
            'conversation_count': len(self.conversation_history) // 2,  # Approximate turns
        }
    
    def load_state(self, state: Dict[str, Any]) -> None:
        """
        Load agent state from dictionary.
        
        Args:
            state: State dictionary to load
        """
        if not self.enable_state_tracking:
            logger.warning("State tracking is disabled, load_state has no effect")
            return
            
        if 'conversation_history' in state:
            self.conversation_history = state['conversation_history']
        
        if 'persistent_state' in state:
            self.persistent_state = state['persistent_state']
        
        if 'session_id' in state:
            self.session_id = state['session_id']
        
        logger.info(f"Agent state loaded with {len(self.conversation_history)} conversation entries")
    
    def _add_conversation_context(self, input_data: Input) -> Input:
        """Add conversation context to input for better continuity."""
        if not self.enable_state_tracking or not self.conversation_history:
            return input_data
        
        # Get recent conversation for context
        recent_history = self.get_recent_history(limit=self.conversation_context_limit)
        
        if not recent_history:
            return input_data
        
        # Format conversation context
        context_lines = []
        for entry in recent_history:
            role = entry['role'].upper()
            content = str(entry['content'])[:200]  # Limit content length
            context_lines.append(f"{role}: {content}")
        
        conversation_context = "\n".join(context_lines)
        
        # Enhanced query with conversation context
        enhanced_query = f"""**Conversation Context:**
{conversation_context}

**Current Request:**
{input_data.query}

**Instructions:**
- Consider the conversation context when responding
- Maintain consistency with previous interactions
- Use any relevant information from the conversation history
- Select appropriate skills and tools to solve the problem
"""
        
        return Input(
            query=enhanced_query,
            route=getattr(input_data, 'route', None) or 'default',
            check=getattr(input_data, 'check', False),
            dataset=getattr(input_data, 'dataset', None),
            metadata=getattr(input_data, 'metadata', {})
        )
    
    async def _record_interaction(self, input_data: Input, result: Any, was_reset: bool) -> None:
        """Record the interaction in conversation history."""
        if not self.enable_state_tracking:
            return
            
        # Record user input
        self.add_to_history("user", input_data.query)
        
        # Record system response
        if isinstance(result, AgentResponse):
            response_content = result.raw_response
        else:
            response_content = str(result)
        
        self.add_to_history("assistant", response_content)
        
        # Add reset indicator if state was reset
        if was_reset:
            self.add_to_history("system", "State was reset before this interaction")
        
        # Update conversation count in persistent state
        self.persistent_state['conversation_count'] = len(self.conversation_history) // 2
    
    def _save_persistent_state(self, current_state: Any) -> None:
        """Save relevant information to persistent state."""
        if not self.enable_state_tracking:
            return
            
        # Extract variables from execution state
        variables = {}
        
        # Handle different types of current_state
        if hasattr(current_state, 'dict'):
            # For Pydantic models
            state_dict = current_state.dict()
            for key, value in state_dict.items():
                if key.startswith('result_'):
                    variables[key] = value
            
            # Save any learned patterns or insights
            if 'learned_patterns' in state_dict:
                self.persistent_state['learned_patterns'].extend(state_dict['learned_patterns'])
        elif isinstance(current_state, dict):
            # For regular dictionaries
            for key, value in current_state.items():
                if key.startswith('result_'):
                    variables[key] = value
            
            # Save any learned patterns or insights
            if 'learned_patterns' in current_state:
                self.persistent_state['learned_patterns'].extend(current_state['learned_patterns'])
        
        if variables:
            self.persistent_state['variables'].update(variables)
    
    def get_recent_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get recent conversation history."""
        if not self.enable_state_tracking:
            return []
            
        if limit is None:
            return self.conversation_history
        return self.conversation_history[-limit:] if self.conversation_history else []
    
    def clear_history(self) -> None:
        """Clear conversation history while preserving persistent state."""
        if not self.enable_state_tracking:
            logger.warning("State tracking is disabled, clear_history has no effect")
            return
            
        self.conversation_history = []
        self.session_id = str(uuid.uuid4())
        logger.info("Conversation history cleared")
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get complete conversation history."""
        if not self.enable_state_tracking:
            return []
            
        return self.conversation_history
    
    def add_to_history(self, role: str, content: Any) -> None:
        """
        Add entry to conversation history.
        
        Args:
            role: Role (user, assistant, system)
            content: Content of the message
        """
        if not self.enable_state_tracking:
            return
            
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": str(uuid.uuid4())[:8]  # Short timestamp
        })
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get conversation and usage statistics."""
        if not self.enable_state_tracking:
            return {
                'state_tracking': 'disabled'
            }
            
        return {
            'total_conversations': self.persistent_state.get('conversation_count', 0),
            'current_session_messages': len(self.conversation_history),
            'session_id': self.session_id,
            'variables_stored': len(self.persistent_state.get('variables', {})),
            'patterns_learned': len(self.persistent_state.get('learned_patterns', [])),
            'auto_save_enabled': self.auto_save_state
        }
