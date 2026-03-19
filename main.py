#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AssistantAgent Example

This example demonstrates how to use the AssistantAgent to solve problems
using direct thinking and various tools and skills.
"""

import asyncio
from minion.agents.assistant_agent import AssistantAgent
from minion.tools.default_tools import FinalAnswerTool
from minion.tools.think_tool import ThinkTool
from minion.tools.web_search_tool import WebSearchTool
from minion.tools.file_tools import FileWriteTool, FileReadTool


async def example_basic_usage():
    """Basic usage of AssistantAgent"""
    print("=== Basic AssistantAgent Usage ===")

    # Create AssistantAgent with basic tools
    agent = AssistantAgent(
        name="assistant_demo",
        enable_reflection=True,
        enable_state_tracking=True
    )
    await agent.setup()
    # Add tools
    agent.add_tool(ThinkTool())
    agent.add_tool(WebSearchTool())
    agent.add_tool(FileWriteTool())
    agent.add_tool(FileReadTool())

    # Run a simple task
    task = "What is the capital of France?"
    result = await agent.run(task)
    print(f"Task: {task}")
    print(f"Result: {result}")
    print()


async def example_complex_task():
    """Complex task demonstration"""
    print("=== Complex Task Example ===")

    # Create AssistantAgent
    agent = AssistantAgent(
        name="assistant_complex",
        enable_reflection=True,
        enable_state_tracking=True
    )
    await agent.setup()
    # Add tools
    agent.add_tool(ThinkTool())
    agent.add_tool(WebSearchTool())
    agent.add_tool(FileWriteTool())
    agent.add_tool(FileReadTool())

    # Run a more complex task
    task = "Research the current population of Paris, France, and write it to a file called 'paris_population.txt'."
    result = await agent.run(task)
    print(f"Task: {task}")
    print(f"Result: {result}")
    print()


async def example_with_skills():
    """Example using skills"""
    print("=== Skills Example ===")

    # Create AssistantAgent
    agent = AssistantAgent(
        name="assistant_skills",
        enable_reflection=True,
        enable_state_tracking=True
    )
    await agent.setup()
    # Add tools (including SkillTool if available)
    agent.add_tool(ThinkTool())

    # Run a task that might benefit from skills
    task = "Analyze the sentiment of the following text: 'I love this product! It's amazing and works perfectly.'"
    result = await agent.run(task)
    print(f"Task: {task}")
    print(f"Result: {result}")
    print()


async def example_state_management():
    """Example of state management"""
    print("=== State Management Example ===")

    # Create AssistantAgent with state tracking enabled
    agent = AssistantAgent(
        name="assistant_state",
        enable_reflection=True,
        enable_state_tracking=True
    )
    await agent.setup()
    # Add tools
    agent.add_tool(ThinkTool())

    # First task
    task1 = "What is the capital of Germany?"
    result1 = await agent.run(task1)
    print(f"Task 1: {task1}")
    print(f"Result 1: {result1}")

    # Second task (should have context from first)
    task2 = "What is its population?"
    result2 = await agent.run(task2)
    print(f"Task 2: {task2}")
    print(f"Result 2: {result2}")

    # Get statistics
    stats = agent.get_statistics()
    print(f"Agent Statistics: {stats}")
    print()


async def main():
    # Run all examples
    await example_basic_usage()
    await example_complex_task()
    await example_with_skills()
    await example_state_management()


if __name__ == "__main__":
    asyncio.run(main())
