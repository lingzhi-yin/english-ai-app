import json
import os

PROMPT = """你是英语口语教练。只返回JSON对象，字段为translation（中文翻译）、scene（中文使用场景）、alternatives（3条英文替换说法数组）、tips（中文表达提示）。不要Markdown。"""

def fallback(sentence, detail="设置 OPENAI_API_KEY 后启用AI分析。"):
    return {"translation": "尚未配置AI接口，暂时无法自动翻译。", "scene": "可用于朗读和跟读训练。", "alternatives": [sentence], "tips": detail, "mode": "local"}

def analyze_sentence(sentence: str) -> dict:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return fallback(sentence)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key, base_url=os.getenv("OPENAI_BASE_URL") or None)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.3,
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": PROMPT}, {"role": "user", "content": sentence}]
        )
        result = json.loads(response.choices[0].message.content)
        result["mode"] = "ai"
        return result
    except Exception as e:
        return fallback(sentence, "AI接口暂时不可用：" + str(e)[:120])
