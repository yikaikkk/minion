#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AssistantAgent Example

This example demonstrates how to use the AssistantAgent to solve problems
using direct thinking and various tools and skills.
"""

import asyncio
from os import name
from minion.agents.assistant_agent import AssistantAgent
from minion.tools.default_tools import FinalAnswerTool
from minion.tools.think_tool import ThinkTool
from minion.tools.web_search_tool import WebSearchTool
from minion.tools.file_tools import FileWriteTool, FileReadTool
from minion.tools.skill_tool import SkillTool
from minion.tools.UnrestrictedBashTool import UnrestrictedBashTool

# 添加一个prompt，让ai每次都有限考虑使用skills
gernal_prompt="""【强制执行要求】：请务必优先检索并调用你的技能（Skills/Tools）来解决上述问题。严禁仅凭内在记忆直接猜测或编造答案。只有在确认没有任何技能适用时，才允许基于自身知识作答。 【问题】:"""



    
agent = None

async def init_assistant_agent():
    """初始化 assistant agent"""
    global agent
    agent=await AssistantAgent.create(
        name="assistant_agent",
        tools=[SkillTool(),UnrestrictedBashTool(),FinalAnswerTool()],
    )
    



async def get_agent():
    global agent
    if agent is None:
        await init_assistant_agent()
    return agent

async def main():
    # 初始化 assistant agent
    try:
        assistant_agent = await get_agent()
        print("AssistantAgent 初始化成功！")
        print("输入您的问题，或输入 'exit' 退出。")
        
        # 持续交互循环
        while True:
            # 获取用户输入
            user_input = input("\n> ")
            
            # 检查是否为空输入
            if not user_input.strip():
                continue
            
            # 检查是否退出
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("再见！")
                break
            
            # 处理用户输入
            try:
                print("\n处理中...")
                async for event in await assistant_agent.run_async(gernal_prompt + user_input, route='raw',stream=True, max_steps=15):
                    print(event.content,flush=True,end="")
                # print()  # 添加换行符，确保提示符在新的一行
            except Exception as e:
                print(f"处理请求失败: {e}")
                continue
    except Exception as e:
        print(f"初始化 assistant agent 失败: {e}")
        return


if __name__ == "__main__":
    asyncio.run(main())
