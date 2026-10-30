"""LLM Agent：用 Function Calling 决定「要不要调工具、调哪个、参数是什么」。

流程（一次工具调用回合）：
1. 把用户消息 + 工具定义发给 LLM
2. LLM 返回两种情况之一：
   a. tool_calls -> 执行对应 Python 函数，把结果回传
   b. 普通文本   -> 直接回复
3. 有 tool_calls 时，再次调用 LLM，让它把工具结果组织成自然语言

注：当前是「单回合」版本。第 2 步会把它升级成完整的 Agent 循环（ReAct / LangGraph），
支持多步工具调用和自主决策。
"""
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from llm.tools import TOOL_FUNCTIONS, TOOLS

load_dotenv()


class CustomerServiceAgent:
    def __init__(self):
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError(
                "缺少 DEEPSEEK_API_KEY，请在项目根目录的 .env 文件或环境变量中配置"
            )
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.model = "deepseek-chat"

        self.system_prompt = (
            "你是一个智能客服助手。根据用户需求选择合适的工具（function）来完成任务，"
            "然后把工具返回的结果用自然、友好的中文告诉用户。"
            "如果用户只是问候或闲聊，直接回复即可，不要调用工具。"
        )
        # 多轮对话的上下文：system 开头，后续追加 user/assistant/tool
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})

        # 第一次调用：让 LLM 决定是否调用工具
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=TOOLS,
        )
        msg = resp.choices[0].message

        if msg.tool_calls:
            # 记录 assistant 提出的 tool_calls（注意格式，这是面试常考点）
            self.messages.append({
                "role": "assistant",
                "content": msg.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ],
            })

            # 逐个执行工具，结果以 role="tool" 回传
            for tc in msg.tool_calls:
                name = tc.function.name
                args = json.loads(tc.function.arguments or "{}")
                func = TOOL_FUNCTIONS.get(name)
                result = func(**args) if func else f"未知工具：{name}"
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result,
                })

            # 第二次调用：让 LLM 把工具结果组织成自然语言
            final = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
            )
            answer = final.choices[0].message.content or ""
        else:
            answer = msg.content or ""

        self.messages.append({"role": "assistant", "content": answer})
        return answer
