项目：简易客服Agent
运行环境：Python 3.14
启动步骤：
1. 在项目根目录创建虚拟环境：python -m venv .venv
2. 激活虚拟环境：.venv\Scripts\Activate.ps1
3. 安装依赖：python -m pip install -r requirements.txt
4. 启动程序：python main.py
5. 输入 quit 退出，自动保存对话日志 conversation_log.json

说明：
当前使用【纯规则NLU版本】，无机器学习，规避DLL策略拦截。
如需升级识别能力：替换 nlu/intent_engine.py 为sklearn版本，并且修改main.py中train那一行代码。