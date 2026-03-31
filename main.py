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
comfire_prompt="""
你是一个具备工具调用能力的智能助手，必须严格遵守以下执行规则：

【执行原则】
1. 删除文件、系统操作等属于高风险操作
2. 必须先确认，不能直接执行

【确认流程】
当需要确认时，必须返回：

{
  "status": "NEED_CONFIRM",
  "message": "描述操作",
  "action": "操作类型",
  "payload": {...}
}

禁止用自然语言询问确认！

【恢复规则】
用户输入 yes/no 时：
- yes → 执行 payload
- no → 取消

必须基于 payload，不要重新理解用户意图
"""




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
        user_id="ikkk",
        session_id="ikkk",
        agent_id="ikkk",
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
        user_id="ikkk",
        session_id="ikkk",
        agent_id="ikkk",
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

        # ====== 状态机 ======
        state = {
            "status": "IDLE",  # IDLE / WAITING_CONFIRM
            "pending": None
        }

        # 持续交互循环
        while True:
            # 获取用户输入
            user_input = input("\n> ")

            # 空输入跳过
            if not user_input.strip():
                continue

            # 退出
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("再见！")
                break

            # ========================
            # 1️⃣ 如果在等待确认
            # ========================
            if state["status"] == "WAITING_CONFIRM":
                decision = "yes" if user_input.lower() in ["yes", "y", "确认"] else "no"

                print(f"\n用户选择: {decision}")

                # 这里可以直接执行，也可以回给 agent
                pending = state["pending"]

                # 简单示例：直接把确认结果交给 assistant 继续处理
                resume_input = f"""
                用户原始请求：
                {state["pending"]["original_input"]}

                系统提示需要确认：
                {state["pending"]["confirm_payload"]["message"]}

                用户确认结果：
                {decision}

                请继续执行原始任务。
                """

                try:
                    print("\n恢复执行中...")
                    response = await assistant_agent_instance.run_async(
                        resume_input,
                        route='raw',
                        stream=False,
                        max_steps=10
                    )

                    answer = response.answer if hasattr(response, 'answer') else str(response)
                    print(answer)
                except Exception as e:
                    print(f"恢复执行失败: {e}")

                state["status"] = "IDLE"
                state["pending"] = None
                continue

            # ========================
            # 2️⃣ 正常执行
            # ========================
            try:
                print("\n处理中...")

                chat_response = await chat_agent_instance.run_async(
                    user_input,
                    route='raw',
                    stream=False,
                    max_steps=1
                )

                chat_answer = chat_response.answer if hasattr(chat_response, 'answer') else str(chat_response)
                chat_content = chat_response.content if hasattr(chat_response, 'content') else str(chat_response)

                if "NEEDS_ASSISTANT_AGENT" in chat_content or "NEEDS_ASSISTANT_AGENT" in chat_answer:
                    async for event in await assistant_agent_instance.run_async(
                        comfire_prompt+"\n"+"用户输入是："+user_input,
                        route='raw',
                        stream=True,
                        max_steps=15
                    ):
                        # 打印流式内容
                        if hasattr(event, "content") and event.content:
                            print(event.content, flush=True, end="")
                            print(1)
                            eventcontent=event.content
                        # 检测是否有结构化返回（例如 NEED_CONFIRM）
                        if hasattr(event, "answer"):
                            result = event.answer
                            print(result)
                            if isinstance(result, dict) and result.get("status") == "NEED_CONFIRM" or isinstance(eventcontent, dict) and eventcontent.get("status") == "NEED_CONFIRM":
                                print("\n" + result["message"])

                                state["status"] = "WAITING_CONFIRM"
                                state["pending"] = {
                                    "original_input": user_input,
                                    "confirm_payload": result
                                }
                                break
                    print(2)
                else:
                    print(chat_answer)

            except Exception as e:
                print(f"处理请求失败: {e}")
                continue
    except Exception as e:
        print(f"初始化 agents 失败: {e}")
        return


if __name__ == "__main__":
    asyncio.run(main())