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
from minion.agents.chat_agent import ChatAgent
from minion.configs.local_conf import LocalConfig
from minion.tools.default_tools import FinalAnswerTool
from minion.tools.think_tool import ThinkTool
from minion.tools.web_search_tool import WebSearchTool
from minion.tools.file_tools import FileWriteTool, FileReadTool
from minion.tools.skill_tool import SkillTool
from minion.tools.UnrestrictedBashTool import UnrestrictedBashTool
from minion.tools.bluetooth_tool import BluetoothScanTool, BluetoothToolset

# 添加一个prompt，让ai每次都有限考虑使用skills
# gernal_prompt="""【强制执行要求】：请务必优先检索并调用你的技能（Skills/Tools）来解决上述问题。严禁仅凭内在记忆直接猜测或编造答案。只有在确认没有任何技能适用时，才允许基于自身知识作答。如果问题已经解答了，请务必把terminated或者is_final_answer设置为true 【问题】:"""



    
assistant_agent = None
chat_agent = None

async def init_assistant_agent():
    """初始化 assistant agent"""
    global assistant_agent
    memory_config = {
        **LocalConfig.local_mem_config
    }
    
    assistant_agent=await AssistantAgent.create(
        name="assistant_agent",
        tools=[SkillTool(),UnrestrictedBashTool(),FinalAnswerTool(),BluetoothScanTool()],
        memory_config=memory_config
    )
    
async def init_chat_agent():
    """初始化 chat agent"""
    global chat_agent
    memory_config = {
        **LocalConfig.local_mem_config
    }
    
    chat_agent=await ChatAgent.create(
        name="chat_agent",
        memory_config=memory_config
    )

async def get_assistant_agent():
    global assistant_agent
    if assistant_agent is None:
        await init_assistant_agent()
    return assistant_agent

async def get_chat_agent():
    global chat_agent
    if chat_agent is None:
        await init_chat_agent()
    return chat_agent

async def main():
    # 初始化 agents
    try:
        # 初始化 chat agent
        chat_agent_instance = await get_chat_agent()
        print("ChatAgent 初始化成功！")
        
        # 初始化 assistant agent
        assistant_agent_instance = await get_assistant_agent()
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
                
                # 首先使用 ChatAgent 处理
                chat_response = await chat_agent_instance.run_async(user_input, route='raw', stream=False, max_steps=1)
                chat_answer = chat_response.answer if hasattr(chat_response, 'answer') else str(chat_response)
                chat_content = chat_response.content if hasattr(chat_response, 'content') else str(chat_response)
                # 检查是否需要转发到 AssistantAgent
                if "NEEDS_ASSISTANT_AGENT" in chat_content or "NEEDS_ASSISTANT_AGENT" in chat_answer:
                    # 使用 AssistantAgent 处理
                    async for event in await assistant_agent_instance.run_async( user_input, route='raw', stream=True,max_steps=15):
                        print(event.content, flush=True, end="")
                        # print(event, flush=True, end="")
                        # print(event)
                else:
                    # 直接返回 ChatAgent 的响应
                    print(chat_answer)
                # print()  # 添加换行符，确保提示符在新的一行
            except Exception as e:
                print(f"处理请求失败: {e}")
                continue
    except Exception as e:
        print(f"初始化 agents 失败: {e}")
        return


if __name__ == "__main__":
    asyncio.run(main())
