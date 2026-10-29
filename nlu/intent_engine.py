import re

class IntentRecognitionEngine:
    def __init__(self):
        self.is_trained = True
        # 关键词映射
        self.intent_keywords = {
            "查询天气": ["天气", "多少度", "下雨", "晴天"],
            "订票": ["订票", "买票", "机票", "火车票"],
            "查询订单": ["订单", "物流", "包裹", "快递"],
            "退款": ["退款", "退货", "不想要"],
            "人工客服": ["转人工", "找客服", "人工服务"],
            "问候": ["你好", "在吗", "嗨", "hello"]
        }
        # 槽位正则
        self.re_city = re.compile(r"(北京|上海|武汉|广州|深圳)")
        self.re_orderid = re.compile(r"ORD\d+")
        self.re_date = re.compile(r"今天|明天|后天")

    def train(self, texts, labels):
        # 占位方法，兼容原有调用，规则版本不需要训练
        print("✅ 规则意图引擎加载完成（无机器学习训练）")

    def _extract_slot(self, text, intent):
        slots = {}
        if intent == "查询天气":
            c = self.re_city.search(text)
            d = self.re_date.search(text)
            if c: slots["city"] = c.group()
            if d: slots["date"] = d.group()
        elif intent == "查询订单":
            o = self.re_orderid.search(text)
            if o: slots["order_id"] = o.group()
        elif intent == "订票":
            cities = self.re_city.findall(text)
            if len(cities)>=1: slots["to"] = cities[-1]
            if len(cities)>=2: slots["from"] = cities[0]
        return slots

    def process(self, text):
        text = text.lower()
        hit_intent = None
        for intent, words in self.intent_keywords.items():
            for w in words:
                if w in text:
                    hit_intent = intent
                    break
            if hit_intent:
                break
        if not hit_intent:
            return {"status":"uncertain","message":"不好意思，我没听懂您的意思"}
        
        slots = self._extract_slot(text, hit_intent)
        need_slots = {
            "查询天气":["city"],
            "查询订单":["order_id"],
            "订票":["to"]
        }
        required = need_slots.get(hit_intent, [])
        missing = [k for k in required if k not in slots]
        if missing:
            msg_map = {
                "city":"请问你想查询哪个城市？",
                "order_id":"请提供订单号，格式如ORD123456",
                "to":"请问你要订去哪里？"
            }
            return {
                "status":"incomplete",
                "intent":hit_intent,
                "slots":slots,
                "message":msg_map[missing[0]]
            }
        return {"status":"ok","intent":hit_intent,"slots":slots}