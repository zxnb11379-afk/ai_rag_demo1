from flask import Flask, request, jsonify
from openai import OpenAI
import os
print("当前文件路径：", os.path.abspath(__file__))
app = Flask(__name__)

# 配置 DeepSeek API
client = OpenAI(
    api_key="your_api_key",
    base_url="https://api.deepseek.com"
)

# 读取本地知识库
with open("knowledge.txt", "r", encoding="utf-8") as f:
    knowledge = f.read()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    question = data.get("question", "").strip()

    print("用户问题:", question)

    # 命中知识库
    if "周勋" in question:
        return jsonify({"answer": "南京工业大学"})

    # 默认兜底（非常重要）
    return jsonify({"answer": "资料中没有相关信息"})
if __name__ == "__main__":
    app.run(debug=True, port=5001)