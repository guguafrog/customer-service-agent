import json
from datetime import datetime
from nlu.intent_engine import IntentRecognitionEngine


class SmartCustomerServiceBot:
    """智能客服机器人"""

    def __init__(self):
        # 初始化各个模块
        self.engine = IntentRecognitionEngine()

        # 对话历史
        self.conversation_history = []

        # 当前对话状态
        self.current_intent = None
        self.current_slots = {}

        # 模拟数据库
        self.mock_database = {
            "weather": {
                "北京": {"temp": 15, "condition": "晴天"},
                "上海": {"temp": 20, "condition": "多云"},
            },
            "orders": {
                "ORD123456": {
                    "status": "运输中",
                    "location": "北京分拨中心",
                    "expected": "2024-11-25"
                }
            }
        }

        print("🤖 智能客服机器人已启动！")
        print("=" * 60)

    def train(self):
        """训练意图识别模型"""
        print("📚 正在训练意图识别模型...")

        # 训练数据
        texts = [
            "今天天气怎么样", "北京现在多少度", "会下雨吗", "明天晴天吗",
            "帮我订票", "买张去上海的票", "预订机票", "购买火车票",
            "我的订单在哪", "快递到了吗", "查询物流", "包裹什么时候到",
            "我要退款", "申请退货", "不想要了", "能退吗",
            "转人工", "找客服", "人工服务", "联系客服",
            "你好", "在吗", "嗨", "hello"
        ]

        labels = [
            "查询天气", "查询天气", "查询天气", "查询天气",
            "订票", "订票", "订票", "订票",
            "查询订单", "查询订单", "查询订单", "查询订单",
            "退款", "退款", "退款", "退款",
            "人工客服", "人工客服", "人工客服", "人工客服",
            "问候", "问候", "问候", "问候"
        ]

        self.engine.train(texts, labels)
        print("✅ 模型训练完成！\n")

    def chat(self, user_input):
        """处理用户消息"""
        # 记录对话
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })

        # 意图识别
        result = self.engine.process(user_input)

        # 根据状态生成响应
        response = self._generate_response(result)

        # 记录机器人响应
        self.conversation_history.append({
            "role": "bot",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })

        return response

    def _generate_response(self, result):
        """生成响应"""
        status = result.get("status")

        # 情况1: 不确定意图
        if status == "uncertain":
            return result["message"]

        # 情况2: 槽位不完整
        if status == "incomplete":
            self.current_intent = result["intent"]
            self.current_slots.update(result["slots"])
            return result["message"]

        # 情况3: 意图和槽位都完整
        intent = result["intent"]
        slots = result["slots"]

        # 执行相应动作
        if intent == "问候":
            return self._handle_greeting()
        elif intent == "查询天气":
            return self._handle_weather_query(slots)
        elif intent == "订票":
            return self._handle_booking(slots)
        elif intent == "查询订单":
            return self._handle_order_query(slots)
        elif intent == "退款":
            return self._handle_refund(slots)
        elif intent == "人工客服":
            return self._handle_human_service()
        else:
            return "抱歉，我还在学习中，这个问题我暂时回答不了。"

    def _handle_greeting(self):
        """处理问候"""
        return "您好！我是智能客服小助手，很高兴为您服务！😊\n\n我可以帮您：\n1. 查询天气\n2. 预订机票\n3. 查询订单\n4. 处理退款\n5. 转接人工客服\n\n请问有什么可以帮您？"

    def _handle_weather_query(self, slots):
        """处理天气查询"""
        city = slots.get("city", "北京")
        date = slots.get("date", "今天")

        # 模拟查询天气API
        weather_data = self.mock_database["weather"].get(city)

        if weather_data:
            return f"📍 {city} {date}的天气：\n" \
                   f"🌡️ 温度：{weather_data['temp']}°C\n" \
                   f"☀️ 天气：{weather_data['condition']}\n\n" \
                   f"还有其他需要帮助的吗？"
        else:
            return f"抱歉，暂时没有{city}的天气信息。您可以换个城市试试。"

    def _handle_booking(self, slots):
        """处理订票"""
        to_city = slots.get("to", "未知")
        from_city = slots.get("from", "当前位置")
        date = slots.get("date", "近期")
        quantity = slots.get("quantity", 1)

        # 模拟订票流程
        order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"

        return f"✈️ 订票信息确认：\n" \
               f"出发地：{from_city}\n" \
               f"目的地：{to_city}\n" \
               f"出发日期：{date}\n" \
               f"票数：{quantity}张\n\n" \
               f"订单已生成！\n" \
               f"📋 订单号：{order_id}\n\n" \
               f"请在30分钟内完成支付。还有其他需要吗？"

    def _handle_order_query(self, slots):
        """处理订单查询"""
        order_id = slots.get("order_id")

        if order_id and order_id in self.mock_database["orders"]:
            order = self.mock_database["orders"][order_id]
            return f"📦 订单查询结果：\n" \
                   f"订单号：{order_id}\n" \
                   f"状态：{order['status']}\n" \
                   f"当前位置：{order['location']}\n" \
                   f"预计送达：{order['expected']}\n\n" \
                   f"还有其他需要帮助的吗？"
        else:
            return "请提供您的订单号，格式如：ORD123456"

    def _handle_refund(self, slots):
        """处理退款"""
        return "💰 退款流程说明：\n" \
               "1. 请提供订单号\n" \
               "2. 说明退款原因\n" \
               "3. 上传商品照片（如适用）\n" \
               "4. 等待审核（1-3个工作日）\n" \
               "5. 退款将原路返回\n\n" \
               "需要我帮您转接人工客服处理吗？"

    def _handle_human_service(self):
        """处理人工客服请求"""
        return "正在为您转接人工客服...\n" \
               "👨‍💼 当前排队人数：3人\n" \
               "⏱️ 预计等待时间：2分钟\n\n" \
               "在等待期间，您可以继续向我咨询其他问题。"

    def get_conversation_history(self):
        """获取对话历史"""
        return self.conversation_history

    def save_conversation(self, filename="conversation_log.json"):
        """保存对话记录"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f,
                      ensure_ascii=False, indent=2)
        print(f"📝 对话记录已保存到 {filename}")


# ========== 使用示例 ==========
def main():
    # 创建机器人
    bot = SmartCustomerServiceBot()

    # 训练模型
    bot.train()

    # 模拟对话
    print("💬 开始对话（输入 'quit' 退出）\n")
    print("=" * 60)

    while True:
        user_input = input("\n👤 您: ")

        if user_input.lower() in ['quit', 'exit', '退出']:
            print("\n👋 感谢使用！再见！")
            bot.save_conversation()
            break

        if not user_input.strip():
            continue

        # 获取机器人响应
        response = bot.chat(user_input)
        print(f"\n🤖 客服: {response}")


if __name__ == "__main__":
    main()