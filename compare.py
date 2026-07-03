import re
from difflib import SequenceMatcher

def words(text):
    return re.findall(r"[a-z0-9']+", text.lower())

def score_pronunciation(target: str, spoken: str) -> dict:
    expected, actual = words(target), words(spoken)
    score = round(SequenceMatcher(None, expected, actual).ratio() * 100)
    missing = [w for w in expected if w not in actual]
    extra = [w for w in actual if w not in expected]
    if score >= 90:
        feedback = "非常棒，表达清晰且完整！"
    elif score >= 75:
        feedback = "整体很好，再留意少数单词。"
    elif score >= 55:
        feedback = "基本正确，建议慢速再读一次。"
    else:
        feedback = "再听一次示范，分词跟读会更容易。"
    return {"score": score, "spoken": spoken, "missing": missing, "extra": extra, "feedback": feedback}
