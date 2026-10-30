import json
from datetime import datetime

from llm.client import CustomerServiceAgent


class SmartCustomerServiceBot:
    """智能客服机器人（LLM Function Calling 版）"""

    def __init__(self):
        # 决策层从「规则引擎」换成了「LLM Agent」
        self.agent = CustomerServiceAgent()

        # 对话历史（记录到内存 + 可落盘）
        self.conversation_history = []

        print("🤖 智能客服机器人已启动（LLM Function Calling 版）！")
        print("=" * 60)

    def chat(self, user_input):
        """处理用户消息"""
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat(),
        })

        # 由 LLM 自主决定调用哪个工具并生成回复
        response = self.agent.chat(user_input)

        self.conversation_history.append({
            "role": "bot",
            "content": response,
            "timestamp": datetime.now().isoformat(),
        })
        return response

    def get_conversation_history(self):
        return self.conversation_history

    def save_conversation(self, filename="conversation_log.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
        print(f"📝 对话记录已保存到 {filename}")


def main():
    bot = SmartCustomerServiceBot()

    print("💬 开始对话（输入 'quit' 退出）\n")
    print("=" * 60)

    while True:
        user_input = input("\n👤 您: ")

        if user_input.lower() in ["quit", "exit", "退出"]:
            print("\n👋 感谢使用！再见！")
            bot.save_conversation()
            break

        if not user_input.strip():
            continue

        response = bot.chat(user_input)
        print(f"\n🤖 客服: {response}")


if __name__ == "__main__":
    main()
