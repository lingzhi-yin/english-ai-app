import os
from flask import Flask, jsonify, render_template, request, send_from_directory
from ocr import extract_english
from ai import analyze_sentence
from compare import score_pronunciation
from storage import save_record, get_records
from voice import voice_config

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/sw.js")
def sw():
    response = send_from_directory("static", "sw.js")
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Cache-Control"] = "no-cache"
    return response

@app.post("/api/ocr")
def ocr():
    image = request.files.get("image")
    if not image:
        return jsonify(error="请选择图片"), 400
    try:
        return jsonify(text=extract_english(image.read()))
    except ValueError as e:
        return jsonify(error=str(e)), 400
    except RuntimeError as e:
        return jsonify(error=str(e)), 503

@app.post("/api/analyze")
def analyze():
    sentence = (request.get_json(silent=True) or {}).get("sentence", "").strip()
    if not sentence:
        return jsonify(error="请输入英文句子"), 400
    result = analyze_sentence(sentence)
    save_record({"sentence": sentence, "analysis": result})
    return jsonify(result)

@app.post("/api/score")
def score():
    data = request.get_json(silent=True) or {}
    if not data.get("target") or not data.get("spoken"):
        return jsonify(error="缺少原句或跟读结果"), 400
    result = score_pronunciation(data["target"], data["spoken"])
    save_record({"sentence": data["target"], "pronunciation": result})
    return jsonify(result)

@app.get("/api/records")
def records():
    return jsonify(get_records(request.args.get("date")))

@app.get("/api/voice-config")
def config():
    return jsonify(voice_config())

@app.errorhandler(413)
def too_large(_):
    return jsonify(error="图片不能超过12MB"), 413

if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 5000)), debug=os.getenv("FLASK_DEBUG") == "1")
