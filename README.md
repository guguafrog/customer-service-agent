# 智能客服 Agent（LLM Function Calling 版）

基于大语言模型的智能客服机器人，使用 Function Calling 实现意图识别与工具调用。

## 功能

- 查询天气
- 预订机票 / 火车票
- 查询订单物流
- 申请退款
- 转人工客服

## 技术栈

- Python 3.14
- DeepSeek（deepseek-chat）
- OpenAI SDK（Function Calling）
- python-dotenv

## 目录结构

```
├── main.py              # 入口 + 对话循环
├── llm/
│   ├── __init__.py
│   ├── client.py        # LLM Agent：Function Calling 往返逻辑
│   └── tools.py         # 工具定义（JSON Schema + 执行函数）
├── nlu/                 # 旧版规则 NLU，已弃用，仅作参考
├── requirements.txt
└── .env.example         # 环境变量模板
```

## 启动步骤

1. 创建虚拟环境：`python -m venv .venv`
2. 激活虚拟环境：`.venv\Scripts\Activate.ps1`
3. 安装依赖：`pip install -r requirements.txt`
4. 配置密钥：`copy .env.example .env`，编辑 `.env` 填入 `DEEPSEEK_API_KEY`
5. 启动：`python main.py`
6. 输入 `quit` 退出，自动保存对话日志

## 工作原理

```
用户输入 → LLM 决定调用哪个工具（Function Calling）
        → 执行对应 Python 函数
        → 结果回传 LLM
        → 生成自然语言回复
```

与旧版规则 NLU 的区别：不再用关键词匹配意图，而是由 LLM 理解语义后自主决定调用哪个工具、填入什么参数。
