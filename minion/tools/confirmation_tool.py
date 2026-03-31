#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户确认工具

这个工具用于向用户请求确认，用户可以选择确认或拒绝某个操作。
"""
from minion.tools.base_tool import BaseTool


class ConfirmationTool(BaseTool):
    """
    用户确认工具

    用于向用户请求确认，用户可以选择确认或拒绝某个操作。
    """

    name: str = "confirmation"
    description: str = "向用户请求确认，用户可以选择确认或拒绝某个操作"
    inputs: dict[str, dict[str, any]] = {
        "message": {
            "type": "string",
            "description": "要向用户显示的确认消息",
            "required": True
        },
        "default": {
            "type": "string",
            "description": "默认选择，可选值为'yes'或'no'",
            "required": False
        }
    }
    output_type: str = "string"
    output_schema: dict[str, any] = {
        "type": "string",
        "description": "用户的选择，值为'yes'或'no'"
    }
    readonly: bool = True
    needs_state: bool = False

    def forward(self, message: str, default: str = "no") -> str:
        """
        向用户请求确认

        Args:
            message: 要向用户显示的确认消息
            default: 默认选择，可选值为'yes'或'no'，默认为'no'

        Returns:
            str: 用户的选择，值为'yes'或'no'
        """
        # 验证默认值
        if default not in ['yes', 'no']:
            default = 'no'

        # 不直接进行 input 阻塞，而是返回一个“需要用户确认”的结构化信号
        return {
            "status": "NEED_CONFIRM",
            "message": message,
            "default": default
        }
