"""工具定义：把业务能力封装成 LLM 可调用的工具（Function Calling）。

每个工具由两部分组成：
1. 一个普通的 Python 函数（真正执行逻辑）
2. 一段 JSON Schema（告诉 LLM 这个工具叫什么、能干什么、需要哪些参数）
"""
from datetime import datetime

# 模拟数据库（后续步骤会替换成真实 API / 向量库 / RAG）
MOCK_DB = {
    "weather": {
        "北京": {"temp": 15, "condition": "晴天"},
        "上海": {"temp": 20, "condition": "多云"},
    },
    "orders": {
        "ORD123456": {
            "status": "运输中",
            "location": "北京分拨中心",
            "expected": "2024-11-25",
        }
    },
}


# ---------- 真正执行的 Python 函数 ----------
def query_weather(city: str, date: str = "今天") -> str:
    weather = MOCK_DB["weather"].get(city)
    if weather:
        return f"{city} {date}天气：温度 {weather['temp']}°C，{weather['condition']}"
    return f"暂时没有 {city} 的天气信息，可以换个城市试试"


def book_ticket(to_city: str, from_city: str = "当前位置",
                date: str = "近期", quantity: int = 1) -> str:
    order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return (f"订票成功：{from_city} → {to_city}，日期 {date}，{quantity} 张。"
            f"订单号 {order_id}，请在 30 分钟内完成支付。")


def query_order(order_id: str) -> str:
    order = MOCK_DB["orders"].get(order_id)
    if order:
        return (f"订单 {order_id}：状态 {order['status']}，"
                f"当前位置 {order['location']}，预计送达 {order['expected']}")
    return f"未找到订单 {order_id}，请核对订单号"


def request_refund() -> str:
    return ("退款流程：1.提供订单号 2.说明退款原因 3.上传商品照片 4.审核 1-3 个工作日 "
            "5.退款原路返回")


def transfer_to_human() -> str:
    return "已转人工客服，当前排队 3 人，预计等待 2 分钟"


# 工具名 -> 可执行函数 的注册表
TOOL_FUNCTIONS = {
    "query_weather": query_weather,
    "book_ticket": book_ticket,
    "query_order": query_order,
    "request_refund": request_refund,
    "transfer_to_human": transfer_to_human,
}


# ---------- 给 LLM 看的工具描述（OpenAI Function Calling 格式） ----------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "query_weather",
            "description": "查询某城市某天的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名，如 北京"},
                    "date": {"type": "string", "description": "日期，如 今天/明天"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_ticket",
            "description": "预订机票或火车票",
            "parameters": {
                "type": "object",
                "properties": {
                    "to_city": {"type": "string", "description": "目的地城市"},
                    "from_city": {"type": "string", "description": "出发地城市"},
                    "date": {"type": "string", "description": "出发日期"},
                    "quantity": {"type": "integer", "description": "票数"},
                },
                "required": ["to_city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "query_order",
            "description": "查询订单的物流状态",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string",
                                 "description": "订单号，如 ORD123456"},
                },
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "request_refund",
            "description": "发起退款或退货申请",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "transfer_to_human",
            "description": "转接人工客服",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]
