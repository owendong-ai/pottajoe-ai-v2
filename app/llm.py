import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def parse_preferences(user_input: str) -> dict:
    """
    把用戶的自然語言描述解析成結構化的咖啡偏好
    例如：「我想要不酸、帶點巧克力味的咖啡」
    → {'acidity': 1, 'bitterness': 4, 'sweetness': 2, 'body': 4, 'flavor': '巧克力', 'roast': '深焙'}
    """
    
    prompt = f"""你是一個專業的手沖咖啡師，請根據顧客的描述，解析出他們的咖啡偏好。

顧客說：「{user_input}」

請回傳一個 JSON 格式，包含以下欄位（不要有其他文字，只要 JSON）：
{{
    "acidity": 1-5的整數（1=極低酸、5=極高酸）,
    "bitterness": 1-5的整數（1=極低苦、5=極高苦）,
    "sweetness": 1-5的整數（1=極低甜、5=極高甜）,
    "body": 1-5的整數（1=極輕盈、5=極醇厚）,
    "flavor": 從以下選一個：果香、堅果、巧克力、花香、焦糖、煙燻,
    "roast": 從以下選一個：淺焙、中焙、深焙,
    "reason": 用一句話解釋你為什麼這樣判斷
}}

如果顧客沒提到某個面向，請根據整體風格合理推斷。"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response_text = message.content[0].text

    # 找出 JSON 的部分（有時 Claude 會多輸出說明文字）
    import re
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        prefs = json.loads(json_match.group())
    else:
        raise ValueError(f"無法解析 JSON：{response_text}")

    return prefs